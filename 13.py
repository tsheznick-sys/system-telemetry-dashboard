import asyncio
import logging
import random
import time
from typing import Dict, List, Any
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s [SWARM_CORE] %(message)s")

class SwarmMemory:
    def __init__(self):
        self.shared_kb: Dict[str, Any] = {}
        self.lock = asyncio.Lock()

    async def update(self, key: str, value: Any):
        async with self.lock:
            self.shared_kb[key] = value
            logging.info(f"[MEMORY SYNC] Key '{key}' updated across swarm.")

    async def read(self, key: str) -> Any:
        async with self.lock:
            return self.shared_kb.get(key)

class AgentNode:
    def __init__(self, agent_id: str, specialty: str, memory: SwarmMemory):
        self.agent_id = agent_id
        self.specialty = specialty
        self.memory = memory

    async def execute_task(self, task_id: str, objective: str):
        logging.info(f"[{self.agent_id}] ({self.specialty}) Starting task {task_id}: '{objective}'")
        await asyncio.sleep(random.uniform(1.0, 2.5))
        
        simulated_output = {
            "agent": self.agent_id,
            "domain": self.specialty,
            "status": "SUCCESS",
            "confidence": round(random.uniform(0.85, 0.99), 4),
            "metrics": np.random.randn(5).tolist()
        }
        
        await self.memory.update(f"task_result_{task_id}", simulated_output)
        logging.info(f"[{self.agent_id}] Task {task_id} completed and published to shared memory.")

async def main_swarm():
    memory = SwarmMemory()
    agents = [
        AgentNode("AGENT_ALPHA", "Macro Data Synthesis", memory),
        AgentNode("AGENT_BETA", "Algorithmic Risk Modeling", memory),
        AgentNode("AGENT_GAMMA", "Execution Routing", memory)
    ]

    tasks = [
        agents[0].execute_task("TK_101", "Analyze liquidity depth across regional nodes"),
        agents[1].execute_task("TK_102", "Calculate Value-at-Risk (VaR) thresholds"),
        agents[2].execute_task("TK_103", "Simulate optimal order routing paths")
    ]

    await asyncio.gather(*tasks)
    final_kb = await memory.read("task_result_TK_101")
    logging.info(f"Swarm execution complete. Sample KB state: {final_kb}")

if __name__ == "__main__":
    asyncio.run(main_swarm())
    