import os
import pandas as pd
import cohere
import numpy as np
from dotenv import load_dotenv

# Load env or use fallback key
load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    api_key = "DSdAuREU39x4mYDJaSDZ3DEmGM1x8000F7BZuRf2"

print(f"Using API Key: {api_key[:5]}...")

# Initialize Cohere
co = cohere.Client(api_key)

# Sample Telugu News Data
news_samples = [
    """హైదరాబాద్: తెలంగాణ రాష్ట్రంలో రానున్న మూడు రోజుల పాటు ఓ మోస్తరు నుంచి భారీ వర్షాలు కురిసే అవకాశం ఉందని వాతావరణ శాఖ తెలిపింది. 
    బంగాళాఖాతంలో ఏర్పడిన అల్పపీడనం వాయుగుండంగా మారే అవకాశం ఉందని అధికారులు హెచ్చరించారు. 
    ముఖ్యంగా ఉత్తర తెలంగాణ జిల్లాల్లో రైతులు అప్రమత్తంగా ఉండాలని సూచించారు.""",
    
    """అమరావతి: ఆంధ్రప్రదేశ్ ప్రభుత్వం కొత్త పారిశ్రామిక విధానాన్ని ప్రకటించింది. 
    దీని ద్వారా రాష్ట్రానికి భారీగా పెట్టుబడులు వస్తాయని పరిశ్రమల మంత్రి తెలిపారు. 
    నిరుద్యోగ యువతకు ఉపాధి అవకాశాలు కల్పించడమే లక్ష్యమని ఆయన పేర్కొన్నారు.""",
    
    """భారత క్రికెట్ జట్టు రాబోయే ప్రపంచ కప్ కోసం ముమ్మరంగా సాధన చేస్తోంది. 
    కెప్టెన్ రోహిత్ శర్మ మాట్లాడుతూ, జట్టు సమతుల్యంగా ఉందని, కచ్చితంగా కప్ గెలుస్తామని ధీమా వ్యక్తం చేశారు.""",
    
    """ప్రపంచ ఆరోగ్య సంస్థ (WHO) కొత్త కోవిడ్ వేరియంట్ పట్ల అప్రమత్తంగా ఉండాలని సూచించింది. 
    ప్రజలు మాస్కులు ధరించాలని, భౌతిక దూరం పాటించాలని కోరింది.""",
    
    """బడ్జెట్ 2024: కేంద్ర ప్రభుత్వం వ్యవసాయ రంగానికి పెద్దపీట వేసింది. 
    ఎరువుల రాయితీని పెంచుతూ నిర్ణయం తీసుకుంది. దీంతో రైతులకు ఊరట కలగనుంది."""
]

print(f"Generating embeddings for {len(news_samples)} news samples...")

try:
    # Generate embeddings
    response = co.embed(
        texts=news_samples,
        model="embed-multilingual-v3.0",
        input_type="search_query"
    )
    
    embeddings = response.embeddings
    print(f"Generated {len(embeddings)} embeddings successfully.")
    
    # Create DataFrame
    data = []
    for text, emb in zip(news_samples, embeddings):
        row = {
            "chunk": text,
            "embedding": str(emb) # Save as string representation of list
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Save to CSV
    output_path = "data/all_telugu_chunk_embeddings_clean.csv"
    df.to_csv(output_path, index=False)
    
    print(f"✅ Data saved to {output_path}")
    print("Files in data folder:", os.listdir("data"))

except Exception as e:
    print(f"❌ Error: {e}")
