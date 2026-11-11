"""
Module 140 — Distributed Job Scheduler with Leases
Loggy3 Enterprise Platform · Distributed Systems Library (Module 140/150)

Workers lease jobs with a deadline; expired leases are reclaimed and reassigned (at-least-once).
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-140] %(message)s")
log = logging.getLogger("Module-140")


class JobScheduler:
    def __init__(self, lease_sec: float = 0.2):
        self.lease_sec = lease_sec
        self.jobs: dict[str, dict] = {}

    def enqueue(self, job_id: str) -> None:
        self.jobs[job_id] = {"status": "queued", "owner": None, "lease_expiry": 0.0, "attempts": 0}

    def lease(self, worker: str) -> str | None:
        now = time.monotonic()
        for jid, job in self.jobs.items():
            if job["status"] == "queued" or (job["status"] == "leased" and job["lease_expiry"] <= now):
                job.update(status="leased", owner=worker, lease_expiry=now + self.lease_sec, attempts=job["attempts"] + 1)
                log.info("job=%s leased -> %s attempt=%d", jid, worker, job["attempts"])
                return jid
        return None

    def complete(self, job_id: str, worker: str) -> bool:
        job = self.jobs[job_id]
        if job["owner"] == worker:
            job["status"] = "done"
            log.info("job=%s completed by %s", job_id, worker)
            return True
        return False


async def main() -> None:
    sched = JobScheduler(lease_sec=0.1)
    for i in range(3):
        sched.enqueue(f"job-{i}")
    j = sched.lease("worker-1")        # worker-1 takes job-0 then "crashes"
    await asyncio.sleep(0.12)           # lease expires
    j2 = sched.lease("worker-2")        # worker-2 reclaims job-0
    log.info("reclaimed=%s (worker-1 never acked)", j2)
    sched.complete(j2, "worker-2")


if __name__ == "__main__":
    asyncio.run(main())
