# pipeline_api.py
import os
from typing import List, Dict, Any

# Replace these imports with your actual pipeline module name
# Example: from pipeline import pipeline_job as real_pipeline_job, query_top_k
# For now we call the functions via placeholders

def pipeline_job(max_depth=1, max_pages_per_site=10):
    # call your real pipeline entrypoint here
    import pipeline
    pipeline.pipeline_job(max_depth=max_depth, max_pages_per_site=max_pages_per_site)

def rebuild_faiss_from_csv():
    import pipeline
    pipeline.rebuild_faiss_from_csv()

def query_faiss(query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
    # Expected to return list of dicts: {"url":..., "title":..., "chunk":..., "score":...}
    import pipeline
    return pipeline.query_top_k(query_text, top_k)
