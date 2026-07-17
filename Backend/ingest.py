import os
from Backend.exctractors import extract_file
from Backend.chunker import chunk_document
from Backend.vector_store import add_chunks

def run_ingestion(folder="docs"):
    if not os.path.exists(folder):
        print(f"Folder '{folder}' does not exist.")
        return

    for filename in os.listdir(folder):
        if not filename.endswith(".txt"):
            continue
        path = os.path.join(folder, filename)
        extracted = extract_file(path)
        chunks = chunk_document(extracted)
        add_chunks(chunks)
        print(f"Ingested {len(chunks)} chunks from {filename}")

    print("Done. Vector DB ready at ./chroma_db")

if __name__ == "__main__":
    run_ingestion()
