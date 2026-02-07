from langchain_core.documents import Document
import requests
from rag.embeddings import load_embeddingModel, sparse_encoder

embeddingModel = load_embeddingModel()

ENDEE_URL = "http://127.0.0.1:8000"

SINGLE_INDEX_QUERY_URL = f"{ENDEE_URL}/index/query"
HYBRID_INDEX_QUERY_URL = f"{ENDEE_URL}/index/hybrid/query"

SINGLE_INDEX_NAME = "enterprise_knowledge_base2"
HYBRID_INDEX_NAME = "enterprise_knowledge_base2_hybrid"

# Base retriever common to both SINGLE and HYBRID Indexed DBs
def _endee_base_retriever(query_url: str, payload: dict):
    response = requests.post(
        query_url,
        json=payload,
        timeout=20
    )
    response.raise_for_status()

    data = response.json()
    docs = []

    for d in data.get("results", []):
        docs.append(
            Document(
                page_content=d.get("text", ""),
                metadata={
                    "similarity": d.get("similarity"),
                    "source": d.get("source"),
                    "title": d.get("title"),
                    "description": d.get("description")
                }
            )
        )

    return docs

def single_index_retriever(query: str):
    dense_vector = embeddingModel.encode(query).tolist()

    payload = {
        "index_name": SINGLE_INDEX_NAME,
        "vector": dense_vector,
        "top_k": 20
    }

    return _endee_base_retriever(
        query_url=SINGLE_INDEX_QUERY_URL,
        payload=payload
    )

def hybrid_index_retriever(query: str):
    dense_vector = embeddingModel.encode(query).tolist()
    sparse_indices, sparse_values = sparse_encoder(query)

    payload = {
        "index_name": HYBRID_INDEX_NAME,
        "vector": dense_vector,
        "sparse_indices": sparse_indices,
        "sparse_values": sparse_values,
        "top_k": 20
    }

    return _endee_base_retriever(
        query_url=HYBRID_INDEX_QUERY_URL,
        payload=payload
    )