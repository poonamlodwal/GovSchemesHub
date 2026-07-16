from langchain_text_splitters import RecursiveCharacterTextSplitter

#2. split the documents into chunks
def splits_documents(documents, chunks_size = 800, chunks_overlap=0):
    print(f"splitting documents into chunks...")
    text_splitter =RecursiveCharacterTextSplitter(
          chunk_size=chunks_size,
          chunk_overlap=chunks_overlap
        )

    chunks = text_splitter.split_documents(documents)

    if chunks:
        for i, chunk in enumerate(chunks[:5]):
                print(f"\n---- chunk{i+1}---")
                print(f"Sourece: {chunk.metadata['source']}")
                print(f"length: {len(chunk.page_content)} characters")
                print(f"Content:")
                print(chunk.page_content)
                print("-"*40)
        if len(chunks) >5:
            print(f"\n...{len(chunks)-5} more chunks")
    return chunks