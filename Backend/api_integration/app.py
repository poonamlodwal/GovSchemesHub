import os
import sys
import json
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from werkzeug.utils import secure_filename
from flask import Flask
from flask_cors import CORS


current_dir = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from the root .env file or KIBO/.env fallback
dotenv_path = find_dotenv()
if not dotenv_path:
    kibo_dotenv = os.path.abspath(os.path.join(current_dir, "..", "KIBO", ".env"))
    if os.path.exists(kibo_dotenv):
        dotenv_path = kibo_dotenv
load_dotenv(dotenv_path)

# Add KIBO to python system path for importing modules from it
kibo_dir = os.path.abspath(os.path.join(current_dir, "..", "KIBO"))
if kibo_dir not in sys.path:
    sys.path.append(kibo_dir)

from rag import ask_with_rag, ask_with_rag_stream
from exctractors import extract_file
from chunker import chunk_document
from vector_store import add_chunks

app = Flask(__name__)

# Configure upload directory
UPLOAD_FOLDER = os.path.abspath(os.path.join(current_dir, "..", "data", "uploads"))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload file size
ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.docx', '.xlsx', '.xls', '.csv'}

allowed_origins = ["*"]
env_origins = os.getenv("CORS_ALLOWED_ORIGINS")
if env_origins:
    allowed_origins.extend([o.strip() for o in env_origins.split(",")])

CORS(app, resources={r"/api/*": {"origins": allowed_origins}}, supports_credentials=True)

def allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS

# Home route
@app.route("/")
def home():
    return "Backend is running 🚀"

# Test API
@app.route("/api/test")
def test():
    return jsonify({"message": "API working!"})

# Query RAG API (Streaming SSE)
@app.route("/api/query", methods=["POST"])
def query_rag():
    data = request.get_json(silent=True) or {}
    question = data.get("question")
    history = data.get("history", [])
    
    if not question or not question.strip():
        return jsonify({"error": "Missing or empty 'question' in request body"}), 400
        
    def sse_generator():
        try:
            for event_data in ask_with_rag_stream(question, history=history):
                if "error" in event_data:
                    yield f"event: error\ndata: {json.dumps({'error': event_data['error']})}\n\n"
                    break
                elif "sources" in event_data:
                    yield f"event: sources\ndata: {json.dumps(event_data['sources'])}\n\n"
                elif "text" in event_data:
                    yield f"event: content\ndata: {json.dumps({'text': event_data['text']})}\n\n"
            
            yield "event: end\ndata: {}\n\n"
        except Exception as e:
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"

    return Response(sse_generator(), mimetype="text/event-stream")

# Upload Document API
@app.route("/api/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_path)
        
        try:
            # Process and ingest document into ChromaDB
            extracted = extract_file(temp_path)
            chunks = chunk_document(extracted)
            add_chunks(chunks)
            
            # Clean up temporary uploaded file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
            return jsonify({
                "message": f"Successfully ingested {len(chunks)} chunks",
                "filename": filename,
                "chunks_count": len(chunks)
            }), 200
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return jsonify({"error": f"Failed to ingest file: {str(e)}"}), 500
            
    return jsonify({"error": f"Invalid file extension. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"}), 400

# Schemes API
@app.route("/api/schemes")
def schemes():
    return jsonify({
        "schemes": [
            {"name": "PM Kisan", "benefit": "₹6000/year"},
            {"name": "Ayushman Bharat", "benefit": "Health insurance"}
        ]
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
