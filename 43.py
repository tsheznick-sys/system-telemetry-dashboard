import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [ACTOR_MODEL] %(message)s")

class Actor:
    def __init__(self, name: str):
        self.name = name
        self.mailbox = asyncio.Queue()
        self.running = True

    async def send(self, message: dict):
        await self.mailbox.put(message)

    async def start(self):
        logging.info(f"Actor [{self.name}] started mailbox listener.")
        while self.running:
            try:
                msg = await asyncio.wait_for(self.mailbox.get(), timeout=1.0)
                await self.process_message(msg)
                self.mailbox.task_done()
            except asyncio.TimeoutError:
                continue

    async def process_message(self, message: dict):
        logging.info(f"Actor [{self.name}] processed message: {message}")

class TelemetryActor(Actor):
    async def process_message(self, message: dict):
        await asyncio.sleep(0.2)
        logging.info(f"📊 Telemetry Actor recorded metric -> {message.get('metric')}: {message.get('value')}")

async def main():
    actor = TelemetryActor("TelemetryWorker")
    actor_task = asyncio.create_task(actor.start())

    await actor.send({"metric": "CPU_LOAD", "value": 45.2})
    await actor.send({"metric": "MEMORY_USAGE", "value": 78.9})
    await asyncio.sleep(0.8)

    actor.running = False
    await actor_task

if __name__ == "__main__":
    asyncio.run(main())
    