import asyncio
import logging
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s [WS_HUB] %(message)s")

class WebSocketClient:
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.queue = asyncio.Queue()

    async def send(self, message: str):
        await self.queue.put(message)

class WebSocketHub:
    def __init__(self):
        self.rooms = {}

    def join_room(self, room: str, client: WebSocketClient):
        if room not in self.rooms:
            self.rooms[room] = []
        self.rooms[room].append(client)
        logging.info(f"Client {client.client_id} joined room '{room}'")

    async def broadcast(self, room: str, message: dict):
        if room in self.rooms:
            payload = json.dumps(message)
            for client in self.rooms[room]:
                await client.send(payload)
            logging.info(f"Broadcasted message to {len(self.rooms[room])} clients in room '{room}'")

async def client_listener(client: WebSocketClient):
    try:
        while True:
            msg = await asyncio.wait_for(client.queue.get(), timeout=2.0)
            logging.info(f"[{client.client_id}] Received WebSocket frame: {msg}")
    except asyncio.TimeoutError:
        logging.info(f"[{client.client_id}] Connection session timed out gracefully.")

async def main():
    hub = WebSocketHub()
    c1 = WebSocketClient("CLIENT_01")
    c2 = WebSocketClient("CLIENT_02")

    hub.join_room("telemetry_stream", c1)
    hub.join_room("telemetry_stream", c2)

    listener_tasks = [
        asyncio.create_task(client_listener(c1)),
        asyncio.create_task(client_listener(c2))
    ]

    await hub.broadcast("telemetry_stream", {"event": "metrics_update", "cpu": 45.2, "status": "OPTIMAL"})
    await asyncio.sleep(0.5)

    for t in listener_tasks:
        t.cancel()

if __name__ == "__main__":
    asyncio.run(main())
    