"""
MANA VARTHA AI - Production-Grade RAG Engine
Multilingual Telugu News Question Answering System
"""

import os
import ast
import json
import logging
from typing import List, Dict, Tuple, Optional
import pandas as pd
import numpy as np
import faiss
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
        self.similarity_threshold = 0.30  # Minimum cosine similarity
        self.top_k = 7  # Number of chunks to retrieve
        
        # Initialize Cohere client (for embeddings/retrieval)
        cohere_api_key = os.getenv("COHERE_API_KEY")
        if not cohere_api_key:
            raise ValueError("COHERE_API_KEY not found in environment variables")
        self.cohere_client = cohere.Client(cohere_api_key)
        
        # Initialize Gemini client (for answer generation)
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=gemini_api_key)
        self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Load data and build index
        self.chunks, self.embeddings, self.index = self._load_and_build_index()
        logger.info(f"✅ RAG Engine initialized with {len(self.chunks)} chunks")
    
    def _load_and_build_index(self) -> Tuple[List[str], np.ndarray, faiss.IndexFlatIP]:
        """
        Load CSV, parse embeddings, validate dimensions, and build FAISS index.
        Handles both formats: single embedding column or spread across multiple columns.
        
        Returns:
            Tuple of (chunk_texts, embeddings_array, faiss_index)
        """
        logger.info(f"📂 Loading data from {self.csv_path}")
        
        # Load CSV
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        
        # Load CSV and drop unnamed columns (artifacts from export)
        df = pd.read_csv(self.csv_path, low_memory=False)
        
        # Drop all 'Unnamed' columns
        unnamed_cols = [col for col in df.columns if 'Unnamed' in str(col)]
        if unnamed_cols:
            logger.info(f"🧹 Dropping {len(unnamed_cols)} unnamed columns")
            df = df.drop(columns=unnamed_cols)
        
        logger.info(f"📊 CSV shape: {df.shape}")
        logger.info(f"📋 Columns: {list(df.columns[:10])}...")
        
        # Auto-detect column names
        text_col = self._find_text_column(df)
        embedding_format = self._detect_embedding_format(df)
        
        if text_col is None:
            raise ValueError(f"Could not find text column. Available columns: {list(df.columns)}")
        
        logger.info(f"✅ Text column: '{text_col}'")
        logger.info(f"✅ Embedding format: {embedding_format}")
        
        logger.info(f"📊 Loaded {len(df)} rows from CSV")
        
        # Parse embeddings and validate
        valid_chunks, valid_embeddings = self._extract_embeddings(df, text_col, embedding_format)
        
        if len(valid_embeddings) == 0:
            raise ValueError("No valid embeddings found in CSV")
        
        logger.info(f"✅ Successfully parsed {len(valid_embeddings)} valid embeddings")
        
        # Convert to numpy array
        embeddings_array = np.vstack(valid_embeddings).astype('float32')
        
        # Build FAISS index (Inner Product for normalized vectors = Cosine Similarity)
        index = faiss.IndexFlatIP(self.embedding_dim)
        index.add(embeddings_array)
        
        logger.info(f"🔍 FAISS index built with {index.ntotal} vectors")
        
        return valid_chunks, embeddings_array, index
    
    def _find_text_column(self, df: pd.DataFrame) -> Optional[str]:
        """Find the text column in dataframe"""
        # Direct match - prioritize 'chunk' over 'content' for chunked data
        for col in ['chunk', 'chunk_text', 'content', 'text', 'article', 'news_text', 'Text', 'Content']:
            if col in df.columns:
                return col
        
        # Partial match
        for col in df.columns:
            col_lower = col.lower()
            if any(word in col_lower for word in ['chunk', 'text', 'content', 'article']):
                return col
        
        return None
    
    def _detect_embedding_format(self, df: pd.DataFrame) -> str:
        """Detect if embeddings are in single column or spread across multiple columns"""
        # Check for single embedding column
        for col in ['embedding', 'embeddings', 'vector', 'emb', 'Embedding']:
            if col in df.columns:
                return f"single_column:{col}"
        
        # Check for spread format (numeric columns)
        numeric_cols = df.select_dtypes(include=['float64', 'float32', 'int64', 'int32']).columns
        if len(numeric_cols) >= 100:  # Likely spread embeddings
            return f"spread:{len(numeric_cols)}_columns"
        
        return "unknown"
    
    def _extract_embeddings(self, df: pd.DataFrame, text_col: str, embedding_format: str) -> Tuple[List[str], List[np.ndarray]]:
        """Extract text and embeddings based on detected format"""
        valid_chunks = []
        valid_embeddings = []
        error_count = 0
        error_types = {}
        
        if embedding_format.startswith("single_column:"):
            # Single column format
            emb_col = embedding_format.split(":")[1]
            logger.info(f"📦 Extracting from single column: '{emb_col}'")
            
            total_rows = len(df)
            for idx, row in df.iterrows():
                try:
                    # Skip if embedding is NaN or empty
                    if pd.isna(row[emb_col]) or row[emb_col] == '':
                        continue
                    
                    # Parse embedding string to list
                    if isinstance(row[emb_col], str):
                        # Clean up the string before parsing
                        emb_str = row[emb_col].strip()
                        # Try to parse as Python literal
                        try:
                            embedding = ast.literal_eval(emb_str)
                        except (ValueError, SyntaxError) as e:
                            # If literal_eval fails, try json
                            import json
                            try:
                                embedding = json.loads(emb_str)
                            except:
                                error_count += 1
                                error_type = type(e).__name__
                                error_types[error_type] = error_types.get(error_type, 0) + 1
                                continue
                    elif isinstance(row[emb_col], (list, tuple)):
                        embedding = row[emb_col]
                    else:
                        continue
                    
                    # Convert to numpy array
                    embedding = np.array(embedding, dtype=np.float32)
                    
                    # Validate dimension
                    if embedding.shape[0] != self.embedding_dim:
                        error_count += 1
                        error_types['wrong_dimension'] = error_types.get('wrong_dimension', 0) + 1
                        continue
                    
                    # Validate no NaN or Inf
                    if np.any(np.isnan(embedding)) or np.any(np.isinf(embedding)):
                        error_count += 1
                        error_types['nan_or_inf'] = error_types.get('nan_or_inf', 0) + 1
                        continue
                    
                    # Normalize embedding for cosine similarity
                    norm = np.linalg.norm(embedding)
                    if norm > 0:
                        embedding = embedding / norm
                    else:
                        error_count += 1
                        error_types['zero_norm'] = error_types.get('zero_norm', 0) + 1
                        continue
                    
                    # Check if text is valid
                    if pd.isna(row[text_col]) or str(row[text_col]).strip() == '':
                        continue
                    
                    valid_chunks.append(str(row[text_col]))
                    valid_embeddings.append(embedding)
                    
                except Exception as e:
                    error_count += 1
                    error_type = type(e).__name__
                    error_types[error_type] = error_types.get(error_type, 0) + 1
                    continue
            
            # Log summary
            logger.info(f"📊 Processing complete:")
            logger.info(f"   ✅ Valid embeddings: {len(valid_embeddings)}")
            logger.info(f"   ⚠️  Skipped rows: {error_count}")
            if error_types:
                logger.info(f"   Error breakdown: {dict(sorted(error_types.items(), key=lambda x: x[1], reverse=True))}")
            success_rate = (len(valid_embeddings) / total_rows * 100) if total_rows > 0 else 0
            logger.info(f"   📈 Success rate: {success_rate:.1f}%")
        
        elif embedding_format.startswith("spread:"):
            # Spread format - embeddings across multiple columns
            logger.info(f"📦 Extracting from spread columns")
            
            # Get numeric columns (these should be embeddings)
            numeric_cols = df.select_dtypes(include=['float64', 'float32', 'int64', 'int32']).columns.tolist()
            
            # Remove text column if it's somehow in numeric
            if text_col in numeric_cols:
                numeric_cols.remove(text_col)
            
            logger.info(f"📊 Found {len(numeric_cols)} numeric columns for embeddings")
            
            # Check if we have the right number of dimensions
            if len(numeric_cols) != self.embedding_dim:
                logger.warning(f"⚠️ Expected {self.embedding_dim} dimensions, found {len(numeric_cols)}")
                # Take first 1024 if more, pad if less
                if len(numeric_cols) > self.embedding_dim:
                    numeric_cols = numeric_cols[:self.embedding_dim]
            
            for idx, row in df.iterrows():
                try:
                    # Extract embedding from numeric columns
                    embedding = row[numeric_cols].values.astype(np.float32)
                    
                    # Pad if needed
                    if len(embedding) < self.embedding_dim:
                        padding = np.zeros(self.embedding_dim - len(embedding), dtype=np.float32)
                        embedding = np.concatenate([embedding, padding])
                    
                    # Validate no NaN or Inf
                    if np.any(np.isnan(embedding)) or np.any(np.isinf(embedding)):
                        continue
                    
                    # Normalize
                    norm = np.linalg.norm(embedding)
                    if norm > 0:
                        embedding = embedding / norm
                    else:
                        continue
                    
                    valid_chunks.append(str(row[text_col]))
                    valid_embeddings.append(embedding)
                    
                except Exception as e:
                    if idx < 5:  # Only log first few errors to avoid spam
                        logger.warning(f"⚠️ Error parsing row {idx}: {e}")
                    continue
            
            # Log summary for spread format
            logger.info(f"📊 Spread format processing complete:")
            logger.info(f"   ✅ Valid embeddings: {len(valid_embeddings)}")
        
        else:
            raise ValueError(f"Unknown embedding format: {embedding_format}")
        
        return valid_chunks, valid_embeddings
    
    def _normalize_query(self, query: str) -> str:
        """
        Normalize query text for better retrieval.
        Handles Telugu, English, and Romanized Telugu.
        
        Args:
            query: Raw user query
            
        Returns:
            Normalized query string
        """
        # Basic normalization
        normalized = query.strip()
        
        # Remove excessive whitespace
        normalized = ' '.join(normalized.split())
        
        return normalized
    
    def _detect_language(self, query: str) -> str:
        """
        Detect query language: 'telugu', 'english', or 'romanized'
        
        Args:
            query: User query
            
        Returns:
            Language code
        """
        # Check for Telugu unicode characters (0C00-0C7F)
        telugu_chars = sum(1 for c in query if '\u0C00' <= c <= '\u0C7F')
        
        if telugu_chars > len(query) * 0.3:
            return 'telugu'
        elif any(c.isascii() and c.isalpha() for c in query):
            # Check if it's English or Romanized Telugu
            # Romanized Telugu often has words like "em", "ela", "evaru"
            romanized_indicators = ['em', 'ela', 'evaru', 'ekkada', 'eppudu', 'enduku']
            if any(indicator in query.lower() for indicator in romanized_indicators):
                return 'romanized'
            return 'english'
        
        return 'unknown'
    
    def _retrieve_chunks(self, query: str) -> List[Tuple[str, float]]:
        """
        Retrieve top-K relevant chunks using FAISS similarity search.
        
        Args:
            query: User query
            
        Returns:
            List of (chunk_text, similarity_score) tuples
        """
        # Normalize query
        normalized_query = self._normalize_query(query)
        
        # Generate query embedding
        try:
            response = self.cohere_client.embed(
                texts=[normalized_query],
                model="embed-multilingual-v3.0",
                input_type="search_query"
            )
            query_embedding = np.array(response.embeddings[0], dtype=np.float32)
            
            # Normalize for cosine similarity
            query_embedding = query_embedding / np.linalg.norm(query_embedding)
            
        except Exception as e:
            logger.error(f"❌ Error generating query embedding: {e}")
            return []
        
        # Search FAISS index
        similarities, indices = self.index.search(
            query_embedding.reshape(1, -1), 
            self.top_k * 2  # Retrieve more, then filter
        )
        
        # Filter by similarity threshold
        results = []
        for sim, idx in zip(similarities[0], indices[0]):
            if sim >= self.similarity_threshold:
                results.append((self.chunks[idx], float(sim)))
        
        # Limit to top_k
        results = results[:self.top_k]
        
        logger.info(f"🔍 Retrieved {len(results)} chunks with similarity >= {self.similarity_threshold}")
        
        return results
    
    def _build_system_prompt(self, language: str) -> str:
        """
        Build system prompt for Gemini API.
        
        Args:
            language: Detected language
            
        Returns:
            System prompt string
        """
        # Language-specific instructions
        if language == 'telugu':
            lang_instruction = "తెలుగులో సమాధానం ఇవ్వండి."
            not_found_msg = "సంబంధిత సమాచారం లభించలేదు"
        elif language == 'romanized':
            lang_instruction = "Respond in Telugu script if possible, or in English."
            not_found_msg = "Sambandhita samacharamu labhinchaledu"
        else:
            lang_instruction = "Respond in English."
            not_found_msg = "Relevant information not found in the news database"
        
        system_prompt = f"""You are a Telugu news assistant. Answer questions using ONLY the provided Telugu news documents.

STRICT RULES:
1. Use ONLY information from the documents provided below
2. Answer in a concise, factual, news-style format (2-4 sentences maximum)
3. {lang_instruction}
4. If the documents don't contain relevant information, respond EXACTLY with: "{not_found_msg}"
5. Do NOT provide generic explanations or information outside the documents
6. Do NOT make up information or provide assumptions
7. Cite specific details from the news when available (dates, names, numbers)

Your role is to extract and summarize relevant information from Telugu news articles."""
        
        return system_prompt
    
    def _build_prompt(self, query: str, chunks: List[Tuple[str, float]], language: str) -> str:
        """
        Build prompt for legacy compatibility (now using Chat API documents instead).
        This method is kept for backward compatibility but not used in Chat API flow.
        
        Args:
            query: User query
            chunks: Retrieved chunks with similarity scores
            language: Detected language
            
        Returns:
            Formatted prompt string (legacy)
        """
        # Build context from chunks
        context_parts = []
        for i, (chunk, score) in enumerate(chunks, 1):
            context_parts.append(f"[Document {i}] (Relevance: {score:.2f})\n{chunk}")
        
        context = "\n\n".join(context_parts)
        
        return context  # Return just context for reference
    
    def generate_answer(self, query: str) -> Dict[str, any]:
        """
        Main RAG pipeline: Retrieve + Generate answer.
        
        Args:
            query: User query
            
        Returns:
            Dictionary with answer, sources, and metadata
        """
        logger.info(f"💬 Processing query: {query}")
        
        # Detect language
        language = self._detect_language(query)
        logger.info(f"🌐 Detected language: {language}")
        
        # Retrieve relevant chunks
        retrieved_chunks = self._retrieve_chunks(query)
        
        if not retrieved_chunks:
            # No relevant chunks found
            if language == 'telugu':
                answer = "సంబంధిత సమాచారం లభించలేదు. దయచేసి వేరే ప్రశ్న అడగండి."
            else:
                answer = "No relevant information found in the news database. Please try a different question."
            
            return {
                "query": query,
                "answer": answer,
                "sources": [],
                "language": language,
                "chunks_retrieved": 0
            }
        
        # Generate answer using Gemini Flash 2.5
        try:
            # Prepare context from retrieved chunks
            context_text = "\n\n".join([
                f"Document {i+1}:\n{chunk}"
                for i, (chunk, score) in enumerate(retrieved_chunks)
            ])
            
            # Build system prompt
            system_prompt = self._build_system_prompt(language)
            
            # Combine system prompt, context, and query for Gemini
            full_prompt = f"""{system_prompt}

===== NEWS DOCUMENTS =====
{context_text}

===== USER QUERY =====
{query}

===== YOUR ANSWER =====
"""
            
            # Generate answer using Gemini Flash 2.5
            response = self.gemini_model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=300,
                )
            )
            
            answer = response.text.strip()
            
        except Exception as e:
            logger.error(f"❌ Error generating answer: {e}")
            if language == 'telugu':
                answer = "క్షమించండి, సమాధానం రూపొందించడంలో సమస్య ఏర్పడింది. దయచేసి మళ్లీ ప్రయత్నించండి."
            else:
                answer = "Sorry, there was an error generating the answer. Please try again."
        
        # Prepare sources (top 3 chunks)
        sources = [chunk for chunk, _ in retrieved_chunks[:3]]
        
        result = {
            "query": query,
            "answer": answer,
            "sources": sources,
            "language": language,
            "chunks_retrieved": len(retrieved_chunks)
        }
        
        logger.info(f"✅ Answer generated successfully")
        
        return result


# Singleton instance (will be initialized in main.py)
rag_engine: Optional[TeluguNewsRAG] = None


def initialize_rag(csv_path: str) -> TeluguNewsRAG:
    """
    Initialize the RAG engine singleton.
    
    Args:
        csv_path: Path to embeddings CSV
        
    Returns:
        Initialized TeluguNewsRAG instance
    """
    global rag_engine
    rag_engine = TeluguNewsRAG(csv_path)
    return rag_engine


def get_rag_engine() -> TeluguNewsRAG:
    """
    Get the RAG engine instance.
    
    Returns:
        TeluguNewsRAG instance
        
    Raises:
        RuntimeError if engine not initialized
    """
    if rag_engine is None:
        raise RuntimeError("RAG engine not initialized. Call initialize_rag() first.")
    return rag_engine