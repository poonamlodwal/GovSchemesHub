import os
# pyrefly: ignore [missing-import]
import chromadb
from llm_api_provider import embed_text

# Locate the database relative to this file's folder (Backend/data/chroma_db)
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.abspath(os.path.join(current_dir, "..", "data", "chroma_db"))

_chroma_client = chromadb.PersistentClient(path=db_path)
_collection = _chroma_client.get_or_create_collection(name="gov_schemes")

def add_chunks(chunks: list[dict]):
    """
    Embeds and stores a list of chunk dicts (from chunk_document())
    into ChromaDB.
    """
    ids = []
    texts = []
    metadatas = []
    embeddings = []

    for chunk in chunks:
        ids.append(chunk["chunk_id"])
        texts.append(chunk["text"])
        embeddings.append(embed_text(chunk["text"]))
        metadatas.append({
            "filename": chunk["filename"],
            "filetype": chunk["filetype"],
            "doc_type": chunk["doc_type"],
            "document_type": chunk["document_type"],
        })

    _collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

def has_chunks() -> bool:
    try:
        return _collection.count() > 0
    except Exception:
        return False

def search(query: str, n_results: int = 5, filter_document_type: str = None):
    """
    Embeds the query and finds the closest matching chunks.
    Optionally filter by document_type.
    """
    if not has_chunks():
        return []

    query_embedding = embed_text(query)

    where_filter = {"document_type": filter_document_type} if filter_document_type else None

    results = _collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=where_filter,
    )

    matches = []
    if results and results.get("ids") and len(results["ids"]) > 0:
        for i in range(len(results["ids"][0])):
            matches.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],  # lower = more similar
            })
    return matches
