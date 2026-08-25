class CustomerThreadStore:
    def __init__(self):
        self.threads = {}

    def append(self, customer_id: str, ticket_id: str, decision) -> None:
        self.threads.setdefault(customer_id, []).append((ticket_id, decision))

    def get(self, customer_id: str):
        return self.threads.get(customer_id, [])
