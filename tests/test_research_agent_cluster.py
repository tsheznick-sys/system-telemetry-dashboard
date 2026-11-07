import asyncio
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from research_agent_cluster import (
    ResearchScraperAgent,
    ResearchSynthesizerOrchestrator,
    VectorMemoryStore,
    _PageTextParser,
)


class ResearchAgentTests(unittest.TestCase):
    def test_hash_vector_search_is_deterministic_and_query_relevant(self) -> None:
        store = VectorMemoryStore()
        store.add_document(
            "Python async",
            "Asynchronous Python programming with asyncio tasks",
            "https://example.org/python",
        )
        store.add_document(
            "Gardening",
            "Tomatoes need sunlight, watering, and healthy soil",
            "https://example.org/garden",
        )

        first = store.semantic_search("async Python asyncio")
        second = store.semantic_search("async Python asyncio")

        self.assertEqual(first, second)
        self.assertEqual(first[0]["source"], "https://example.org/python")
        self.assertEqual(
            first[0]["similarity_method"],
            "hashed lexical cosine similarity",
        )

    def test_html_parser_omits_script_and_style_content(self) -> None:
        parser = _PageTextParser()
        parser.feed(
            "<html><title>Research title</title><body>Visible "
            "<script>secret()</script><style>.x{}</style> text</body></html>"
        )
        parser.close()

        self.assertEqual(" ".join(parser.title_parts), "Research title")
        self.assertEqual(" ".join(parser.text_parts), "Research title Visible text")

    def test_output_escaping_blocks_markdown_and_csv_formulas(self) -> None:
        escaped = ResearchSynthesizerOrchestrator._markdown_escape(
            "<script>alert(1)</script> *text*"
        )

        self.assertNotIn("<script>", escaped)
        self.assertIn(r"\*text\*", escaped)
        self.assertEqual(
            ResearchSynthesizerOrchestrator._csv_safe("  =1+1"),
            "'  =1+1",
        )

    def test_url_validation_rejects_non_https_and_private_addresses(self) -> None:
        agent = ResearchScraperAgent()
        for url in (
            "http://example.org/",
            "https://127.0.0.1/",
            "https://user:pass@example.org/",
            "https://example.org:8443/",
        ):
            with self.subTest(url=url), self.assertRaises(ValueError):
                asyncio.run(agent._validated_url(url))

    def test_pipeline_writes_dossier_and_csv_from_fetched_sources(self) -> None:
        async def run_pipeline(output_dir: Path) -> dict:
            orchestrator = ResearchSynthesizerOrchestrator(output_dir)
            source_result = {
                "url": "https://example.org/research",
                "title": "Python concurrency",
                "extracted_text": "Python asyncio concurrency and bounded tasks.",
                "status": "SUCCESS",
                "content_type": "text/plain",
                "bytes_read": 48,
                "elapsed_seconds": 0.01,
            }
            with patch.object(
                orchestrator.agent,
                "crawl_target",
                new=AsyncMock(return_value=source_result),
            ):
                return await orchestrator.execute_research_pipeline(
                    "Python asyncio", ["https://example.org/research"]
                )

        with tempfile.TemporaryDirectory() as directory:
            result = asyncio.run(run_pipeline(Path(directory)))
            dossier_path = Path(directory) / result["output_files"]["dossier"]
            csv_path = Path(directory) / result["output_files"]["csv"]

            self.assertTrue(dossier_path.is_file())
            self.assertTrue(csv_path.is_file())
            self.assertIn("Python concurrency", dossier_path.read_text())
            self.assertEqual(
                result["matches"][0]["source"],
                "https://example.org/research",
            )


if __name__ == "__main__":
    unittest.main()
