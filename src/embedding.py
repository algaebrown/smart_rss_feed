import yaml
from sentence_transformers import SentenceTransformer
from typing import List

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
model_name = config.get("embedding_model", "BAAI/bge-small-en-v1.5")

# Load embedding model
model = SentenceTransformer(model_name)


def compute_embeddings(texts: List[str]) -> List[List[float]]:
    return model.encode(texts, show_progress_bar=False).tolist()
