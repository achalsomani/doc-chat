# RAG demo

This repository contains a full stack RAG application:

* **Backend:** FastAPI, OpenAI API, Snowflake  
* **Frontend:** React

Users can ingest text files, ask questions, and receive answers that are grounded in the uploaded documents. All chats are stored in Snowflake.


## Features

* File ingestion  
* chunking  
* Embedding generation with the OpenAI Embeddings API  
* Cosine-similarity retrieval of the top-k relevant chunks  
* Answer generation with GPT-4.1-mini  
* Persistent chat history in Snowflake  


## API Endpoints

| Method | Path                | Description                                         |
| ------ | ------------------- | --------------------------------------------------- |
| POST   | `/ingest`           | Upload a `.txt`, split, embed, and store            |
| POST   | `/chat/new`         | Create a chat and return `chat_id`                  |
| POST   | `/message`          | Send `{chat_id, input}` and receive the AI answer   |
| GET    | `/chat/{chat_id}`   | Retrieve all messages for one chat                  |
| GET    | `/history`          | List every chat with its first question preview     |


## Frontend routes

| Route            | Purpose                                   |
| ---------------- | ----------------------------------------- |
| `/`              | Home                                      |
| `/ingest`        | Upload and ingest a file                  |
| `/chat/new`      | Start a new chat                          |
| `/chat/:chatId`  | View or continue a specific chat          |
| `/history`       | Browse all past chats                     |


## Tech stack

* OpenAI Embeddings model: `text-embedding-3-small`  
* OpenAI LLM: `gpt-4.1-mini`  
* Vector storage and chat persistence: Snowflake (`CHUNKS`, `MESSAGES` tables)  
* Similarity search: cosine similarity computed in Python  
## Local Setup

### 1. Create tables on Snowflake

```sql
CREATE OR REPLACE TABLE NERVE.PUBLIC.CHUNKS (
  ID VARCHAR(16777216) NOT NULL,
  FILENAME VARCHAR(16777216),
  CHUNK_TEXT VARCHAR(16777216),
  EMBEDDING VARIANT,
  CREATED_AT TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (ID)
);

CREATE OR REPLACE TABLE NERVE.PUBLIC.MESSAGES (
  ID VARCHAR(16777216) NOT NULL,
  CHAT_ID VARCHAR(16777216),
  ROLE VARCHAR(16777216),
  CONTENT VARCHAR(16777216),
  CREATED_AT TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (ID)
);
```

### 2. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 3. Create an `.env` file (Inside the `backend/` folder)

```env
OPENAI_API_KEY=your_openai_key
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
SNOWFLAKE_ROLE=your_role
```

### 4. Run the application

**Backend:**

```bash
cd backend
python main.py
```

**Frontend:**

```bash
cd nerve-frontend
npm install
npm run dev
```

---

## Typical flow

1. Visit `/ingest` and upload a `.txt` file.  
2. Navigate to `/chat/new` and enter a question.  
3. The backend embeds the query, retrieves the most relevant chunks, and sends them to GPT-4.1-mini.  
4. The question-answer pair is stored under the same `chat_id`.  
5. Browse or continue any conversation from `/history`.  
