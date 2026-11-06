import asyncio
import random
import time
import logging
import json
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

# Configure professional distributed system logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [RAFT_CLUSTER] %(message)s",
    handlers=[
        logging.FileHandler("raft_consensus.log"),
        logging.StreamHandler()
    ]
)

class NodeState(Enum):
    FOLLOWER = "FOLLOWER"
    CANDIDATE = "CANDIDATE"
    LEADER = "LEADER"

@dataclass
class LogEntry:
    term: int
    index: int
    command: Dict[str, Any]

class RaftNode:
    """Represents an individual consensus node within a distributed Raft cluster."""
    def __init__(self, node_id: str, peer_ids: List[str]):
        self.node_id = node_id
        self.peer_ids = peer_ids
        
        # Persistent state on all servers
        self.current_term: int = 0
        self.voted_for: Optional[str] = None
        self.log: List[LogEntry] = []
        
        # Volatile state on all servers
        self.state: NodeState = NodeState.FOLLOWER
        self.commit_index: int = 0
        self.last_applied: int = 0
        
        # Volatile state on leaders
        self.next_index: Dict[str, int] = {peer: 1 for peer in peer_ids}
        self.match_index: Dict[str, int] = {peer: 0 for peer in peer_ids}
        
        # Election timer management
        self.election_timeout: float = random.uniform(1.5, 3.0)
        self.last_heartbeat: float = time.time()
        self.running: bool = False
        self.mailbox: asyncio.Queue = asyncio.Queue()

    async def start(self):
        """Starts the node's main event loop."""
        self.running = True
        logging.info(f"[{self.node_id}] Node online in state: {self.state.value}")
        
        while self.running:
            try:
                # Process incoming RPC messages with timeout to check election timers
                timeout = 0.1
                try:
                    message = await asyncio.wait_for(self.mailbox.get(), timeout=timeout)
                    await self.handle_rpc(message)
                except asyncio.TimeoutError:
                    pass
                
                # State machine checks
                current_time = time.time()
                if self.state == NodeState.LEADER:
                    # Leaders broadcast heartbeats periodically
                    if current_time - self.last_heartbeat >= 0.5:
                        await self.broadcast_heartbeat()
                        self.last_heartbeat = current_time
                else:
                    # Followers / Candidates check for election timeout
                    if current_time - self.last_heartbeat >= self.election_timeout:
                        logging.warning(f"[{self.node_id}] Election timeout expired! Transitioning to CANDIDATE.")
                        await self.start_election()
                        
            except Exception as e:
                logging.error(f"[{self.node_id}] Critical error in node loop: {e}")

    async def start_election(self):
        """Transitions node to candidate status and requests votes from peers."""
        self.state = NodeState.CANDIDATE
        self.current_term += 1
        self.voted_for = self.node_id
        self.election_timeout = random.uniform(1.5, 3.0)
        self.last_heartbeat = time.time()

        votes_received = 1  # self.node_id votes for itself
        logging.info(f"[{self.node_id}] Starting election for Term {self.current_term}")
        
        last_log_index = len(self.log)
        last_log_term = self.log[-1].term if last_log_index > 0 else 0
        
        vote_payload = {
            "type": "REQUEST_VOTE",
            "term": self.current_term,
            "candidate_id": self.node_id,
            "last_log_index": last_log_index,
            "last_log_term": last_log_term
        }
        
        # Broadcast vote request to peers (simulated via cluster orchestrator routing)
        for peer in self.peer_ids:
            granted = await ClusterNetworkRouter.send_rpc(peer, vote_payload)
            if granted and self.state == NodeState.CANDIDATE:
                votes_received += 1
                if votes_received > (len(self.peer_ids) + 1) // 2:
                    await self.transition_to_leader()
                    break

    async def transition_to_leader(self):
        """Assumes leadership responsibilities across the cluster."""
        self.state = NodeState.LEADER
        logging.info(f"👑 [{self.node_id}] WON ELECTION! Promoted to LEADER for Term {self.current_term}")
        
        for peer in self.peer_ids:
            self.next_index[peer] = len(self.log) + 1
            self.match_index[peer] = 0
            
        await self.broadcast_heartbeat()

    async def broadcast_heartbeat(self):
        """Dispatches empty AppendEntries RPCs to maintain authority."""
        last_log_index = len(self.log)
        prev_log_index = last_log_index - 1
        prev_log_term = self.log[prev_log_index].term if prev_log_index >= 0 else 0
        
        heartbeat_payload = {
            "type": "APPEND_ENTRIES",
            "term": self.current_term,
            "leader_id": self.node_id,
            "prev_log_index": prev_log_index,
            "prev_log_term": prev_log_term,
            "entries": [],
            "leader_commit": self.commit_index
        }
        
        for peer in self.peer_ids:
            asyncio.create_task(ClusterNetworkRouter.dispatch_to_peer(peer, heartbeat_payload))

    async def handle_rpc(self, message: Dict[str, Any]):
        """Decodes and responds to incoming consensus control messages."""
        msg_type = message.get("type")
        
        if msg_type == "REQUEST_VOTE":
            term = message["term"]
            candidate_id = message["candidate_id"]
            
            if term > self.current_term:
                self.current_term = term
                self.state = NodeState.FOLLOWER
                self.voted_for = None
                
            vote_granted = False
            if term == self.current_term and (self.voted_for is None or self.voted_for == candidate_id):
                self.voted_for = candidate_id
                vote_granted = True
                self.last_heartbeat = time.time()
                logging.info(f"[{self.node_id}] Voted for candidate {candidate_id} in term {term}")
                
            await ClusterNetworkRouter.reply_rpc(candidate_id, {"vote_granted": vote_granted, "term": self.current_term})
            
        elif msg_type == "APPEND_ENTRIES":
            term = message["term"]
            leader_id = message["leader_id"]
            
            if term >= self.current_term:
                self.current_term = term
                self.state = NodeState.FOLLOWER
                self.voted_for = leader_id
                self.last_heartbeat = time.time()


class ClusterNetworkRouter:
    """Centralized message broker routing network packets between isolated nodes."""
    _nodes: Dict[str, RaftNode] = {}

    @classmethod
    def register_node(cls, node: RaftNode):
        cls._nodes[node.node_id] = node

    @classmethod
    async def send_rpc(cls, recipient_id: str, payload: Dict[str, Any]) -> bool:
        """Sends a vote request and returns confirmation."""
        node = cls._nodes.get(recipient_id)
        if node and node.running:
            # Simulate slight network jitter
            await asyncio.sleep(random.uniform(0.01, 0.05))
            if payload["type"] == "REQUEST_VOTE":
                # Simulated vote response logic
                return payload["term"] >= node.current_term
        return False

    @classmethod
    async def reply_rpc(cls, recipient_id: str, payload: Dict[str, Any]) -> bool:
        """Delivers a response message back to a peer via its mailbox."""
        node = cls._nodes.get(recipient_id)
        if node and node.running:
            await asyncio.sleep(random.uniform(0.01, 0.05))
            await node.mailbox.put(payload)
            return True
        return False

    @classmethod
    async def dispatch_to_peer(cls, recipient_id: str, payload: Dict[str, Any]):
        """Dispatches background RPC messages to peer mailboxes."""
        node = cls._nodes.get(recipient_id)
        if node and node.running:
            await node.mailbox.put(payload)


async def main():
    print("=== INITIALIZING DISTRIBUTED RAFT CONSENSUS CLUSTER ===")
    
    node_ids = ["NODE_ALPHA", "NODE_BETA", "NODE_GAMMA", "NODE_DELTA", "NODE_EPSILON"]
    cluster_nodes = []
    
    # Instantiate nodes
    for n_id in node_ids:
        peers = [p for p in node_ids if p != n_id]
        node = RaftNode(n_id, peers)
        cluster_nodes.append(node)
        ClusterNetworkRouter.register_node(node)
        
    # Launch all nodes concurrently in background tasks
    node_tasks = [asyncio.create_task(node.start()) for node in cluster_nodes]
    
    # Let the cluster run through leader elections and heartbeats for 15 seconds
    await asyncio.sleep(15.0)
    
    # Graceful shutdown
    print("\n=== INITIATING CLUSTER SHUTDOWN ===")
    for node in cluster_nodes:
        node.running = False
        
    await asyncio.gather(*node_tasks, return_exceptions=True)
    print("=== CLUSTER SHUTDOWN COMPLETE ===")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCluster run manually terminated by operator.")
