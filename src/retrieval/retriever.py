from .vector_store import LexicalVectorStore
from .chunking import chunk_text


class Retriever:
    def __init__(self, store: LexicalVectorStore):
        self.store = store

    def retrieve(self, query: str, limit: int = 3, query_chunk_size: int = 80):
        if not isinstance(query, str) or not query.strip():
            return []
        if limit < 1:
            return []
        query_chunks = chunk_text(query, "query", query_chunk_size, overlap=10)
        return self.store.search_many((chunk.text for chunk in query_chunks), limit)
