# server.py
import os, time
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import pipeline_api

ARTICLES_CSV = os.getenv("ARTICLES_CSV", "all_telugu_news_articles.csv")

app = FastAPI(title="Telugu News RAG Backend")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

job_state = {"running": False, "last_run": None, "last_result": None}

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

@app.get("/health")
def health():
    return {"status": "ok", "time": time.time()}

@app.post("/run-pipeline")
def run_pipeline(background_tasks: BackgroundTasks, max_depth: int = 1, max_pages_per_site: int = 10):
    if job_state["running"]:
        return {"status":"already_running"}
    def wrapper():
        try:
            job_state["running"] = True
            job_state["last_run"] = time.time()
            pipeline_api.pipeline_job(max_depth=max_depth, max_pages_per_site=max_pages_per_site)
            pipeline_api.rebuild_faiss_from_csv()
            job_state["last_result"] = {"ok": True, "time": time.time()}
        except Exception as e:
            job_state["last_result"] = {"ok": False, "error": str(e)}
        finally:
            job_state["running"] = False
    background_tasks.add_task(wrapper)
    return {"status":"started"}

@app.get("/pipeline-status")
def pipeline_status():
    return job_state

@app.post("/query")
def query(req: QueryRequest):
    if not req.query.strip():
        raise HTTPException(400, "Empty query")
    results = pipeline_api.query_faiss(req.query, top_k=req.top_k)
    return {"query": req.query, "results": results}

@app.get("/latest-articles")
def latest_articles(n: int = 20):
    if not os.path.exists(ARTICLES_CSV):
        return {"articles": []}
    df = pd.read_csv(ARTICLES_CSV, encoding="utf-8", engine="python")
    if "date" in df.columns:
        df_sorted = df.sort_values(by="date", ascending=False)
    else:
        df_sorted = df.iloc[::-1]
    return {"articles": df_sorted.head(n).to_dict(orient="records")}

@app.get("/article")
def article(url: str):
    if not os.path.exists(ARTICLES_CSV):
        raise HTTPException(404, "articles file not found")
    df = pd.read_csv(ARTICLES_CSV, encoding="utf-8", engine="python")
    match = df[df["url"].astype(str) == str(url)]
    if match.empty:
        raise HTTPException(404, "article not found")
    return match.iloc[0].to_dict()
