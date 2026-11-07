import heapq
import logging
from typing import Dict, List, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s [GRAPH_DB] %(message)s")

class GraphDatabase:
    def __init__(self):
        self.adjacency_list: Dict[str, List[Tuple[str, float]]] = {}

    def add_edge(self, u: str, v: str, weight: float):
        if u not in self.adjacency_list:
            self.adjacency_list[u] = []
        if v not in self.adjacency_list:
            self.adjacency_list[v] = []
        self.adjacency_list[u].append((v, weight))
        self.adjacency_list[v].append((u, weight)) # Undirected graph

    def shortest_path(self, start: str, target: str) -> Tuple[float, List[str]]:
        pq = [(0.0, start, [start])]
        visited = set()

        while pq:
            cost, current, path = heapq.heappop(pq)

            if current == target:
                return cost, path

            if current in visited:
                continue
            visited.add(current)

            for neighbor, weight in self.adjacency_list.get(current, []):
                if neighbor not in visited:
                    heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))

        return float("inf"), []

if __name__ == "__main__":
    db = GraphDatabase()
    db.add_edge("Nairobi", "Mombasa", 485.0)
    db.add_edge("Nairobi", "Nakuru", 160.0)
    db.add_edge("Nakuru", "Kisumu", 200.0)
    db.add_edge("Mombasa", "Kisumu", 700.0)
    db.add_edge("Nairobi", "Eldoret", 310.0)
    db.add_edge("Eldoret", "Kisumu", 120.0)

    cost, path = db.shortest_path("Nairobi", "Kisumu")
    logging.info(f"Shortest path from Nairobi to Kisumu: {' -> '.join(path)} (Total Distance: {cost} km)")
    