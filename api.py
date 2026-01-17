from fastapi import FastAPI
from pydantic import BaseModel
import faiss
import numpy as np
import pandas as pd
import cohere
import google.generativeai as genai
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ---------- CONFIG ----------
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY not found in environment variables")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

FAISS_INDEX_FILE = "telugu_faiss_index.index"
METADATA_FILE = "all_telugu_faiss_metadata.csv"

# ---------- LOAD MODELS ----------
co = cohere.Client(COHERE_API_KEY)

genai.configure(api_key=GEMINI_API_KEY)
gem_model = genai.GenerativeModel("models/gemini-2.5-flash")

# ---------- LOAD FAISS ----------
# Note: This will fail if index file doesn't exist. Create proper data files first.
try:
    index = faiss.read_index(FAISS_INDEX_FILE)
    meta_df = pd.read_csv(METADATA_FILE)
except Exception as e:
    print(f"Warning: Could not load FAISS index or metadata: {e}")
    print("This is expected if you haven't generated the data files yet.")
    index = None
    meta_df = None

# ---------- HELPERS ----------
def embed(text):
    response = co.embed(
        texts=[text],
        model="embed-multilingual-v3.0",
        input_type="search_query"
    )
    return np.array(response.embeddings[0], dtype="float32").reshape(1, -1)


def answer_question(question):
    if index is None or meta_df is None:
        return "⚠️ Error: FAISS index or metadata not loaded. Please generate data files first."
    
    try:
        q_emb = embed(question)
        D, I = index.search(q_emb, k=20)
        print("i am here....")
        chunks = []
        for i in I[0]:
            if 0 <= i < len(meta_df):
                chunks.append(meta_df.iloc[i]["chunk"])

        context = "\n\n".join(chunks)

        prompt = f"""
        ప్రశ్న: {question}

        సంబంధిత వార్తలు:
        {context}

        పై సమాచారాన్ని ఆధారంగా, స్పష్టంగా మరియు వివరాలతో సమాధానం ఇవ్వండి.
        """

        # ------ SAFE GEMINI CALL -------
        try:
            gem_response = gem_model.generate_content(prompt)
            if not gem_response or not gem_response.text:
                raise Exception("Empty Gemini response")
            print("gemini response received ",gem_response.text)
            return gem_response.text.strip()

        except Exception as e:
            print(e)
            return f"⚠️ Gemini Error: {str(e)}"

    except Exception as e:
        print(e)
        return f"⚠️ Internal Error: {str(e)}"


# ---------- FASTAPI ----------
app = FastAPI(
    title="Telugu News Q&A API",
    description="RAG-based Telugu news question answering system",
    version="1.0.0"
)

# Add CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_api(payload: Query):
    try:
        answer = answer_question(payload.question)
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"⚠️ API Error: {str(e)}"}
