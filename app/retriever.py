import requests
import os
import chromadb
from dotenv import load_dotenv
from pathlib import Path
import time
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
_client = chromadb.PersistentClient(path=str(BASE_DIR / "chroma_db"))
collection = _client.get_collection(
    name="shl-assessment",
    embedding_function=DefaultEmbeddingFunction()
)


HF_URL = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2/pipeline/feature-extraction"
def get_query_embedding(query:str) -> list:
    headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}
    for attempt in range(5):
        response = requests.post(HF_URL, headers=headers, json={"inputs": query})
        if response.status_code == 503:
            wait = response.json().get("estimated_time", 20)
            time.sleep(wait)
        elif response.status_code == 200:
            return response.json()
        else:
            raise RuntimeError(f"HF API error: {response.status_code}")
        
    raise RuntimeError("HF API failed after 5 retries")
    
def retrieve(query : str,top_k :int = 15) -> list[dict]:
    query_embedding = get_query_embedding(query)
    result = collection.query(
    query_embeddings=[query_embedding],
    n_results=top_k
)
    candidates = []
    for metadata in result["metadatas"][0]:
        candidates.append({
            "name": metadata["name"],
            "test_type": metadata["test_type"],
            "keys": metadata["keys"],
            "duration": metadata["duration"],
            "languages": metadata["languages"],
            "url": metadata["url"],
            "description": metadata["description"],
            "job_levels": metadata["job_levels"],
        })
    return candidates

    

