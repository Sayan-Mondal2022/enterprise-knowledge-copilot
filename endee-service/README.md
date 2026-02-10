# 📦 Endee Middleware Service

This service acts as the secure **Middleware** between the Client (LangChain RAG Service) and the **Endee Vector Database**. It decouples the application logic from the storage layer, ensuring no direct connection exists between the Frontend and the Vector DB.

## 🚀 Overview

The **Endee Service** is a Flask-based REST API designed to handle all vector database operations centrally.

* **Middleware Role**: Acts as the bridge between the LangChain Service and the Endee Vector DB.
* **Secure Interaction**: The Frontend/LangChain service never talks directly to the DB; all requests go through this API.
* **Powered by Flask**: Lightweight and fast Python web server.
* **Validation Layer**: Includes strict input validation for vector dimensions, index names, and data types before they reach the database.

## 🛠️ Tech Stack

* **Framework**: Flask
* **Language**: Python 3.11
* **Vector DB Client**: `endee` Python SDK
* **Validation**: Custom validators and `pydantic`

## 🔌 API Endpoints

The service runs on Port `8000` by default.

### 🔹 Single Index (Dense Vectors)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/index/create` | Create a new dense vector index |
| `POST` | `/index/get` | Retrieve index metadata |
| `POST` | `/index/upsert` | Insert or update vectors |
| `POST` | `/index/query` | Perform semantic search (Dense retrieval) |

### 🔸 Hybrid Index (Dense + Sparse)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/index/hybrid/create` | Create a hybrid index (Dense + Sparse support) |
| `POST` | `/index/get` | Retrieve index metadata |
| `POST` | `/index/hybrid/upsert` | Insert vectors with sparse indices/values |
| `POST` | `/index/hybrid/query` | Perform hybrid search (Semantic + Keyword) |

## 📡 API Payload Structures

Below are the JSON payloads required for each endpoint.

### 🔹 Single Index (Dense)

#### 1. Create Index

**Endpoint:** `POST /index/create`
```json
{
  "index_name": "my_knowledge_base",
  "dimension": 384,
  "metric": "cosine",      // Optional: "cosine" (default), "l2", "ip"
  "precision": "INT16D"     // Optional: "INT8D" (default), "FLOAT32", "BINARY"
}
```

#### 2. Upsert Vectors

**Endpoint:** `POST /index/upsert`
```json
{
  "index_name": "my_knowledge_base",
  "embedded_vectors": [
    {
      "id": 101,
      "vector": [0.12, -0.05, 0.88, ...],  // Must match dimension
      "meta": {
        "title": title,
        "description": description,
        "source": source,
        "text": text
      }
    }
  ]
}
```

#### 3. Query Index

**Endpoint:** `POST /index/query`
```json
{
  "index_name": "my_knowledge_base",
  "vector": [0.12, -0.05, 0.88, ...],
  "top_k": 5,
  "include_vectors": false  // Set true to get vectors back in response
}
```

### 🔸 Hybrid Index (Dense + Sparse)

#### 1. Create Hybrid Index

**Endpoint:** `POST /index/hybrid/create`
```json
{
  "index_name": "my_hybrid_base",
  "dimension": 384,
  "sparse_dimension": 30522,  // Vocab size (e.g., BERT vocab size)
  "metric": "cosine",
  "precision": "INT16D"
}
```

#### 2. Upsert Hybrid Vectors

**Endpoint:** `POST /index/hybrid/upsert`
```json
{
  "index_name": "my_hybrid_base",
  "embedded_vectors": [
    {
      "id": 202,
      "vector": [0.12, -0.05, ...],
      "sparse_indices": [101, 2500, 301],  // Token IDs from SPLADE/BM25
      "sparse_values": [0.5, 1.2, 0.8],    // Importance weights
      "meta": {
        "title": title,
        "description": description,
        "source": source,
        "text": text
      }
    }
  ]
}
```

#### 3. Query Hybrid Index

**Endpoint:** `POST /index/hybrid/query`
```json
{
  "index_name": "my_hybrid_base",
  "vector": [0.12, -0.05, ...],
  "sparse_indices": [101, 2500],
  "sparse_values": [0.5, 1.2],
  "top_k": 5
}
```

### 📤 Query Response Structure

Both the **Dense** and **Hybrid** query endpoints return the same JSON structure containing the top-k most relevant results.

**Response JSON:**
```json
{
  "index_name": "my_knowledge_base",
  "top_k": 5,
  "results": [
    {
      "id": 101,
      "similarity": 0.85,       // Similarity score (higher is better for cosine)
      "distance": null,         // Distance metric (if applicable, else null)
      "title": "Document Title",
      "description": "Brief description of the document...",
      "text": "The actual text content retrieved from the chunk..."
    },
    {
      "id": 205,
      "similarity": 0.81,
      "distance": null,
      "title": "Another Document",
      "description": "Description...",
      "text": "Content..."
    }
  ]
}
```

#### 📝 Field Descriptions

| Field | Type | Description |
| :--- | :--- | :--- |
| **`index_name`** | `string` | The specific index queried (e.g., `"enterprise_knowledge_base"`). |
| **`top_k`** | `integer` | The number of relevant results requested. |
| **`results`** | `list` | An array of the most relevant document chunks found. |
| **`results[].id`** | `integer` | Unique identifier of the vector in the database. |
| **`results[].similarity`** | `float` | The similarity score (e.g., Cosine Similarity). Higher is better. |
| **`results[].text`** | `string` | The actual text content used for RAG context generation. |
| **`results[].title`** | `string` | Title of the source document (from metadata). |
| **`results[].description`** | `string` | Brief summary or description of the document (from metadata). |
| **`results[].distance`** | `float` or `null` | The distance metric (if applicable for the chosen metric type). |
