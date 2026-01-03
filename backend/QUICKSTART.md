# Quick Start Guide

## Step 1: Create .env File

Create a file named `.env` in the `backend` directory with your API keys:

```
COHERE_API_KEY=DSdAuREU39x4mYDJaSDZ3DEmGM1x8000F7BZuRf2
GEMINI_API_KEY=AIzaSyALIVRIoCOYGmoNWRkO4B2vRXK9pXYQaRU
```

Get your API keys from:
- Cohere: https://dashboard.cohere.com/api-keys (for embeddings)
- Gemini: https://aistudio.google.com/app/apikey (for answer generation)

## Step 2: Start the Server

### Option 1: Using Batch File (Recommended for Windows - No PowerShell policy issues)

**If you're in PowerShell:**
```powershell
.\start_server.bat
```

**If you're in CMD:**
```cmd
start_server.bat
```

**If you're in the project root:**
```cmd
cd backend
.\start_server.bat    # PowerShell
# OR
start_server.bat      # CMD
```

### Option 2: Using Batch Activation (Windows CMD)
```cmd
venv\Scripts\activate.bat
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: Direct Python Execution (No activation needed - Works in both CMD and PowerShell)
```cmd
venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**In PowerShell:**
```powershell
.\venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Option 4: PowerShell (If execution policy allows)
```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Note:** If you get "running scripts is disabled" error in PowerShell, use Option 1, 2, or 3 instead.

## Step 3: Test the Server

Open your browser and go to:
- http://localhost:8000/docs (Interactive API documentation)
- http://localhost:8000/health (Health check)

## Step 4: Test a Query

Try this in your browser or using curl:
```
http://localhost:8000/search?query=తెలుగు%20న్యూస్
```

## Troubleshooting

1. **"running scripts is disabled" (PowerShell error)**
   - **Solution 1 (Easiest):** Use `start_server.bat` instead
   - **Solution 2:** Use `venv\Scripts\activate.bat` (batch file, not PowerShell)
   - **Solution 3:** Run directly: `venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000`
   - **Solution 4:** Change PowerShell policy (run as admin): `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

2. **"uvicorn is not recognized"**
   - Make sure you activated the virtual environment first
   - Or use: `venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000`

3. **"COHERE_API_KEY is not set"**
   - Create a `.env` file in the `backend` directory with your API key

4. **"CSV file not found"**
   - Make sure `data/all_telugu_chunk_embeddings_clean.csv` exists in the `backend` directory

5. **Port already in use**
   - Change the port: `uvicorn main:app --reload --host 0.0.0.0 --port 8001`

