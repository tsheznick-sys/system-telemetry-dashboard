import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [2PC_COORDINATOR] %(message)s")

class ParticipantNode:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.prepared = False

    async def vote_prepare(self, tx_id: str) -> bool:
        await asyncio.sleep(0.2)
        # Simulate vote failure condition
        self.prepared = random.random() > 0.2
        status = "VOTE_COMMIT" if self.prepared else "VOTE_ABORT"
        logging.info(f"[{self.node_id}] Transaction {tx_id} prepare phase -> {status}")
        return self.prepared

    async def commit(self, tx_id: str):
        await asyncio.sleep(0.1)
        logging.info(f"[{self.node_id}] Transaction {tx_id} COMMITTED successfully.")

    async def abort(self, tx_id: str):
        await asyncio.sleep(0.1)
        logging.info(f"[{self.node_id}] Transaction {tx_id} ABORTED & rolled back.")

class TransactionCoordinator:
    def __init__(self, participants: list):
        self.participants = participants

    async def execute_transaction(self, tx_id: str) -> bool:
        logging.info(f"=== Starting 2PC Distributed Transaction: {tx_id} ===")
        
        # Phase 1: Prepare
        prepare_tasks = [p.vote_prepare(tx_id) for p in self.participants]
        votes = await asyncio.gather(*prepare_tasks)

        if all(votes):
            logging.info(f"All participants voted COMMIT for {tx_id}. Proceeding to Phase 2 (Commit).")
            commit_tasks = [p.commit(tx_id) for p in self.participants]
            await asyncio.gather(*commit_tasks)
            return True
        else:
            logging.warning(f"One or more participants aborted for {tx_id}. Initiating Global Rollback.")
            abort_tasks = [p.abort(tx_id) for p in self.participants]
            await asyncio.gather(*abort_tasks)
            return False

async def main():
    participants = [ParticipantNode(f"SHARD_DB_{i}") for i in range(1, 4)]
    coordinator = TransactionCoordinator(participants)
    
    await coordinator.execute_transaction("TX_9901")

if __name__ == "__main__":
    asyncio.run(main())
    