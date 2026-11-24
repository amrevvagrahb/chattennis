import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

load_dotenv()

DOCS_DIR = Path(__file__).resolve().parents[1] / "docs"
CHROMA_DIR = Path(__file__).resolve().parents[1] / "chroma_db"
COLLECTION = "tennis_docs"
EMBED_MODEL = "text-embedding-3-small"


def load_pages(docs_dir: Path = DOCS_DIR) -> list[dict]:
    pages = []
    for pdf in sorted(docs_dir.glob("*.pdf")):
        reader = PdfReader(pdf)
        for i, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()
            if text:
                pages.append({"source": pdf.name, "page": i, "text": text})
    return pages


def chunk_pages(pages: list[dict], size: int = 800, overlap: int = 100) -> list[dict]:
    chunks = []
    step = size - overlap
    for p in pages:
        text = p["text"]
        start = 0
        while start < len(text):
            piece = text[start:start + size].strip()
            if piece:
                chunks.append({
                    "source": p["source"],
                    "page": p["page"],
                    "text": piece,
                })
            if start + size >= len(text):
                break
            start += step
    return chunks


def embed(texts: list[str], client: OpenAI) -> list[list[float]]:
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]


def build_index() -> int:
    chunks = chunk_pages(load_pages())
    client = OpenAI()
    db = chromadb.PersistentClient(path=str(CHROMA_DIR))

    try:
        db.delete_collection(COLLECTION)  # clean rebuild each run
    except Exception:
        pass
    col = db.create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})

    batch = 50
    for i in range(0, len(chunks), batch):
        part = chunks[i:i + batch]
        col.add(
            ids=[str(i + j) for j in range(len(part))],
            documents=[c["text"] for c in part],
            embeddings=embed([c["text"] for c in part], client),
            metadatas=[{"source": c["source"], "page": c["page"]} for c in part],
        )
    return len(chunks)


if __name__ == "__main__":
    print("indexed", build_index(), "chunks")