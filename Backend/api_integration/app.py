import os
import sys
import json
import shutil
from datetime import datetime, timezone
from typing import List, Optional, Any
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv


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

app = FastAPI(
    title="GovSchemesHub API",
    description="FastAPI Backend for Government Schemes RAG and Assistance",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure upload directory
UPLOAD_FOLDER = os.path.abspath(os.path.join(current_dir, "..", "data", "uploads"))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.docx', '.xlsx', '.xls', '.csv'}


class QueryRequest(BaseModel):
    question: str
    history: Optional[List[dict]] = []


# Health check routes
@app.get("/")
@app.head("/")
@app.get("/health")
@app.head("/health")
@app.get("/api/health")
@app.head("/api/health")
async def health_check():
    return {
        "success": True,
        "status": "online",
        "message": "Server is healthy 🚀",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# Test API
@app.get("/api/test")
async def test():
    return {"message": "API working!"}

# Query RAG API (Streaming SSE)
@app.post("/api/query")
async def query_rag(payload: QueryRequest):
    question = payload.question
    history = payload.history or []
    
    if not question or not question.strip():
        raise HTTPException(status_code=400, detail="Missing or empty 'question' in request body")
        
    async def sse_generator():
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

    return StreamingResponse(
        sse_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )

# Query RAG API (JSON payload fallback)
@app.post("/api/query_json")
async def query_rag_json(payload: QueryRequest):
    question = payload.question
    history = payload.history or []
    
    if not question or not question.strip():
        raise HTTPException(status_code=400, detail="Missing or empty 'question' in request body")
        
    try:
        sources = []
        answer_text = ""
        for event_data in ask_with_rag_stream(question, history=history):
            if "error" in event_data:
                raise HTTPException(status_code=500, detail=event_data["error"])
            elif "sources" in event_data:
                sources = event_data["sources"]
            elif "text" in event_data:
                answer_text += event_data["text"]
                
        return {
            "answer": answer_text,
            "sources": sources
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Upload Document API
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    if not filename:
        raise HTTPException(status_code=400, detail="No file selected")
        
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    temp_path = os.path.join(UPLOAD_FOLDER, filename)
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        extracted = extract_file(temp_path)
        chunks = chunk_document(extracted)
        add_chunks(chunks)
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return {
            "message": f"Successfully ingested {len(chunks)} chunks",
            "filename": filename,
            "chunks_count": len(chunks)
        }
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Failed to ingest file: {str(e)}")

# Schemes API
@app.get("/api/schemes")
async def schemes():
    return {
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
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)

