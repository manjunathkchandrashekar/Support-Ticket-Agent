class ApprovalQueue:
    def __init__(self):
        self.items = []

    def add(self, decision):
        ticket_id = getattr(decision, "ticket_id", None)
        if ticket_id and any(getattr(item, "ticket_id", None) == ticket_id for item in self.items):
            raise ValueError(f"ticket {ticket_id!r} is already queued")
        self.items.append(decision)
        return decision

    def pending(self):
        return [item for item in self.items if getattr(item, "review_status", "pending") == "pending"]

    def get(self, ticket_id):
        for item in self.items:
            if getattr(item, "ticket_id", None) == ticket_id:
                return item
        return None

    def remove(self, ticket_id):
        item = self.get(ticket_id)
        if item is None:
            raise KeyError(f"ticket {ticket_id!r} is not queued")
        self.items.remove(item)
        return item
