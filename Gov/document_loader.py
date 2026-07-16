import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader

ocs_path = "./docs"
chroma_path = "./db/chroma_db"
def load_my_documents(docs_path="docs"):
    print(f"loading documents from {docs_path}...")

    if not os.path.exists(docs_path):
          raise FileNotFoundError(f"the directory {docs_path} does not exist. please create the directory and add your text files to it.")

    loader = DirectoryLoader(
       path = docs_path,
       glob="*.txt",
       loader_cls=TextLoader
)

    documents = loader.load()

    if len(documents)==0:
       raise FileNotFoundError(f"No.txt files found in the directory: {docs_path}.please add you text files to the directory and try again.")

    for i, doc in enumerate(documents[:2]):
       print(f"\nDocument {i+1}:")
       print(f"Source: {doc.metadata['source']}")
       print(f" content length: {len(doc.page_content)}characters")
       print(f" content preview: {doc.page_content[:100]}...")
       print(f" metadata: {doc.metadata}")

    return documents