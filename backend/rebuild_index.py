import os
import sys
import logging
import subprocess

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("rebuild_index.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Ensure backend directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rag_engine import TeluguNewsRAG

def rebuild_and_restart():
    logger.info("🚀 Starting Nightly Index Rebuild...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    chunks_dir = os.path.join(base_dir, "data", "chunks")
    
    # 1. Initialize RAG (Forces load of all chunks if index not found, or we can force rebuild)
    # Actually, we want to LOAD DATA anew, not load existing index.
    # So we should delete the old index meta check or instantiate cleanly.
    # To force rebuild, we can pass a non-existent index path or modify RAG to allow force rebuild.
    # But RAG init logic is: if index exists, load it.
    # We need to bypass this.
    
    # Simpler: Rename old index temporarily?
    # Or better: The RAG class doesn't have a "force_rebuild" flag in init.
    # But we can call `rag = TeluguNewsRAG(...)` which loads OLD index, then call `rag.reload_data()` which DOES rebuild from CSVs.
    # Let's check `reload_data` in rag_engine.py.
    
    try:
        # Load current state (fast)
        rag = TeluguNewsRAG(csv_path=chunks_dir)
        
        # Force Reload from all CSVs (Slow process - Nightly)
        logger.info("♻️  Forcing full data reload...")
        success = rag.reload_data()
        
        if success:
            # Save the new index
            logger.info("💾 Saving new index...")
            if rag.save_index():
                logger.info("✅ Index saved. Restarting Service...")
                # Restart Systemd Service
                subprocess.run(["sudo", "systemctl", "restart", "manavartha"], check=True)
                logger.info("✅ Service Restarted.")
            else:
                logger.error("❌ Failed to save index.")
        else:
            logger.error("❌ Data reload failed.")
            
    except Exception as e:
        logger.error(f"❌ Rebuild Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    rebuild_and_restart()
