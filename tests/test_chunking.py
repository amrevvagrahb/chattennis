from src.ingest import chunk_pages

def make_page(text):
    return [{"source": "x.pdf", "page": 3, "text": text}]


def test_keeps_source_and_page():
    for c in chunk_pages(make_page("hello world " * 200)):
        assert c["source"] == "x.pdf" and c["page"] == 3


def test_chunk_size_limit():
    for c in chunk_pages(make_page("abcdefghij" * 300), size=800, overlap=100):
        assert len(c["text"]) <= 800


def test_overlap_between_chunks():
    text = "0123456789" * 200
    chunks = chunk_pages(make_page(text), size=800, overlap=100)
    assert chunks[0]["text"][-100:] == chunks[1]["text"][:100]


def test_short_page_is_one_chunk():
    assert len(chunk_pages(make_page("short text"))) == 1