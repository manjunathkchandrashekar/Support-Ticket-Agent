from src.retrieval.retriever import Retriever


class RAGAgent:
    def __init__(self, retriever: Retriever):
        self.retriever = retriever

    def retrieve(self, ticket):
        query = f"{ticket.subject} {ticket.message}"
        return self.retriever.retrieve(query)
