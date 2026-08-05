import os
from llm_api_provider import embed_text

_chroma_client = None
_collection = None

def get_collection():
    global _chroma_client, _collection
    if _collection is not None:
        return _collection
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.abspath(os.path.join(current_dir, "..", "data", "chroma_db"))
    if not os.path.exists(db_path):
        return None
    import chromadb
    _chroma_client = chromadb.PersistentClient(path=db_path)
    _collection = _chroma_client.get_or_create_collection(name="gov_schemes", embedding_function=None)
    return _collection

def add_chunks(chunks: list[dict]):
    """
    Embeds and stores a list of chunk dicts (from chunk_document())
    into ChromaDB.
    """
    col = get_collection()
    if col is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.abspath(os.path.join(current_dir, "..", "data", "chroma_db"))
        os.makedirs(db_path, exist_ok=True)
        import chromadb
        global _chroma_client, _collection
        _chroma_client = chromadb.PersistentClient(path=db_path)
        _collection = _chroma_client.get_or_create_collection(name="gov_schemes", embedding_function=None)
        col = _collection

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

    col.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

def has_chunks() -> bool:
    try:
        col = get_collection()
        if col is None:
            return False
        return col.count() > 0
    except Exception:
        return False

def search(query: str, n_results: int = 5, filter_document_type: str = None):
    """
    Embeds the query and finds the closest matching chunks.
    Optionally filter by document_type.
    """
    col = get_collection()
    if col is None or not has_chunks():
        return []

    query_embedding = embed_text(query)

    where_filter = {"document_type": filter_document_type} if filter_document_type else None

    results = col.query(
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
