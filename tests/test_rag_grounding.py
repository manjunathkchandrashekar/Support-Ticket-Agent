import pytest

from src.retrieval.chunking import chunk_text
from src.retrieval.retriever import Retriever
from src.retrieval.vector_store import LexicalVectorStore


def test_refund_retrieval_is_grounded():
    store = LexicalVectorStore(chunk_text('duplicate charges can be refunded', 'refund_policy.md'))
    results = store.search('duplicate charge refund')
    assert results and results[0][0].source == 'refund_policy.md'


def test_chunking_preserves_all_words_and_adds_overlap():
    chunks = chunk_text("one two three four five six seven", "faq.md", max_words=4, overlap=1)

    assert [chunk.text for chunk in chunks] == [
        "one two three four",
        "four five six seven",
    ]
    assert chunks[0].start_word == 0
    assert chunks[1].start_word == 3
    assert chunks[-1].end_word == 7


def test_chunking_rejects_invalid_sizes():
    with pytest.raises(ValueError):
        chunk_text("content", "faq.md", max_words=0)
    with pytest.raises(ValueError):
        chunk_text("content", "faq.md", max_words=4, overlap=4)


def test_long_user_input_is_searched_in_multiple_windows():
    chunks = chunk_text("duplicate charges are refundable", "refund.md")
    store = LexicalVectorStore(chunks)
    retriever = Retriever(store)
    query = "unrelated words " * 45 + "duplicate charges refundable"

    results = retriever.retrieve(query, limit=1, query_chunk_size=20)

    assert results and results[0][0].source == "refund.md"
