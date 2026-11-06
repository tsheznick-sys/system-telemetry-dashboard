import heapq
import logging
from dataclasses import dataclass, field
from typing import List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [ORDER_BOOK] %(message)s")

@dataclass(order=True)
class Order:
    price: float
    order_id: str = field(compare=False)
    size: float = field(compare=False)
    side: str = field(compare=False)

class MatchingEngine:
    def __init__(self):
        self.buy_book = [] # Max heap simulated via negative prices
        self.sell_book = [] # Min heap

    def process_order(self, order_id: str, side: str, price: float, size: float):
        logging.info(f"Received Order [{order_id}] {side} {size} units @ ${price:,.2f}")
        
        if side == "BUY":
            # Match against sell book
            while self.sell_book and size > 0 and price >= self.sell_book[0].price:
                best_sell = self.sell_book[0]
                matched_size = min(size, best_sell.size)
                logging.info(f"⚡ MATCHED! BUY [{order_id}] with SELL [{best_sell.order_id}] -> {matched_size} units @ ${best_sell.price:,.2f}")
                size -= matched_size
                best_sell.size -= matched_size
                if best_sell.size <= 0:
                    heapq.heappop(self.sell_book)
            if size > 0:
                heapq.heappush(self.buy_book, Order(-price, order_id, size, side))
                
        elif side == "SELL":
            # Match against buy book (stored with negative prices)
            while self.buy_book and size > 0 and price <= -self.buy_book[0].price:
                best_buy = self.buy_book[0]
                matched_size = min(size, best_buy.size)
                logging.info(f"⚡ MATCHED! SELL [{order_id}] with BUY [{best_buy.order_id}] -> {matched_size} units @ ${-best_buy.price:,.2f}")
                size -= matched_size
                best_buy.size -= matched_size
                if best_buy.size <= 0:
                    heapq.heappop(self.buy_book)
            if size > 0:
                heapq.heappush(self.sell_book, Order(price, order_id, size, side))

if __name__ == "__main__":
    engine = MatchingEngine()
    engine.process_order("ORD_001", "SELL", 67500.0, 1.5)
    engine.process_order("ORD_002", "SELL", 67450.0, 2.0)
    engine.process_order("ORD_003", "BUY", 67460.0, 3.0)
    engine.process_order("ORD_004", "BUY", 67505.0, 1.0)
    