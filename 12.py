import re
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [LOG_ANALYTICS] %(message)s")

SAMPLE_LOGS = """
2026-11-05 14:01:22 [INFO] [CORE_NODE] System heartbeat established successfully.
2026-11-05 14:01:25 [WARNING] [AUTH_SERVICE] High latency detected on token verification: 450ms.
2026-11-05 14:01:28 [ERROR] [DB_POOL] Connection refused on endpoint 127.0.0.1:5432.
2026-11-05 14:01:30 [INFO] [CORE_NODE] Telemetry stream synchronized.
2026-11-05 14:01:35 [CRITICAL] [PAYMENT_GW] Gateway timeout during transaction settlement.
"""

def parse_logs(raw_logs: str) -> dict:
    log_pattern = re.compile(
        r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
        r"\[(?P<level>\w+)\]\s+"
        r"\[(?P<module>[\w_]+)\]\s+"
        r"(?P<message>.*)"
    )

    parsed_records = []
    level_counts = {}

    for line in raw_logs.strip().split("\n"):
        match = log_pattern.match(line)
        if match:
            rec = match.groupdict()
            parsed_records.append(rec)
            lvl = rec["level"]
            level_counts[lvl] = level_counts.get(lvl, 0) + 1

    report = {
        "total_records": len(parsed_records),
        "level_breakdown": level_counts,
        "records": parsed_records
    }
    return report

if __name__ == "__main__":
    report = parse_logs(SAMPLE_LOGS)
    report_path = Path("log_analytics_report.json")
    
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
        
    logging.info(f"Log analytics compilation complete. Report written to {report_path}")
    print(json.dumps(report, indent=4))
    