import re
from collections import Counter
from .chunking import Chunk


def _terms(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


class LexicalVectorStore:
    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        self.term_counts = [Counter(_terms(chunk.text)) for chunk in chunks]

    def search(self, query: str, limit: int = 3) -> list[tuple[Chunk, float]]:
        query_terms = {term for term in _terms(query) if len(term) > 3}
        if limit < 1 or not query_terms:
            return []
        scored = []
        for chunk, counts in zip(self.chunks, self.term_counts):
            overlap = sum(counts[term] for term in query_terms)
            score = overlap / len(query_terms)
            if score:
                scored.append((chunk, min(score, 1.0)))
        return sorted(scored, key=lambda item: item[1], reverse=True)[:limit]

    def search_many(self, queries, limit: int = 3) -> list[tuple[Chunk, float]]:
        best_scores = {}
        for query in queries:
            for chunk, score in self.search(query, limit):
                key = id(chunk)
                best_scores[key] = max(score, best_scores.get(key, 0.0))
        ranked = [
            (chunk, best_scores[id(chunk)])
            for chunk in self.chunks
            if id(chunk) in best_scores
        ]
        return sorted(ranked, key=lambda item: item[1], reverse=True)[:limit]
