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
    role=os.getenv("SNOWFLAKE_ROLE")
)

cursor = conn.cursor()

def insert_chunk(filename: str, chunk_text: str, embedding: list[float]) -> None:
    chunk_id = str(uuid.uuid4())
    sql = """
        INSERT INTO CHUNKS (id, filename, chunk_text, embedding, created_at)
        SELECT %s, %s, %s, PARSE_JSON(%s), %s
    """
    cursor.execute(sql, (
        chunk_id,
        filename,
        chunk_text,
        json.dumps(embedding), 
        datetime.utcnow()
    ))
    conn.commit()
