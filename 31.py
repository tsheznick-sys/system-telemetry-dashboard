import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [FSM_ENGINE] %(message)s")

class StateMachine:
    def __init__(self):
        self.state = "PENDING"
        self.transitions = {
            "PENDING": ["RUNNING", "CANCELLED"],
            "RUNNING": ["COMPLETED", "FAILED"],
            "COMPLETED": [],
            "FAILED": ["PENDING"],
            "CANCELLED": []
        }

    def transition(self, new_state: str):
        allowed_states = self.transitions.get(self.state, [])
        if new_state in allowed_states:
            logging.info(f"FSM Transition: {self.state} -> {new_state}")
            self.state = new_state
        else:
            raise ValueError(f"Invalid transition from '{self.state}' to '{new_state}'")

if __name__ == "__main__":
    fsm = StateMachine()
    fsm.transition("RUNNING")
    fsm.transition("COMPLETED")
    