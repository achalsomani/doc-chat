import openai
import os
import dotenv

dotenv.load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_embedding(text: str, model: str = "text-embedding-ada-002") -> list[float]:
    try:
        response = client.embeddings.create(model=model, input=[text])
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e.__class__.__name__} - {e}")
        return []
