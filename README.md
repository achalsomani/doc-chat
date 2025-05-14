# Retrieval-Augmented Generation (RAG) System

This repository contains a full-stack RAG application:

* **Backend:** FastAPI, OpenAI API, Snowflake  
* **Frontend:** React

Users can ingest text files, ask questions, and receive answers that are grounded in the uploaded documents. All chats and messages are stored permanently in Snowflake and can be revisited at any time.


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


## Frontend Routes

| Route            | Purpose                                   |
| ---------------- | ----------------------------------------- |
| `/`              | Home                                      |
| `/ingest`        | Upload and ingest a file                  |
| `/chat/new`      | Start a new chat                          |
| `/chat/:chatId`  | View or continue a specific chat          |
| `/history`       | Browse all past chats                     |


## Technology Stack

* OpenAI Embeddings model: `text-embedding-3-small`  
* OpenAI LLM: `gpt-4.1-mini`  
* Vector storage and chat persistence: Snowflake (`CHUNKS`, `MESSAGES` tables)  
* Similarity search: cosine similarity computed in Python  

**Local Setup**
#Snowflake: create the required tables

    ```sql 
    create or replace TABLE NERVE.PUBLIC.CHUNKS (
      ID VARCHAR(16777216) NOT NULL,
      FILENAME VARCHAR(16777216),
      CHUNK_TEXT VARCHAR(16777216),
      EMBEDDING VARIANT,
      CREATED_AT TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP(),
      primary key (ID)
    );
    create or replace TABLE NERVE.PUBLIC.MESSAGES (
      ID VARCHAR(16777216) NOT NULL,
      CHAT_ID VARCHAR(16777216),
      ROLE VARCHAR(16777216),
      CONTENT VARCHAR(16777216),
      CREATED_AT TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP(),
      primary key (ID)
    );
    ```

#Install backend dependencies
#pip install -r requirements.txt
#Create an .env file (inside the backend/ folder) and add:
  
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

#Run the backend: cd backend && python main.py
#Run the frontend: cd nerve-frontend && npm install && npm run dev

**Typical Flow**
Visit /ingest, upload a .txt file.
Go to /chat/new, enter a question.
Backend embeds the query, retrieves the most relevant chunks, and sends them to GPT-4.1-mini.
The Q-A pair is stored under the same chat_id.
Browse or continue any conversation from /history.