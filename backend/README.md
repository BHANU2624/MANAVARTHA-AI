# Telugu News AI - Backend

FastAPI backend for Telugu News AI RAG application using:
- **Cohere embed-multilingual-v3.0** for embeddings and retrieval
- **Gemini Flash 2.0** for query normalization and answer generation

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the `backend` directory:
   ```
   COHERE_API_KEY=DSdAuREU39x4mYDJaSDZ3DEmGM1x8000F7BZuRf2
   GEMINI_API_KEY=AIzaSyALIVRIoCOYGmoNWRkO4B2vRXK9pXYQaRU
   ```
   Get your API keys from:
   - Cohere: https://dashboard.cohere.com/api-keys
   - Gemini: https://aistudio.google.com/app/apikey

3. **Ensure data file exists:**
   Make sure `data/all_telugu_chunk_embeddings_clean.csv` exists with the required columns:
   - `embedding`: String representation of embedding vector
   - `chunk`: Text chunk content

## Running the Server

### Option 1: Using Batch File (Windows - Recommended)

**PowerShell:**
```powershell
.\start_server.bat
```

**CMD:**
```cmd
start_server.bat
```

### Option 2: Direct Python Execution (Windows - No activation needed)

**PowerShell:**
```powershell
.\venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**CMD:**
```cmd
venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: Using Batch Activation (Windows CMD)
```cmd
venv\Scripts\activate.bat
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Option 4: Using PowerShell Script (Windows - if execution policy allows)
```powershell
cd backend
.\start_server.ps1
```

### Option 5: Manual Start (Linux/Mac)
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Note:** If you encounter PowerShell execution policy errors, use Option 1, 2, or 3.

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## API Endpoints

- `GET /search?query=<your_query>` - Search for news articles
- `GET /health` - Check server health
- `GET /` - API information

## Example Request

```bash
curl "http://localhost:8000/search?query=తెలుగు%20న్యూస్"
```

