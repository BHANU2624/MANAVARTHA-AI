import google.generativeai as genai
import os
from dotenv import load_dotenv
import sys

# Force UTF-8
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv(encoding='utf-8-sig')
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("NO API KEY")
else:
    genai.configure(api_key=api_key)
    print("Listing available models:")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"Error listing models: {e}")
