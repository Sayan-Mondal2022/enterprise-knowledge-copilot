# 🚀 Enterprise Knowledge Copilot

This project implements an Enterprise Knowledge Base Copilot that enables employees to query internal documentation using natural language.

It uses semantic search powered by a **vector database** and **Retrieval-Augmented Generation (RAG)** to return accurate, step-by-step answers grounded in organizational knowledge such as policies, SOPs, and technical documentation.



## 🧠 Project Overview

Enterprise Knowledge Copilot is a **Retrieval-Augmented Generation (RAG)** system that:

- Stores enterprise documents in a **hybrid vector database**
- Performs **semantic + keyword-aware retrieval**
- Uses **LLMs to generate grounded, contextual answers**
- Supports **Normal** and **Pro** query modes for cost-performance control

The architecture follows a **microservices approach**, separating vector storage from LLM reasoning.



## ✨ Features

- 🔍 **Hybrid Retrieval** (Dense + Sparse)
- 🧠 **Custom Open-Source Vector DB (Endee)**
- 🔗 **LangChain-based RAG Pipeline**
- ⚡ Fast similarity search with indexing
- 🧩 Modular services (DB + LLM decoupled)



## 🛠 Tech Stack

### Python Version
- Python 3.11 recommended
- Python 3.10 / 3.11 supported
- Python 3.12+ not recommended

### Backend & AI
- LangChain
- HuggingFace Transformers
- Sentence Transformers
- SPLADE (Sparse embeddings)
- Groq compatible LLMs

### Data & Storage
- Endee Vector Database (Dense + Sparse)
- JSON-based payloads



## 🏗 System Architecture

Will be adding a image

## ▶️ Local Installation Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Sayan-Mondal2022/enterprise-knowledge-copilot.git
cd enterprise-knowledge-copilot
```

### 2️⃣ Environment Configuration

```bash
# Required for the LLM (LangChain Service)
GROQ_API_KEY=your_groq_api_key_here
```

### 🚀 Option A: Run with Docker (When you already have docker)

```bash
docker-compose up --build
```

Services will be available at:

- Frontend (Streamlit): `http://localhost:8501`
- Endee Middleware API: `http://localhost:8000`
- Endee Vector DB: `http://localhost:8080`

### 🛠 Option B: Manual Setup

> Note: You must still run the `endee-db` core via Docker or have it installed locally, as it is a compiled service.

**1. Start the Vector Database**

```bash
docker-compose up -d endee-db
```

**2. Set up the Endee Middleware Service**

Open a new terminal:
```bash
cd endee-service

# Create virtual environment
python -m venv .endee-venv
source .endee-venv/bin/activate  # On Windows: .endee-venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API
python api.py
```

Service running on `http://localhost:8000`

**3. Set up the LangChain RAG Service**

Open a new terminal:
```bash
cd langchain-service

# Create virtual environment
python -m venv .langchain-venv
source .langchain-venv/bin/activate # On Windows: .langchain-venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit App
streamlit run app.py
```

App running on `http://localhost:8501`


## 📚 Detailed Documentation

### 📦 Endee Vector Database Service
This service acts as the middleware API (Flask) for the custom Vector DB. It handles index management, vector storage, and executes both dense and hybrid search queries.
👉 **[Read More](./endee-service/README.md)**

### 🧠 LangChain RAG Service
This is the user-facing Streamlit application. It manages the full RAG pipeline, including document ingestion, chunking, embedding generation, and the chat interface powered by Groq.
👉 **[Read More](./langchain-service/README.md)**

## 🙏 Acknowledgements

This project would not have been possible without the amazing open-source community and the following powerful tools:

* **[Endee Vector Database](https://github.com/endee-io/endee.git)**: Special thanks to the creators of **Endee** for providing the high-performance, custom vector database that powers the core retrieval engine of this project.
* **[LangChain](https://www.langchain.com/)**: For the robust framework used to build the RAG pipeline and manage LLM interactions.
* **[Groq](https://groq.com/)**: For providing the ultra-fast inference API that powers the generative capabilities of the system.
* **[Streamlit](https://streamlit.io/)**: For enabling the rapid development of the interactive frontend interface.
* **[Hugging Face](https://huggingface.co/) & [Sentence Transformers](https://www.sbert.net/)**: For the state-of-the-art embedding models and transformers.
* **[Naver Labs Europe](https://europe.naverlabs.com/)**: For the **SPLADE** model architecture used for efficient sparse retrieval.

## ❤️ Thank You

Thank you for checking out **Enterprise Knowledge Copilot**! I hope this tool helps you build powerful internal knowledge assistants.

If you find this project useful, please consider giving it a ⭐ **Star** on GitHub! Your support motivates me to keep improving the system.

### 🌟 Show Your Support

* **Star the Repo**: It helps others discover the project.
* **Fork & Contribute**: Pull requests are welcome!
* **Open an Issue**: Found a bug or have a feature request? Let me know.

Happy Coding! 🚀
