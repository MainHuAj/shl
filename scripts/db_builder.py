import sys
import chromadb
from pathlib import Path
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

sys.path.insert(0, str(Path(__file__).parent.parent))
from app.catalog import get_catalog


BASE_DIR = Path(__file__).parent.parent

client = chromadb.PersistentClient(path=BASE_DIR/"chroma_db")
collection = client.create_collection(
    name="shl-assessment",
    metadata={"hnsw:space": "cosine"},
    embedding_function=DefaultEmbeddingFunction()
    )


entries = get_catalog()
for entry in entries:
    collection.add(
        ids=[entry["entity_id"]],
        documents=[entry["embed_text"]],
        metadatas=[{
            "name": entry["name"],
            "url": entry["url"],
            "test_type": entry["test_type"],
            "duration": entry["duration"],
            "keys": ", ".join(entry["keys"]),
            "languages": ", ".join(entry["languages"]),
            "description": entry["description"][:500],
            "job_levels": ", ".join(entry["job_levels"]),
        }]
    )