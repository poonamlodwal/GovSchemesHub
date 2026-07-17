# GovSchemeHub

GovSchemeHub is a web-based platform that helps users explore and understand various government schemes in one place. It simplifies access to scheme-related information for users.

## 🔗 Live Demo

[Live Demo](https://schemehub-a.netlify.app?utm_source=chatgpt.com)

## 🚀 Features
🔍 Search government schemes easily
🤖 AI-powered answers using LLM
📄 Document-based retrieval system
⚡ Fast and relevant responses using vector database
🧠 Context-aware responses using RAG pipeline

## 🛠️ Tech Stack

* HTML
* CSS
* JavaScript
* Python
* LangChain
* Vector Database (FAISS / Chroma)acj
* OpenAI / LLM APIs
* Document Loaders & Text Chunking

## 📂 Project Structure

```
GovSchemesHub/ 
|──Frontend/
|    │── index.html
│    |── css/
│    |── js/
│    |── assets/
|── Backend/
|    │── python_main.py             # Main entry point
|    │── document_loader.py         # Loads scheme      documents
|    │── chunks.py                  # Text chunking logic
|    │── vectorDB.py                # Vector database      setup
|    │── retriever.py               # Retrieval logic
|    │── llm_chain.py               # LLM pipeline (RAG)
|    │── .env                       # Environment variables      
|── .gitignore                      # Ignored files
|── README.md

    ```

    
## ⚙️ Installation & Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/poonamlodwal/GovSchemesHub.git
   ```

2. Open the project folder:

   ```bash
   cd GovSchemeHub
   ```

3. Run the project:

   * Open `index.html` in your browser

## 🧠 How It Works

1. Documents are loaded using `document_loader.py`
2. Text is split into chunks
3. Chunks are converted into embeddings
4. Stored in a vector database
5. User query is matched with relevant chunks
6. LLM generates a final answer using context

---


## 📌 Usage

* Open the website using the Live Demo link or locally
* Browse available government schemes
* View details for each scheme


## 📄 License

This project is open source and available under the MIT License.

