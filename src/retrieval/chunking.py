from dataclasses import dataclass


@dataclass
class Chunk:
    source: str
    text: str
    index: int = 0
    start_word: int = 0
    end_word: int = 0


def chunk_text(text: str, source: str, max_words: int = 120, overlap: int = 20) -> list[Chunk]:
    if max_words < 1:
        raise ValueError("max_words must be greater than zero")
    if overlap < 0 or overlap >= max_words:
        raise ValueError("overlap must be at least zero and smaller than max_words")
    words = text.split()
    step = max_words - overlap
    chunks = []
    for index, start in enumerate(range(0, len(words), step)):
        end = min(start + max_words, len(words))
        chunks.append(Chunk(source, " ".join(words[start:end]), index, start, end))
        if end == len(words):
            break
    return chunks
