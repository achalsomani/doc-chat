from fastapi import FastAPI
import uuid
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from chunking import split_text_into_chunks

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Or ["*"] during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat/new")
def creatChat():
    chat_id = str(uuid.uuid4())
    return {"chat_id": chat_id}

@app.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    content = (await file.read()).decode('utf-8', errors='ignore')
    chunks = split_text_into_chunks(content, max_tokens=300, overlap_tokens=50)

    return {"success": True, "chunks_created": len(chunks)}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)

