import os
import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError

ENDEE_URL = os.getenv("ENDEE_DB_URL", "http://localhost:8080")

SINGLE_INDEX_QUERY_URL = f"{ENDEE_URL}/index/upsert"
HYBRID_INDEX_QUERY_URL = f"{ENDEE_URL}/index/hybrid/upsert"

SINGLE_INDEX_NAME = "enterprise_knowledge_base2"
HYBRID_INDEX_NAME = "enterprise_knowledge_base2_hybrid"

# Performing list slicing because, insertion limit is 1000 vectors, and I am keeping 950 vectors per upsert
def get_slices(vectors, batch_size=950):
    slices = []
    for start in range(0, len(vectors), batch_size):
        end = min(start + batch_size, len(vectors))
        slices.append((start, end))
    return slices

# This is the function to UPSERT the VECTORS into DB
def upsertVectors(payload, URL):
    try:
        response = requests.post(
            URL,
            json=payload,
            timeout=15
        )
        response.raise_for_status()

        return {
            "success": True,
            "message": "Vectors upserted successfully",
            "data": response.json()
        }

    except ConnectionError:
        return {
            "success": False,
            "message": "Backend service is not reachable",
            "data": None
        }

    except Timeout:
        return {
            "success": False,
            "message": "Request timed out",
            "data": None
        }

    except HTTPError as e:
        try:
            err = e.response.json()
            return {
                "success": False,
                "message": err.get("error", "HTTP error occurred"),
                "data": None
            }
        except ValueError:
            return {
                "success": False,
                "message": e.response.text,
                "data": None
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Unexpected error: {str(e)}",
            "data": None
        }


def batch_upsert_vectors(vectors, INDEX_NAME, URL):
    slices = get_slices(vectors)
    result = {}

    for start, end in slices:
        payload = {
            "index_name": INDEX_NAME,
            "embedded_vectors": vectors[start: end]
        }

        result = upsertVectors(payload, URL)
    
    return result


def upsert_single_index(vectors):
    return batch_upsert_vectors(vectors, SINGLE_INDEX_NAME, SINGLE_INDEX_QUERY_URL)


def upsert_hybrid_index(vectors):
    return batch_upsert_vectors(vectors, HYBRID_INDEX_NAME, HYBRID_INDEX_QUERY_URL)