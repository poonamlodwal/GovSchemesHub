import os
import sys
import json
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from werkzeug.utils import secure_filename


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

CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
    else:
        response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

@app.route('/api/<path:path>', methods=['OPTIONS'])
def options_handler(path):
    return '', 200

def allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS

# Home route
@app.route("/")
@app.route("/api/health")
def home():
    return jsonify({
        "status": "online",
        "message": "Backend service is running 🚀"
    }), 200

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

    res = Response(sse_generator(), mimetype="text/event-stream")
    res.headers["Cache-Control"] = "no-cache"
    res.headers["X-Accel-Buffering"] = "no"
    return res

# Query RAG API (JSON payload fallback)
@app.route("/api/query_json", methods=["POST"])
def query_rag_json():
    data = request.get_json(silent=True) or {}
    question = data.get("question")
    history = data.get("history", [])
    
    if not question or not question.strip():
        return jsonify({"error": "Missing or empty 'question' in request body"}), 400
        
    try:
        sources = []
        answer_text = ""
        for event_data in ask_with_rag_stream(question, history=history):
            if "error" in event_data:
                return jsonify({"error": event_data["error"]}), 500
            elif "sources" in event_data:
                sources = event_data["sources"]
            elif "text" in event_data:
                answer_text += event_data["text"]
                
        return jsonify({
            "answer": answer_text,
            "sources": sources
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
# Backend/api_integration/app.py
@app.route("/api/schemes", methods=["GET"])
def schemes():
    # Production me aap ise database se fetch kar sakte hain
    return jsonify({
        "status": "success",
        "schemes": [
            {
                "id": "pm-kisan",
                "title": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
                "category": "farmers",
                "benefits": "₹6,000 per year in three installments",
                "eligibility": ["Must be a landholding farmer family"],
                "officialLink": "https://pmkisan.gov.in"
            },
            {
                "id": "ayushman-bharat",
                "title": "Ayushman Bharat PM-JAY",
                "category": "healthcare",
                "benefits": "Health cover up to ₹5 lakh per family per year",
                "eligibility": ["Low income families based on SECC data"],
                "officialLink": "https://pmjay.gov.in"
            }
        ]
    }), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
