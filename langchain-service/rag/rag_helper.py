import os
from langchain_core.documents import Document
import requests
from rag.embeddings import load_embeddingModel, sparse_encoder, load_tokenizer
from requests.exceptions import ConnectionError, Timeout, HTTPError

embeddingModel = load_embeddingModel()
tokenizer = load_tokenizer()

ENDEE_URL = os.getenv(
    "ENDEE_SERVICE_URL",
    "http://localhost:8000"
)


SINGLE_INDEX_QUERY_URL = f"{ENDEE_URL}/index/query"
HYBRID_INDEX_QUERY_URL = f"{ENDEE_URL}/index/hybrid/query"

SINGLE_INDEX_NAME = "enterprise_knowledge_base2"
HYBRID_INDEX_NAME = "enterprise_knowledge_base2_hybrid"


# This functions will create SINGLE and HYBRID indexed DBs.
# Creates the DB whenever the app starts and checks if they are already created to avoid redundant creation.
def create_load_dbs():
    configs = [
        {
            "name": SINGLE_INDEX_NAME,
            "check_url": f"{ENDEE_URL}/index/get",
            "create_url": f"{ENDEE_URL}/index/create",
            "payload": {
                "index_name": SINGLE_INDEX_NAME,
                "dimension": embeddingModel.get_sentence_embedding_dimension(),
                "precision": "INT16D"
            }
        },
        {
            "name": HYBRID_INDEX_NAME,
            "check_url": f"{ENDEE_URL}/index/get",
            "create_url": f"{ENDEE_URL}/index/hybrid/create",
            "payload": {
                "index_name": HYBRID_INDEX_NAME,
                "dimension": embeddingModel.get_sentence_embedding_dimension(),
                "sparse_dimension": tokenizer.vocab_size,
                "precision": "INT16D"
            }
        }
    ]   
    for item in configs:
        try:
            check_resp = requests.post(
                item["check_url"], 
                json={"index_name": item["name"]}, 
                timeout=5
            )

            if check_resp.status_code == 200 and check_resp.json().get("status") == "index loaded":
                print(f"Index '{item['name']}' already exists and is loaded.")
                continue


            print(f"Index '{item['name']}' not found. Creating now...")
            create_resp = requests.post(item["create_url"], json=item["payload"], timeout=10)
            create_resp.raise_for_status()
            print(f"Successfully created: {create_resp.json()}")

        except (HTTPError, Exception) as e:
                print(f"Check failed for {item['name']}, attempting creation...")
                try:
                    create_resp = requests.post(item["create_url"], json=item["payload"], timeout=10)
                    if create_resp.status_code == 200:
                        print(f"Created {item['name']} after check failure.")
                except Exception as final_err:
                    print(f"Failed to handle {item['name']}: {final_err}")

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