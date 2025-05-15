import snowflake.connector
import uuid
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
    role=os.getenv("SNOWFLAKE_ROLE"),
)

cursor = conn.cursor()


def insert_chunk(filename: str, chunk_text: str, embedding: list[float]) -> None:
    chunk_id = str(uuid.uuid4())
    sql = """
        INSERT INTO CHUNKS (id, filename, chunk_text, embedding, created_at)
        SELECT %s, %s, %s, PARSE_JSON(%s), %s
    """
    cursor.execute(
        sql, (chunk_id, filename, chunk_text, json.dumps(embedding), datetime.utcnow())
    )
    conn.commit()


def insert_new_chat(chat_id: str) -> None:
    sql = """
        INSERT INTO MESSAGES (id, chat_id, created_at)
        VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (chat_id, chat_id, datetime.utcnow()))
    conn.commit()


def update_chat(chat_id: str, content: dict) -> None:
    sql = """
        UPDATE MESSAGES 
        SET content = %s, created_at = %s 
        WHERE id = %s
    """
    cursor.execute(sql, (json.dumps(content), datetime.utcnow(), chat_id))
    conn.commit()


def fetch_content(chat_id: str) -> list[dict]:
    sql = "SELECT content FROM MESSAGES WHERE id = %s"
    cursor.execute(sql, (chat_id,))
    row = cursor.fetchone()
    if row and row[0]:
        return json.loads(row[0])
    return []


def fetch_all_chunks() -> list[dict]:
    sql = "SELECT id, chunk_text, embedding FROM CHUNKS"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return [
        {"id": row[0], "chunk": row[1], "embedding": json.loads(row[2])} for row in rows
    ]


def fetch_all_chats() -> list[dict]:
    sql = "SELECT id, content FROM MESSAGES ORDER BY created_at DESC"
    cursor.execute(sql)
    rows = cursor.fetchall()

    chats = []
    for row in rows:
        chat_id, content_json = row
        content = json.loads(content_json) if content_json else []
        chats.append({"chat_id": chat_id, "content": content})

    return chats
