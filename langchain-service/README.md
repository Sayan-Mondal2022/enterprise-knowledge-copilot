# 🧠 LangChain RAG Service

The **LangChain RAG Service** is the user-facing component of the **Enterprise Knowledge Copilot**. It provides an interactive web interface (Streamlit) for users to chat with their internal documentation and manage the knowledge base.

This service handles the complete **RAG (Retrieval-Augmented Generation)** pipeline: from ingesting documents and generating hybrid embeddings to querying the vector database and generating responses using Groq's LLMs.

## ✨ Key Features

* **🤖 Interactive Chat Interface**: A user-friendly chat UI powered by **Streamlit**.
* **📂 Document Ingestion**:
    * Supports **PDF** and **Markdown** file uploads.
    * Automatically cleans, preprocesses, and chunks text.
* **🧠 Advanced Embedding Pipeline**:
    * **Dense Embeddings**: Uses `sentence-transformers/all-MiniLM-L6-v2` for semantic understanding.
    * **Sparse Embeddings (SPLADE)**: Uses `naver/splade-cocondenser-ensembledistil` for keyword-aware lexical search.
* **⚡ Query Modes**:
    * **Normal Mode**: Fast, dense-only retrieval.
    * **Pro Mode**: Hybrid retrieval (Dense + Sparse) for higher accuracy on specific technical terms.
* **🚀 High-Performance LLM**: Powered by **Groq API** (using `llama-3.3-70b-versatile`) for near-instant responses.

## 🛠️ Tech Stack

* **Frontend**: [Streamlit](https://streamlit.io/)
* **Orchestration**: [LangChain](https://www.langchain.com/)
* **LLM Inference**: [Groq API](https://groq.com/)
* **Embeddings**:
    * [Sentence Transformers](https://sbert.net/) (Dense)
    * [SPLADE](https://github.com/naver/splade) (Sparse)
* **Vector Store Interaction**: Custom API calls to **Endee Middleware**.

## 🏗️ Architecture Flow

1.  **Ingestion**: User uploads files -> Text is extracted -> Cleaned -> Chunked (Recursive Character Splitter).
2.  **Vectorization**:
    * Chunks are passed to the Embedding Model (Dense).
    * *If Pro Mode:* Chunks are also passed to the SPLADE Model (Sparse Indices/Values).
3.  **Storage**: Processed vectors are sent to the `endee-service` via REST API for indexing.
4.  **Retrieval & Generation**:
    * User asks a question.
    * System retrieves relevant chunks from `endee-db`.
    * LLM generates a context-aware answer based on retrieved data.


## 📂 Project Structure

```bash
langchain-service/
├── ingestion/
│   ├── chunking.py         # Logic for splitting text into chunks
│   ├── loaders.py          # Handles loading of PDF and Markdown files
│   ├── preprocessing.py    # Cleans and normalizes text data
│   ├── upsert.py           # Manages sending vectors to the Endee service
│   └── vectorize_data.py   # Converts text chunks into vector embeddings
├── rag/
│   ├── embeddings.py       # Loads embedding models (Dense & SPLADE)
│   ├── prompts.py          # Stores system prompts for the LLM
│   ├── rag_helper.py       # Helper functions for retrieval logic
│   └── rag_pipeline.py     # Defines the main RAG chain (Retrieval + Generation)
├── .dockerignore           # Files to exclude from Docker build
├── Dockerfile              # Docker configuration for the service
├── README.md               # README file
├── app.py                  # Main Streamlit application entry point
├── requirements.txt        # Python dependencies
├── testing.ipynb           # Notebook for testing single index functionality
└── testing_hybrid_db.ipynb # Notebook for testing hybrid index functionality
```

## 📖 Usage Guide

### 1. Ingesting Documents
1.  Open the **sidebar** on the left.
2.  Click **"Browse files"** under "Upload Documents".
3.  Select your `.pdf` or `.md` files.
4.  Click **"📥 Ingest Documents"**.
5.  Wait for the success message: *✅ Documents ingested successfully*.

### 2. Chatting
1.  Select your mode in the sidebar:
    * **Normal**: For general questions.
    * **Pro**: For specific, technical, or keyword-heavy questions.
2.  Type your question in the chat input (e.g., *"What is the company policy on remote work?"*).
3.  The assistant will retrieve relevant context and generate an answer.

## ⚠️ Troubleshooting

| Error | Solution |
| :--- | :--- |
| **`ConnectionError` / `Backend service not reachable`** | Ensure `endee-service` is running and `ENDEE_SERVICE_URL` is set correctly in `.env`. |
| **`GROQ_API_KEY not found`** | Make sure you created the `.env` file and added your key. |
| **Ingestion Fails** | Check if the files are valid PDFs/Markdown. Ensure the backend DB is up. |

## ⚙️ Advanced Configuration

### Environment Variables
You can configure the service using the following environment variables in your `.env` file:

| Variable | Description | Default Value |
| :--- | :--- | :--- |
| **`GROQ_API_KEY`** | **Required**. API Key for Groq Cloud (LLM provider). | `None` |
| **`ENDEE_SERVICE_URL`** | URL of the running Endee Middleware Service. | `http://localhost:8000` |

### 🤖 Customizing the Persona
By default, the bot is configured as **"GitLab Copilot"**. To change this for your own organization:

1. Open `rag/prompts.py`.
2. Edit the `system_prompt` string:
   ```python
   system_prompt = """
   You are a professional assistant for [YOUR COMPANY NAME].
   Your name is '[YOUR BOT NAME]'...
   """
   ```
3. Restart the Streamlit app to apply changes.

### 🧩 Ingestion Details

If you need to tune how documents are processed:

- **Chunking:** Modified in `ingestion/chunking.py`. Default is `chunk_size=500`, `chunk_overlap=100`.
- **Clean-up:** Text cleaning logic (removing YAML, HTML tags) is located in `ingestion/preprocessing.py`.

## ❤️ Thank You

Thank you for using the **LangChain RAG Service**! I hope this interface makes it easy for your team to access internal knowledge.

If you find this project useful, please consider giving the main repository a ⭐ **Star** on GitHub.

* **Main Repository**: [Enterprise Knowledge Copilot](https://github.com/Sayan-Mondal2022/enterprise-knowledge-copilot)
* **Feedback**: Have ideas for a better UI or new features? Open an issue!

Happy Coding! 🚀
