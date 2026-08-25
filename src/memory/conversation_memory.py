from collections import defaultdict


class ConversationMemory:
    def __init__(self):
        self.messages = defaultdict(list)

    def add(self, customer_id: str, message: str) -> None:
        self.messages[customer_id].append(message)

    def get(self, customer_id: str) -> list[str]:
        return self.messages[customer_id]
