"""
Check CSV structure and identify correct column names
"""

import pandas as pd
import sys

csv_path = r"C:\Users\bhanu\Documents\capstone project\MVAI\backend\data\all_telugu_chunk_embeddings_clean.csv"

print("🔍 Analyzing CSV structure...\n")

try:
    # Load CSV with low_memory=False to avoid dtype warnings
    df = pd.read_csv(csv_path, low_memory=False, nrows=5)
    
    print(f"✅ CSV loaded successfully")
    print(f"📊 Shape: {df.shape} (rows, columns)\n")
    
    print("📋 All column names:")
    print("="*80)
    for i, col in enumerate(df.columns, 1):
        print(f"{i}. {col}")
    print("="*80)
    
    print("\n🔎 Looking for text/embedding columns...\n")
    
    # Look for likely candidates
    text_candidates = []
    embedding_candidates = []
    
    for col in df.columns:
        col_lower = col.lower()
        
        # Check for text columns
        if any(word in col_lower for word in ['text', 'content', 'chunk', 'article', 'news']):
            text_candidates.append(col)
            print(f"📝 Possible text column: '{col}'")
            # Show sample
            sample = str(df[col].iloc[0])[:100]
            print(f"   Sample: {sample}...\n")
        
        # Check for embedding columns
        if any(word in col_lower for word in ['embed', 'vector', 'emb']):
            embedding_candidates.append(col)
            print(f"🔢 Possible embedding column: '{col}'")
            # Show sample
            sample = str(df[col].iloc[0])[:100]
            print(f"   Sample: {sample}...\n")
    
    if not text_candidates:
        print("⚠️  No obvious text column found. Showing first few columns:")
        for col in df.columns[:5]:
            print(f"\n Column: {col}")
            print(f" Type: {df[col].dtype}")
            print(f" Sample: {df[col].iloc[0]}")
    
    if not embedding_candidates:
        print("⚠️  No obvious embedding column found. Checking numeric columns...")
        
        # Check if embeddings are spread across multiple columns (common format)
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_cols) > 100:
            print(f"✅ Found {len(numeric_cols)} numeric columns - embeddings might be spread across columns")
            print(f"   Columns: {list(numeric_cols[:5])} ... {list(numeric_cols[-5:])}")
            print("\n💡 Your embeddings are likely stored in separate columns (one column per dimension)")
    
    print("\n" + "="*80)
    print("📌 RECOMMENDATION:")
    print("="*80)
    
    if text_candidates and embedding_candidates:
        print(f"✅ Use these columns:")
        print(f"   Text column: '{text_candidates[0]}'")
        print(f"   Embedding column: '{embedding_candidates[0]}'")
    elif text_candidates and len(numeric_cols) > 100:
        print(f"✅ Text column: '{text_candidates[0]}'")
        print(f"✅ Embeddings: Spread across {len(numeric_cols)} numeric columns")
        print(f"   Need to combine columns into single embedding column")
    else:
        print("❌ Unable to automatically identify columns")
        print("   Please manually specify column names")
        
except FileNotFoundError:
    print(f"❌ File not found: {csv_path}")
    print("   Please verify the file path")
except Exception as e:
    print(f"❌ Error reading CSV: {e}")
    import traceback
    traceback.print_exc()