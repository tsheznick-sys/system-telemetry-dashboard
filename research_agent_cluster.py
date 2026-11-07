from __future__ import annotations

import argparse
import asyncio
import hashlib
import html
import ipaddress
import logging
import re
import socket
import tempfile
import time
import uuid
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

import aiohttp
import numpy as np
import pandas as pd

MAX_TARGETS = 5
MAX_RESPONSE_BYTES = 1_000_000
MAX_DOCUMENT_CHARS = 20_000
REQUEST_TIMEOUT_SECONDS = 12
VECTOR_DIMENSION = 512
WORD_PATTERN = re.compile(r"[^\W_]+", re.UNICODE)

logger = logging.getLogger(__name__)


class _PageTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.text_parts: list[str] = []
        self._in_title = False
        self._ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        if tag in {"script", "style", "noscript", "svg"}:
            self._ignored_depth += 1
        elif tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg"} and self._ignored_depth:
            self._ignored_depth -= 1
        elif tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        text = " ".join(data.split())
        if not text or self._ignored_depth:
            return
        if self._in_title:
            self.title_parts.append(text)
        self.text_parts.append(text)


class _PinnedPublicResolver(aiohttp.abc.AbstractResolver):
    """Resolve a host only to IPs already checked as globally routable."""

    def __init__(self, hostname: str, addresses: list[tuple[int, str]]) -> None:
        self.hostname = hostname
        self.addresses = addresses

    async def resolve(
        self, host: str, port: int = 0, family: int = socket.AF_INET
    ) -> list[dict[str, Any]]:
        if host.casefold() != self.hostname.casefold():
            raise OSError("Unexpected hostname during public URL resolution.")
        return [
            {
                "hostname": host,
                "host": address,
                "port": port,
                "family": address_family,
                "proto": 0,
                "flags": 0,
            }
            for address_family, address in self.addresses
            if family in (socket.AF_UNSPEC, address_family)
        ]

    async def close(self) -> None:
        return None


class VectorMemoryStore:
    """Deterministic hashed-token vectors for lightweight lexical retrieval."""

    def __init__(self, vector_dimension: int = VECTOR_DIMENSION) -> None:
        if vector_dimension < 8:
            raise ValueError("Vector dimension must be at least 8.")
        self.dimension = vector_dimension
        self.documents: list[dict[str, Any]] = []
        self.embeddings: list[np.ndarray] = []

    def _vectorize(self, text: str) -> np.ndarray:
        tokens = [token.casefold() for token in WORD_PATTERN.findall(text)]
        features = tokens + [
            f"{left}_{right}" for left, right in zip(tokens, tokens[1:])
        ]
        vector = np.zeros(self.dimension, dtype=float)
        for feature, count in Counter(features).items():
            digest = hashlib.blake2b(
                feature.encode("utf-8"), digest_size=8
            ).digest()
            value = int.from_bytes(digest, "big")
            index = value % self.dimension
            sign = 1.0 if value & (1 << 63) else -1.0
            vector[index] += sign * (1.0 + np.log(count))
        norm = float(np.linalg.norm(vector))
        if norm:
            vector /= norm
        return vector

    def add_document(self, title: str, text: str, source: str) -> None:
        self.documents.append(
            {
                "title": title,
                "text": text[:MAX_DOCUMENT_CHARS],
                "source": source,
                "indexed_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        self.embeddings.append(self._vectorize(f"{title} {text}"))

    def semantic_search(self, query: str, top_k: int = 3) -> list[dict[str, Any]]:
        if top_k < 1:
            raise ValueError("top_k must be at least 1.")
        if not self.embeddings:
            return []
        query_vector = self._vectorize(query)
        matrix = np.vstack(self.embeddings)
        similarities = matrix @ query_vector
        top_indices = np.argsort(similarities)[::-1][:top_k]
        return [
            {
                **self.documents[int(index)],
                "similarity_score": round(float(similarities[index]), 4),
                "similarity_method": "hashed lexical cosine similarity",
            }
            for index in top_indices
        ]


class ResearchScraperAgent:
    """Fetch and extract bounded text from public HTTPS pages."""

    async def _resolve_public_host(
        self, hostname: str, port: int
    ) -> list[tuple[int, str]]:
        loop = asyncio.get_running_loop()
        try:
            records = await loop.getaddrinfo(
                hostname,
                port,
                family=socket.AF_UNSPEC,
                type=socket.SOCK_STREAM,
            )
        except OSError as exc:
            raise ValueError(f"Could not resolve research host {hostname}.") from exc

        addresses: set[tuple[int, str]] = set()
        for record in records:
            family = record[0]
            address = ipaddress.ip_address(record[4][0])
            if not address.is_global:
                raise ValueError("Research URLs must resolve only to public IP addresses.")
            addresses.add((family, str(address)))
        if not addresses:
            raise ValueError(f"No public addresses found for {hostname}.")
        return sorted(addresses)

    async def _validated_url(
        self, raw_url: str
    ) -> tuple[str, str, list[tuple[int, str]]]:
        if len(raw_url) > 2048:
            raise ValueError("Research URL exceeds the 2048-character limit.")
        parsed = urlsplit(raw_url.strip())
        if (
            parsed.scheme.lower() != "https"
            or not parsed.hostname
            or parsed.username is not None
            or parsed.password is not None
            or parsed.fragment
        ):
            raise ValueError("Only credential-free HTTPS URLs without fragments are allowed.")
        try:
            port = parsed.port or 443
        except ValueError as exc:
            raise ValueError("Research URL contains an invalid port.") from exc
        if port != 443:
            raise ValueError("Research URLs may use only the standard HTTPS port.")

        hostname = parsed.hostname.rstrip(".").encode("idna").decode("ascii")
        try:
            literal_address = ipaddress.ip_address(hostname)
        except ValueError:
            addresses = await self._resolve_public_host(hostname, port)
        else:
            if not literal_address.is_global:
                raise ValueError("Research URL must use a public IP address.")
            family = socket.AF_INET6 if literal_address.version == 6 else socket.AF_INET
            addresses = [(family, str(literal_address))]

        safe_host = f"[{hostname}]" if ":" in hostname else hostname
        safe_url = urlunsplit(
            ("https", safe_host, parsed.path or "/", parsed.query, "")
        )
        return safe_url, hostname, addresses

    async def crawl_target(self, target_url: str) -> dict[str, Any]:
        started = time.perf_counter()
        try:
            url, hostname, addresses = await self._validated_url(target_url)
            connector = aiohttp.TCPConnector(
                resolver=_PinnedPublicResolver(hostname, addresses),
                use_dns_cache=False,
                limit=1,
            )
            timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT_SECONDS)
            async with aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={"User-Agent": "SystemTelemetryResearch/1.0"},
                trust_env=False,
            ) as session:
                async with session.get(url, allow_redirects=False) as response:
                    if 300 <= response.status < 400:
                        raise ValueError("Redirects are not followed for research URLs.")
                    response.raise_for_status()
                    content_type = response.headers.get("Content-Type", "").split(";")[0].lower()
                    if content_type not in {
                        "text/html",
                        "text/plain",
                        "application/xhtml+xml",
                    }:
                        raise ValueError(
                            f"Unsupported response content type: {content_type or 'unknown'}."
                        )
                    length_header = response.headers.get("Content-Length")
                    if length_header and int(length_header) > MAX_RESPONSE_BYTES:
                        raise ValueError("Research page exceeds the 1 MB response limit.")
                    chunks: list[bytes] = []
                    total_bytes = 0
                    async for chunk in response.content.iter_chunked(16_384):
                        total_bytes += len(chunk)
                        if total_bytes > MAX_RESPONSE_BYTES:
                            raise ValueError("Research page exceeds the 1 MB response limit.")
                        chunks.append(chunk)
                    charset = response.charset or "utf-8"
                    body = b"".join(chunks).decode(charset, errors="replace")

            if content_type == "text/plain":
                title = urlsplit(url).path.rsplit("/", 1)[-1] or hostname
                text = " ".join(body.split())
            else:
                parser = _PageTextParser()
                parser.feed(body)
                parser.close()
                title = " ".join(" ".join(parser.title_parts).split()) or hostname
                text = " ".join(" ".join(parser.text_parts).split())
            if not text:
                raise ValueError("No readable text was found on the page.")
            return {
                "url": url,
                "title": title[:300],
                "extracted_text": text[:MAX_DOCUMENT_CHARS],
                "status": "SUCCESS",
                "content_type": content_type,
                "bytes_read": total_bytes,
                "elapsed_seconds": round(time.perf_counter() - started, 3),
            }
        except (
            aiohttp.ClientError,
            asyncio.TimeoutError,
            OSError,
            UnicodeError,
            LookupError,
            ValueError,
        ) as exc:
            logger.warning("Research fetch failed for %s: %s", target_url, exc)
            return {
                "url": target_url,
                "title": "",
                "extracted_text": "",
                "status": "FAILED",
                "error": str(exc),
                "elapsed_seconds": round(time.perf_counter() - started, 3),
            }


class ResearchSynthesizerOrchestrator:
    """Fetch public pages, rank them lexically, and produce evidence-linked output."""

    def __init__(self, output_dir: str | Path = "./research_output") -> None:
        self.output_dir = Path(output_dir).expanduser().resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.vector_db = VectorMemoryStore()
        self.agent = ResearchScraperAgent()

    async def execute_research_pipeline(
        self, research_query: str, target_urls: list[str]
    ) -> dict[str, Any]:
        query = research_query.strip()
        if not query:
            raise ValueError("Research query cannot be empty.")
        if not 1 <= len(target_urls) <= MAX_TARGETS:
            raise ValueError(f"Provide between 1 and {MAX_TARGETS} research URLs.")
        if len({url.strip() for url in target_urls}) != len(target_urls):
            raise ValueError("Research URLs must be unique.")

        started = time.perf_counter()
        results = await asyncio.gather(
            *(self.agent.crawl_target(url) for url in target_urls)
        )
        for result in results:
            if result["status"] == "SUCCESS":
                self.vector_db.add_document(
                    result["title"], result["extracted_text"], result["url"]
                )
        matches = self.vector_db.semantic_search(query, top_k=MAX_TARGETS)
        elapsed = round(time.perf_counter() - started, 3)
        dossier = self._compile_dossier(query, results, matches, elapsed)
        run_id = uuid.uuid4().hex
        dossier_path = self.output_dir / f"research-{run_id}.md"
        csv_path = self.output_dir / f"research-{run_id}.csv"
        self._write_dossier(dossier_path, dossier)
        export_results = [
            {
                key: self._csv_safe(value)
                for key, value in result.items()
            }
            for result in results
        ]
        pd.DataFrame(export_results).to_csv(csv_path, index=False)
        return {
            "query": query,
            "results": results,
            "matches": matches,
            "dossier": dossier,
            "elapsed_seconds": elapsed,
            "output_files": {
                "dossier": dossier_path.name,
                "csv": csv_path.name,
            },
        }

    @staticmethod
    def _compile_dossier(
        query: str,
        results: list[dict[str, Any]],
        matches: list[dict[str, Any]],
        elapsed: float,
    ) -> str:
        lines = [
            "# Public Web Research Dossier",
            "",
            f"- Query: {ResearchSynthesizerOrchestrator._markdown_escape(query)}",
            f"- Compiled (UTC): {datetime.now(timezone.utc).isoformat()}",
            f"- Sources requested: {len(results)}",
            f"- Sources fetched: {sum(item['status'] == 'SUCCESS' for item in results)}",
            f"- Elapsed: {elapsed:.3f} seconds",
            "- Ranking: deterministic hashed lexical cosine similarity; not an LLM embedding.",
            "",
            "## Sources",
        ]
        for result in results:
            lines.extend(
                [
                    "",
                    f"### {ResearchSynthesizerOrchestrator._markdown_escape(result['title'] or result['url'])}",
                    f"- URL: `{result['url'].replace('`', '%60')}`",
                    f"- Status: {result['status']}",
                ]
            )
            if result["status"] == "SUCCESS":
                lines.extend(
                    [
                        f"- Content type: {result['content_type']}",
                        f"- Bytes read: {result['bytes_read']}",
                    ]
                )
            else:
                lines.append(
                    f"- Error: {ResearchSynthesizerOrchestrator._markdown_escape(result['error'])}"
                )

        lines.extend(["", "## Ranked source excerpts"])
        if not matches:
            lines.append("No sources were successfully fetched.")
        for index, match in enumerate(matches, start=1):
            lines.extend(
                [
                    "",
                    f"### {index}. {ResearchSynthesizerOrchestrator._markdown_escape(match['title'])}",
                    f"- URL: `{match['source'].replace('`', '%60')}`",
                    f"- Lexical similarity: {match['similarity_score']}",
                    f"- Excerpt: {ResearchSynthesizerOrchestrator._markdown_escape(match['text'])}",
                ]
            )
        lines.append("")
        return "\n".join(lines)

    @staticmethod
    def _markdown_escape(value: str) -> str:
        escaped = html.escape(value, quote=True)
        return re.sub(r"([\\`*_{}\[\]()#+\-.!|>])", r"\\\1", escaped)

    @staticmethod
    def _csv_safe(value: Any) -> Any:
        if not isinstance(value, str):
            return value
        if value.lstrip()[:1] in {"=", "+", "-", "@"}:
            return "'" + value
        return value

    @staticmethod
    def _write_dossier(path: Path, content: str) -> None:
        temporary_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=path.parent,
                prefix=f".{path.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                temporary_file.write(content)
                temporary_path = Path(temporary_file.name)
            temporary_path.replace(path)
        except OSError:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
            raise


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch public HTTPS pages and create a local research dossier."
    )
    parser.add_argument("query", help="Research query used to rank fetched pages.")
    parser.add_argument(
        "urls",
        nargs="+",
        help=f"One to {MAX_TARGETS} public HTTPS URLs.",
    )
    parser.add_argument("--output-dir", default="./research_output")
    args = parser.parse_args()
    try:
        result = asyncio.run(
            ResearchSynthesizerOrchestrator(args.output_dir).execute_research_pipeline(
                args.query, args.urls
            )
        )
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(result["dossier"])
    print(f"Dossier: {result['output_files']['dossier']}")
    print(f"CSV: {result['output_files']['csv']}")


if __name__ == "__main__":
    main()
