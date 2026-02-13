import os
import pandas as pd
import math

def split_csv(input_file, output_dir, chunk_size_mb=45):
    """
    Splits a CSV file into smaller chunks based on size.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Estimate rows per chunk based on file size
    file_size_mb = os.path.getsize(input_file) / (1024 * 1024)
    print(f"Input File Size: {file_size_mb:.2f} MB")
    
    # Read first 1000 lines to estimate row size
    sample = pd.read_csv(input_file, nrows=1000)
    sample.to_csv("temp_sample.csv", index=False)
    sample_size_mb = os.path.getsize("temp_sample.csv") / (1024 * 1024)
    os.remove("temp_sample.csv")
    
    avg_row_size_mb = sample_size_mb / 1000
    rows_per_chunk = int(chunk_size_mb / avg_row_size_mb)
    
    print(f"Estimated rows per chunk: {rows_per_chunk}")
    
    chunk_num = 0
    total_rows = 0
    
    print("Starting split process...")
    try:
        # Use robust encoding options
        for chunk in pd.read_csv(input_file, chunksize=rows_per_chunk, encoding='utf-8', encoding_errors='replace', on_bad_lines='skip'):
            output_file = os.path.join(output_dir, f"part_{chunk_num:03d}.csv")
            chunk.to_csv(output_file, index=False)
            print(f"Saved {output_file} (Rows: {len(chunk)})")
            chunk_num += 1
            total_rows += len(chunk)
            
        print(f"✅ Successfully split into {chunk_num} files.")
    except Exception as e:
        print(f"❌ Error splitting file: {e}")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILE = os.path.join(BASE_DIR, "data", "all_telugu_chunk_embeddings_clean.csv")
    OUTPUT_DIR = os.path.join(BASE_DIR, "data", "chunks")
    
    split_csv(INPUT_FILE, OUTPUT_DIR)
