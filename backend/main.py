from fastapi import FastAPI, HTTPException
import uuid
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from chunking import split_text_into_chunks
from database import insert_chunk, fetch_all_chunks,update_chat, fetch_content, insert_new_chat,fetch_all_chats
from embedd import generate_embedding
from top_k import retrieve_top_chunks
import os
import json
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat/new")
async def create_chat() -> dict:
    try:
        chat_id = str(uuid.uuid4())
        insert_new_chat(chat_id)
        return {"chat_id": chat_id}
    except Exception as e:
        print(f"Create chat error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create chat.")


class MessageRequest(BaseModel):
    chat_id: str
    input: str

@app.post("/message")
async def handle_message(request: MessageRequest) -> dict:
    try:
        content = fetch_content(request.chat_id)
        query_embedding = generate_embedding(request.input)
        if not query_embedding:
            raise HTTPException(status_code=500, detail="Failed to generate embedding.")

        stored_chunks = fetch_all_chunks()
        top_chunks = retrieve_top_chunks(query_embedding, stored_chunks, top_k=2)
        print(f"Top chunks: {top_chunks}")
        context = "\n".join([item["chunk"] for item in top_chunks])
        print(f"Context: {context}")
        used_chunk_ids = [item["id"] for item in top_chunks]

        prompt = f"Context:\n{context}\n\nQuestion: {request.input}\nAnswer the question based on the context above. Please dont include any information that is not in the context. If you don't know the answer, say 'I don't know'. and dont include extra information."
        response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content

        content.append({"message_id": str(uuid.uuid4()), "user": request.input, "agent": answer})
        update_chat(request.chat_id, content)

        return {
            "chat_id": request.chat_id,
            "response": answer,
            "used_chunks": used_chunk_ids
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Message error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process message.")

@app.get("/history")
async def get_full_history() -> dict:
    try:
        chats = fetch_all_chats()
        return {"chats": chats}
    except Exception as e:
        print(f"History error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch history.")

@app.get("/chat/{chat_id}")
async def get_chat(chat_id: str) -> dict:
    try:
        content = fetch_content(chat_id)
        print(f"Content for chat {chat_id}: {content}")
        return {"chat_id": chat_id, "messages": content}
    except Exception as e:
        print(f"Get chat error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch chat.")

@app.post("/ingest")
async def ingest_file(file: UploadFile = File(...)) -> dict:
    try:
        content = (await file.read()).decode('utf-8', errors='ignore')
        chunks = split_text_into_chunks(content, max_tokens=300, overlap_tokens=50)

        for chunk in chunks:
            embedding = generate_embedding(chunk)
            insert_chunk(file.filename, chunk, embedding)

        return {"success": True, "chunks_created": len(chunks)}
    except Exception as e:
        print(f"Ingest error: {e}")
        raise HTTPException(status_code=500, detail="Failed to ingest file.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)

