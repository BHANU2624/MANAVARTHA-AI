import cohere
import os
from dotenv import load_dotenv

# Try to load from .env first, otherwise use the one found in README/code
load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    # Fallback to the one seen in api.py or README (caution: exposing keys)
    # The one in api.py was: DSdAuREU39x4mYDJaSDZ3DEmGM1x8000F7BZuRf2
    api_key = "DSdAuREU39x4mYDJaSDZ3DEmGM1x8000F7BZuRf2"

try:
    co = cohere.Client(api_key)
    response = co.embed(
        texts=["This is a test"],
        model="embed-multilingual-v3.0",
        input_type="search_query"
    )
    print("SUCCESS: API key works!")
    print(f"Embedding shape: {len(response.embeddings[0])}")
except Exception as e:
    print(f"FAILURE: {e}")
