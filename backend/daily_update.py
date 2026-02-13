import os
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import cohere
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
import numpy as np

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("daily_update.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load Env
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    logger.error("❌ COHERE_API_KEY not found.")
    exit(1)

co = cohere.Client(COHERE_API_KEY)

# Config
RSS_URL = "https://news.google.com/rss/search?q=Telangana+News+Telugu&hl=te&gl=IN&ceid=IN:te"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CHUNKS_DIR = os.path.join(DATA_DIR, "chunks")
os.makedirs(CHUNKS_DIR, exist_ok=True)

def fetch_rss():
    logger.info(f"📡 Fetching RSS Feed: {RSS_URL}")
    try:
        response = requests.get(RSS_URL, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception as e:
        logger.error(f"❌ Failed to fetch RSS: {e}")
        return None

def parse_rss(xml_content):
    root = ET.fromstring(xml_content)
    articles = []
    seen_urls = set()
    
    # Load existing URLs to avoid duplicates (Optimization: Check recent chunks only?)
    # For now, just rely on RSS being recent.
    
    for item in root.findall(".//item"):
        title = item.find("title").text
        link = item.find("link").text
        pubDate = item.find("pubDate").text
        
        # Simple ID
        if link in seen_urls: continue
        seen_urls.add(link)
        
        # Clean title
        if " - " in title: # Remove source name usually at end
            title = title.rsplit(" - ", 1)[0]
            
        articles.append({
            "chunk": title, # Using Title as Chunk for simple news
            "url": link,
            "date": pubDate
        })
    
    logger.info(f"📰 Found {len(articles)} articles.")
    return articles

def generate_embeddings(articles):
    if not articles: return []
    
    logger.info("🧠 Generating Embeddings...")
    texts = [a["chunk"] for a in articles]
    
    try:
        response = co.embed(
            texts=texts,
            model="embed-multilingual-v3.0",
            input_type="search_query"
        )
        embeddings = response.embeddings
        
        results = []
        for article, emb in zip(articles, embeddings):
            article["embedding"] = str(emb) # Store as string
            results.append(article)
            
        logger.info(f"✅ Generated {len(results)} embeddings.")
        return results
    except Exception as e:
        logger.error(f"❌ Embedding Generation Failed: {e}")
        return []

def save_chunk(data):
    if not data: return
    
    today = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"daily_update_{today}.csv"
    filepath = os.path.join(CHUNKS_DIR, filename)
    
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    logger.info(f"💾 Saved {len(df)} rows to {filepath}")

def main():
    logger.info("🚀 Starting Daily Update Pipeline...")
    xml = fetch_rss()
    if not xml: return
    
    articles = parse_rss(xml)
    if not articles: 
        logger.info("no new articles found.")
        return
        
    embeddings = generate_embeddings(articles)
    save_chunk(embeddings)
    logger.info("✅ Daily Update Complete.")

if __name__ == "__main__":
    main()
