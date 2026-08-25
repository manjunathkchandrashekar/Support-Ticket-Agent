from pathlib import Path
from .chunking import Chunk, chunk_text


def load_documents(directory: str | Path) -> list[Chunk]:
    chunks = []
    for path in sorted(Path(directory).glob("*.md")):
        chunks.extend(chunk_text(path.read_text(encoding="utf-8"), path.name))
    return chunks
    