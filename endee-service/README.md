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
