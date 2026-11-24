from src.ingest import CHROMA_DIR, COLLECTION, embed
from openai import OpenAI
import chromadb

_client = OpenAI()
_col = chromadb.PersistentClient(path=str(CHROMA_DIR)).get_collection(COLLECTION)


def doc_search_tool(query: str, n: int = 4, max_distance: float = 0.6) -> dict:
    if not query.strip():
        return {"status": "invalid", "message": "Empty query."}

    vec = embed([query], _client)[0]
    res = _col.query(query_embeddings=[vec], n_results=n)

    passages = []
    for text, meta, dist in zip(
        res["documents"][0], res["metadatas"][0], res["distances"][0]
    ):
        if dist <= max_distance:
            passages.append({
                "text": text,
                "source": meta["source"],
                "page": meta["page"],
                "distance": round(dist, 3),
            })

    if not passages:
        return {
            "status": "no_results",
            "message": "Nothing relevant found in the documents.",
        }
    return {'status':'ok', 'passages': passages}