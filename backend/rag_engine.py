"""
MANA VARTHA AI - Production-Grade RAG Engine
Multilingual Telugu News Question Answering System
"""

import os
import ast
import json
import logging
import re
from typing import List, Dict, Tuple, Optional
import pandas as pd
import numpy as np
import faiss
import pickle
import cohere
import google.generativeai as genai
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(encoding='utf-8-sig')  # Handle UTF-8 BOM on Windows

class TeluguNewsRAG:
    """
    Production-grade RAG engine for Telugu news with multilingual support.
    Handles Telugu, English, and Romanized Telugu queries.
    """
    
    def __init__(self, csv_path: str, embedding_dim: int = 1024):
        """
        Initialize RAG engine with embeddings and FAISS index.
        
        Args:
            csv_path: Path to CSV with chunk_text and embedding columns
            embedding_dim: Expected embedding dimension (default: 1024 for Cohere multilingual-v3)
        """
        self.csv_path = csv_path
        self.embedding_dim = embedding_dim
        self.similarity_threshold = 0.25  # Lower threshold to allow broader retrieval, strict gate later
        self.top_k = 15
        
        # Initialize Cohere client
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY not found in environment variables")
        self.cohere_client = cohere.Client(api_key)

        # Initialize Gemini client
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            logger.warning("⚠️ GOOGLE_API_KEY not found. Answer generation will fail.")
        else:
            # 1️⃣ Explicit Model Validation & Centralized Config
            available_models = [m.name for m in genai.list_models()]
            
            # Priority List: 2.5 Flash -> 1.5 Flash -> Pro
            preferred_models = [
                "models/gemini-2.5-flash", 
                "models/gemini-1.5-flash",
                "models/gemini-pro"
            ]
            
            selected_model = "models/gemini-1.5-flash" # Default fallback
            for model in preferred_models:
                if model in available_models:
                    selected_model = model
                    break
            
            logger.info(f"✅ Selected Primary Model: {selected_model}")
            self.gemini_model = genai.GenerativeModel(selected_model)
            self.model_name = selected_model
        
        # Load index
        self.index_path = os.path.join(os.path.dirname(csv_path), "faiss_prod.index") if csv_path else "faiss_prod.index"
        
        if os.path.exists(self.index_path) and os.path.exists(self.index_path + ".meta"):
            logger.info(f"🚀 Loading pre-built index from {self.index_path}...")
            self.chunks, self.embeddings, self.index = self._load_index_from_disk()
        else:
            logger.info("⚠️ Pre-built index not found. Building from scratch (This may take time)...")
            self.chunks, self.embeddings, self.index = self._load_and_build_index()
            
        logger.info(f"✅ RAG Engine initialized with {len(self.chunks)} chunks")
        
    def save_index(self, path: str = None):
        """Save FAISS index and metadata to disk."""
        if path is None: path = self.index_path
        
        logger.info(f"💾 Saving index to {path}...")
        try:
            # Save FAISS index
            faiss.write_index(self.index, path)
            
            # Save Metadata (chunks, embeddings)
            with open(path + ".meta", "wb") as f:
                pickle.dump({"chunks": self.chunks, "embeddings": self.embeddings}, f)
            
            logger.info("✅ Index saved successfully.")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to save index: {e}")
            return False

    def _load_index_from_disk(self):
        """Load FAISS index and metadata from disk."""
        try:
            index = faiss.read_index(self.index_path)
            with open(self.index_path + ".meta", "rb") as f:
                data = pickle.load(f)
            return data["chunks"], data["embeddings"], index
        except Exception as e:
            logger.error(f"❌ Failed to load index from disk: {e}")
            raise e
    
    def reload_data(self):
        """Reload data from CSV and rebuild index."""
        logger.info("♻️ Reloading data and rebuilding index...")
        try:
            self.chunks, self.embeddings, self.index = self._load_and_build_index()
            logger.info(f"✅ Data reloaded successfully. Total chunks: {len(self.chunks)}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to reload data: {e}")
            return False
    
    def _load_and_build_index(self) -> Tuple[List[str], np.ndarray, faiss.IndexFlatIP]:
        """
        Load CSV(s) in chunks, parse embeddings, and build FAISS index.
        Supports single file or directory of CSVs.
        """
        valid_chunks: List[str] = []
        valid_embeddings: List[np.ndarray] = []

        # Determine file list
        files_to_load = []
        if os.path.isdir(self.csv_path):
            logger.info(f"📂 Loading data from directory: {self.csv_path}")
            files_to_load = [os.path.join(self.csv_path, f) for f in os.listdir(self.csv_path) if f.endswith('.csv')]
            files_to_load.sort() # Ensure consistent order
        elif os.path.exists(self.csv_path):
            logger.info(f"📂 Loading data from file: {self.csv_path}")
            files_to_load = [self.csv_path]
        else:
            raise FileNotFoundError(f"Data path not found: {self.csv_path}")

        if not files_to_load:
             raise ValueError(f"No CSV files found in {self.csv_path}")

        logger.info(f"📚 Found {len(files_to_load)} files to process.")

        text_col = None
        embedding_format = None

        # Iterate over all files
        for file_path in files_to_load:
            logger.info(f"🔹 Processing {os.path.basename(file_path)}...")
            
            # Detect schema from first file
            if text_col is None:
                first_chunk = pd.read_csv(file_path, nrows=5, encoding='utf-8', encoding_errors='replace', on_bad_lines='skip')
                text_col = self._find_text_column(first_chunk)
                embedding_format = self._detect_embedding_format(first_chunk)
                if text_col is None:
                     raise ValueError(f"Could not find text column in {file_path}")

            # Read file in chunks
            chunk_size = 2000 
            for chunk_df in pd.read_csv(file_path, chunksize=chunk_size, encoding='utf-8', encoding_errors='replace', on_bad_lines='skip'):
                chunk_df = chunk_df.loc[:, ~chunk_df.columns.str.contains('^Unnamed')]
                batch_texts, batch_embs = self._extract_embeddings(chunk_df, text_col, embedding_format)
                valid_chunks.extend(batch_texts)
                valid_embeddings.extend(batch_embs)
                del chunk_df

        if not valid_embeddings:
            raise ValueError("No valid embeddings found in any file")
        
        logger.info(f"✅ Loaded {len(valid_embeddings)} embeddings values successfully.")
        
        embeddings_array = np.vstack(valid_embeddings).astype('float32')
        index = faiss.IndexFlatIP(self.embedding_dim)
        index.add(embeddings_array)
        
        return valid_chunks, embeddings_array, index
    
    def _find_text_column(self, df: pd.DataFrame) -> Optional[str]:
        for col in ['chunk', 'chunk_text', 'content', 'text', 'article', 'news_text', 'Text', 'Content']:
            if col in df.columns: return col
        for col in df.columns:
            if any(word in col.lower() for word in ['chunk', 'text', 'content', 'article']): return col
        return None
    
    def _detect_embedding_format(self, df: pd.DataFrame) -> str:
        for col in ['embedding', 'embeddings', 'vector', 'emb', 'Embedding']:
            if col in df.columns: return f"single_column:{col}"
        numeric_cols = df.select_dtypes(include=['float64', 'float32', 'int64', 'int32']).columns
        if len(numeric_cols) >= 100: return f"spread:{len(numeric_cols)}_columns"
        return "unknown"
    
    def _extract_embeddings(self, df: pd.DataFrame, text_col: str, embedding_format: str) -> Tuple[List[str], List[np.ndarray]]:
        batch_chunks = []
        batch_embeddings = []
        
        if embedding_format.startswith("single_column:"):
            emb_col = embedding_format.split(":")[1]
            for idx, row in df.iterrows():
                try:
                    val = row[emb_col]
                    if pd.isna(val) or val == '': continue
                    
                    # Faster string parsing
                    if isinstance(val, str):
                        val = val.strip()
                        if val.startswith('[') and val.endswith(']'):
                            # Try JSON first (faster usually)
                            try: embedding = json.loads(val)
                            except: embedding = ast.literal_eval(val)
                        else:
                            continue
                    elif isinstance(val, (list, tuple)):
                        embedding = val
                    else: continue
                    
                    emb_arr = np.array(embedding, dtype=np.float32)
                    if emb_arr.shape[0] != self.embedding_dim: continue
                    
                    # Normalize
                    norm = np.linalg.norm(emb_arr)
                    if norm > 0: emb_arr /= norm
                    
                    txt = row[text_col]
                    if pd.isna(txt) or str(txt).strip() == '': continue
                    
                    batch_chunks.append(str(txt))
                    batch_embeddings.append(emb_arr)
                except: continue
        
        elif embedding_format.startswith("spread:"):
            # Logic for spread columns (optimized)
            numeric_cols = df.select_dtypes(include=['float64', 'float32', 'int64', 'int32']).columns.tolist()
            if text_col in numeric_cols: numeric_cols.remove(text_col)
            # Ensure we only take up to dim
            cols_to_use = numeric_cols[:self.embedding_dim]
            
            # Vectorized extraction is risky if rows are missing data, but faster
            # Let's do row-by-row for safety in this constrained env
            for idx, row in df.iterrows():
                try:
                    raw_vals = row[cols_to_use].values.astype(np.float32)
                    if len(raw_vals) < self.embedding_dim:
                         padding = np.zeros(self.embedding_dim - len(raw_vals), dtype=np.float32)
                         raw_vals = np.concatenate([raw_vals, padding])
                    
                    norm = np.linalg.norm(raw_vals)
                    if norm > 0: raw_vals /= norm
                    
                    batch_chunks.append(str(row[text_col]))
                    batch_embeddings.append(raw_vals)
                except: continue
                
        return batch_chunks, batch_embeddings
    
    def _normalize_query(self, query: str) -> str:
        return ' '.join(query.strip().split())
    
    def _detect_language(self, query: str) -> str:
        telugu_chars = sum(1 for c in query if '\u0C00' <= c <= '\u0C7F')
        if telugu_chars > len(query) * 0.3: return 'telugu'
        return 'english'

    def _is_greeting(self, query: str) -> bool:
        """Lightweight intent router for greetings/casual inputs."""
        greetings = [
            'hi', 'hello', 'hey', 'namaskaram', 'namaste', 'bagunnara', 
            'how are you', 'good morning', 'good afternoon', 'good evening',
            'em chestunnav', 'what are you doing', 'who are you', 'evaru nuvvu'
        ]
        q_lower = query.lower().strip()
        # Direct match or starts with greeting word (up to 3 words)
        if len(q_lower.split()) <= 3 and any(q_lower.startswith(g) for g in greetings):
            return True
        return False

    def _clean_output(self, text: str) -> str:
        """Remove markdown artifacts for clean plain text."""
        # Remove bold/italic markers
        text = text.replace('**', '').replace('*', '').replace('__', '')
        # Remove bullet points (-, •) at start of lines
        cleaned_lines = []
        for line in text.split('\n'):
            line = line.strip()
            # Remove leading bullets
            line = re.sub(r'^[-•]\s*', '', line)
            # Remove numbered lists "1. "
            line = re.sub(r'^\d+\.\s*', '', line)
            cleaned_lines.append(line)
        return '\n'.join(cleaned_lines)

    def _safe_generate_content(self, prompt: str, retry: bool = True) -> Optional[str]:
        """
        3️⃣ Automatic Safe Fallback (FAIL-SAFE)
        Wraps Gemini calls with error handling, logging, and retry logic.
        """
        if not hasattr(self, 'gemini_model'):
            logger.error("❌ Gemini model not initialized.")
            return None

        try:
            response = self.gemini_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(temperature=0.3)
            )
            if response.text:
                return response.text.strip()
        except Exception as e:
            logger.warning(f"⚠️ Gemini {self.model_name} Error: {e}")
            if retry:
                logger.info("🔄 Retrying generation...")
                try:
                    # Retry logic (could use sleep here if heavy load, but keeping it simple)
                    response = self.gemini_model.generate_content(prompt)
                    if response.text:
                        return response.text.strip()
                except Exception as retry_e:
                    logger.error(f"❌ Gemini Retry Failed: {retry_e}")
        
        return None

    def _retrieve_chunks(self, query: str) -> List[Tuple[str, float]]:
        normalized_query = self._normalize_query(query)
        try:
            response = self.cohere_client.embed(
                texts=[normalized_query],
                model="embed-multilingual-v3.0",
                input_type="search_query"
            )
            query_embedding = np.array(response.embeddings[0], dtype=np.float32)
            query_embedding = query_embedding / np.linalg.norm(query_embedding)
        except Exception as e:
            logger.error(f"❌ Error generating query embedding: {e}")
            return []
        
        similarities, indices = self.index.search(query_embedding.reshape(1, -1), self.top_k * 2)
        results = []
        for sim, idx in zip(similarities[0], indices[0]):
            if sim >= self.similarity_threshold:
                results.append((self.chunks[idx], float(sim)))
        return results[:self.top_k]

    def _rewrite_query(self, query: str, history: List[Dict[str, str]]) -> str:
        """
        Uses LLM to rewrite the user query based on conversation history.
        This handles pronouns, follow-ups (Enduku?), and context switching.
        """
        if not history:
            return query
            
        # Limit history to last few turns
        recent_history = history[-6:] 
        
        hist_text = ""
        for msg in recent_history:
            role = "User" if msg['role'] == 'user' else "Assistant"
            hist_text += f"{role}: {msg['content']}\n"
            
        prompt = f"""You are a query refinement AI for a Telugu news bot.
Conversation History:
{{hist_text}}

Current User Input: {{query}}

Task: Rewrite the user input into a standalone, specific search query.
- Resolve pronouns ("idi", "adi", "ayana") to the actual entities mentioned in history.
- If the user asks "Enduku?" (Why?) or "Ela?" (How?), append the topic from history (e.g., "Why Telangana rainfall is increasing").
- If the input is fully standalone (e.g., "New topic"), return it as is.
- Output ONLY the rewritten query text. No explanations.

Rewritten Query:"""

        # We use format explicitly because of f-string brace escaping issues in large blocks
        try:
            final_prompt = prompt.format(hist_text=hist_text, query=query)
            
            rewritten = self._safe_generate_content(final_prompt)
            
            if not rewritten:
                return query
                
            logger.info(f"🔄 Contextualized Query: '{query}' -> '{rewritten}'")
            return rewritten
        except Exception as e:
            logger.warning(f"⚠️ Query Rewrite Error: {e}")
            return query

    def generate_daily_brief(self) -> Dict[str, str]:
        """
        Generates a 'Morning Briefing' style summary from random/top content.
        """
        logger.info("🌤️ Generating Daily Editorial Brief...")
        
        # Select context for the brief
        # Strategy: Randomly sample 8 chunks to simulate "diverse news"
        # In a real DB system, we would query "created_at > yesterday", 
        # but here we rely on the static CSV content.
        import random
        selected_chunks = random.sample(self.chunks, min(len(self.chunks), 8))
        context_text = "\n\n".join([f"- {c}" for c in selected_chunks])
        
        prompt = f"""You are the Editor-in-Chief of 'Manavartha', a premium Telugu News App.

Task: Create a "Daily Editorial Brief" (వార్తా సమాహారం) for today.
Context:
{context_text}

Instructions:
1.  **Format**:
    - **Headline**: Catchy, dated headline (e.g., "ఈరోజు ముఖ్యాంశాలు").
    - **Top Stories**: 3-4 bullet points summarizing the most interesting news from the context.
    - **Editorial Quote**: A short, inspiring or neutral observation about the day's trends.
2.  **Tone**: Professional, crisp, and high-quality Telugu.
3.  **No Markdown**: Use plain text formatting. Use dashes (-) for bullets.

Output (Telugu):
"""
        # 3. Automatic Safe Fallback
        brief = self._safe_generate_content(prompt)
        
        if brief:
            brief = self._clean_output(brief)
            return {
                "title": "Daily Brief",
                "content": brief
            }
        else:
            return {"title": "Error", "content": "క్షమించండి, వార్తా సమాహారం సిద్ధం చేయలేకపోయాను."}

    def generate_answer(self, query: str, mode: str = "standard", history: List[Dict] = []) -> Dict[str, any]:
        """
        Main Agentic Pipeline with Mode Support and Conversational Memory:
        Modes:
        - 'standard': Balanced (Bridge + Answer + Why This Matters)
        - 'quick': Concise, bullets, no fluff
        - 'deep': Extensive context, background, analysis
        """
        # 1. Contextualize (Rewrite) Query
        search_query = self._rewrite_query(query, history)
        
        logger.info(f"💬 Processing query: {query} (Search: {search_query}) [Mode: {mode}]")
        language = self._detect_language(search_query)
        
        # 2. Intent Router (Skip for greetings if standard)
        is_greeting = self._is_greeting(search_query)
        
        # 4️⃣ Greeting & Short Input Bypass (IMPORTANT)
        if is_greeting:
            logger.info("👋 Detected greeting, bypassing RAG/Gemini.")
            return {
                "query": query,
                "answer": "నమస్కారం! నేను మనవార్త AI ని. తాజా వార్తల కోసం అడగండి.",
                "sources": [],
                "language": language,
                "chunks_retrieved": 0
            }

        retrieved_chunks = []
        context_text = ""
        
        # 3. Retrieval (Use Rewritten Query)
        retrieved_chunks = self._retrieve_chunks(search_query)
        if retrieved_chunks:
            for i, (chunk, _) in enumerate(retrieved_chunks, 1):
                context_text += f"Article {i}:\n{chunk}\n\n"
        
        # 4. Prompt Logic based on MODE
        intent_guide = ""
        structure_guide = ""
        
        lower_query = search_query.lower()
        
        if mode == "quick":
            intent_guide = "- Provide a very short, bulleted summary. Max 100 words."
            structure_guide = """    - **Summary**: 3-4 bullet points.
    - **No Intro/Outro**: Go straight to the point."""
            
        elif mode == "deep":
            intent_guide = "- Provide an exhaustive explanation with background and future implications."
            structure_guide = """    - **Bridge Line** (Professional)
    - **Background Context**: History or origin of the issue.
    - **Detailed Analysis**: Key arguments and details.
    - **Future Outlook**: What might happen next.
    - **Why This Matters**: Detailed insight."""
            
        else: # Standard Mode (Existing Premium Logic)
            if "why" in lower_query or "enduku" in lower_query:
                intent_guide = "- Provide a detailed, logical explanation."
                structure_guide = """    - **Bridge Line**
    - **Core Answer**: Detailed explanation.
    - **Why This Matters (MANDATORY)**: Ends with a section explicitly titled "ఇది ఎందుకు ముఖ్యం:" followed by 1-2 lines of insight.
    - **Summary**: Ends with "సంక్షిప్తంగా:" """
            elif len(search_query.split()) < 4 or is_greeting:
                intent_guide = "- Provide a concise, direct answer in a friendly tone."
                structure_guide = """    - **Bridge Line** (Brief)
    - **Core Answer**: Direct and simple.
    - (Skip 'Why This Matters')"""
            else:
                intent_guide = "- Provide a balanced news summary with context."
                structure_guide = """    - **Bridge Line**
    - **Core Answer**: Clear, well-structured paragraphs.
    - **Why This Matters (MANDATORY for news)**: Ends with a section explicitly titled "ఇది ఎందుకు ముఖ్యం:" followed by 1-2 lines of insight.
    - **Summary**: Ends with "సంక్షిప్తంగా:" """

        # 5. Build Final Prompt with History
        history_section = ""
        if history:
            history_section = "Conversation History (for context):\n"
            for msg in history[-4:]: # Last 4 turns
                role = "User" if msg['role'] == 'user' else "Assistant"
                # Truncate content
                content = msg['content'][:300] + "..." if len(msg['content']) > 300 else msg['content']
                history_section += f"{role}: {content}\n"
            history_section += "\n"

        prompt = f"""You are 'Manavartha', a Senior Telugu News Editor and highly intelligent AI Assistant.
        
{history_section}
Context (if available):
{context_text}

User Question: "{query}" (Context: "{search_query}")

CORE INSTRUCTIONS:
1.  **Role**: Act as a seasoned journalist—neutral, professional, yet conversational.
2.  **Bridge**: If mode is NOT 'quick', start with a natural Telugu bridge.
3.  **Tone**: {intent_guide}
4.  **Structure**:
{structure_guide}
5.  **Strict Formatting**:
    - **NO MARKDOWN**. Plain text only.

6.  **Safety**:
    - If context is missing/irrelevant, admit it politely.

Generative Response:
"""
        
        answer = ""
        if not is_greeting:
            raw_answer = self._safe_generate_content(prompt)
            answer = self._clean_output(raw_answer) if raw_answer else None
        else:
            # Greeting bypass - already handled via intent router conceptually, 
            # but if we reached here with is_greeting=True (logic flow), we should respond simply.
            # Actually, standard flow skips retrieval but still prompts? 
            # Let's use a lightweight fallback if prompt fails or just prompt.
            raw_answer = self._safe_generate_content(prompt)
            answer = self._clean_output(raw_answer) if raw_answer else "నమస్కారం! నేను మనవార్త AI ని. మీకు ఎలా సహాయపడగలను?"

        if not answer:
             # Final Fail-Safe Fallback
             answer = "క్షమించండి, ప్రస్తుతం సమాచారాన్ని పొందడంలో అంతరాయం ఏర్పడింది. కొద్దిసేపటి తర్వాత ప్రయత్నించండి."
        
        return {
            "query": query,
            "answer": answer,
            "sources": [chunk for chunk, _ in retrieved_chunks[:3]],
            "language": language,
            "chunks_retrieved": len(retrieved_chunks)
        }

# Singleton instance
rag_engine: Optional[TeluguNewsRAG] = None

def initialize_rag(csv_path: str) -> TeluguNewsRAG:
    global rag_engine
    rag_engine = TeluguNewsRAG(csv_path)
    return rag_engine

def get_rag_engine() -> TeluguNewsRAG:
    if rag_engine is None: raise RuntimeError("RAG initialized.")
    return rag_engine