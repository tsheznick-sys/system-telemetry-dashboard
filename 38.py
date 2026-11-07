import logging
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [EVENT_SOURCING] %(message)s")

class DomainEvent:
    def __init__(self, event_type: str, aggregate_id: str, payload: dict):
        self.event_type = event_type
        self.aggregate_id = aggregate_id
        self.payload = payload

class EventStore:
    def __init__(self):
        self.events: List[DomainEvent] = []

    def append(self, event: DomainEvent):
        self.events.append(event)
        logging.info(f"Appended event: {event.event_type} for aggregate {event.aggregate_id}")

    def get_events(self, aggregate_id: str) -> List[DomainEvent]:
        return [e for e in self.events if e.aggregate_id == aggregate_id]

class AccountAggregate:
    def __init__(self, account_id: str, event_store: EventStore):
        self.account_id = account_id
        self.event_store = event_store
        self.balance = 0.0
        self.status = "CREATED"

    def apply_events(self):
        history = self.event_store.get_events(self.account_id)
        for event in history:
            if event.event_type == "FUNDS_DEPOSITED":
                self.balance += event.payload["amount"]
            elif event.event_type == "FUNDS_WITHDRAWN":
                self.balance -= event.payload["amount"]
        logging.info(f"Rehydrated state for account {self.account_id} -> Balance: ${self.balance:,.2f}")

    def deposit(self, amount: float):
        event = DomainEvent("FUNDS_DEPOSITED", self.account_id, {"amount": amount})
        self.event_store.append(event)
        self.balance += amount

if __name__ == "__main__":
    store = EventStore()
    account = AccountAggregate("ACC_9988", store)
    account.deposit(500.0)
    account.deposit(250.0)
    
    # Rehydrate state from event log
    new_instance = AccountAggregate("ACC_9988", store)
    new_instance.apply_events()

logging.info("Event Sourcing simulation completed.")    
