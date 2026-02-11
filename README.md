# 🚀 Enterprise Knowledge Copilot

This project implements an Enterprise Knowledge Base Copilot that enables employees to query internal documentation using natural language.

It uses semantic search powered by a **vector database** and **Retrieval-Augmented Generation (RAG)** to return accurate, step-by-step answers grounded in organizational knowledge such as policies, SOPs, and technical documentation.


## 🧠 Project Overview

**Enterprise Knowledge Copilot** is a modular **RAG System** that transforms internal documents into an intelligent knowledge base.

**Core Capabilities:**
* **Hybrid Storage Engine:** Utilizes a custom vector database to store both **Dense** (semantic) and **Sparse** (keyword) embeddings.
* **Dual-Mode Retrieval:**
    * **Normal Mode:** Optimized for fast, semantic Q&A.
    * **Pro Mode:** Enhances accuracy for technical queries using keyword-aware retrieval.
* **Grounded Generation:** Uses LLMs to synthesize answers strictly from retrieved context, minimizing hallucinations.
* **Decoupled Architecture:** Built as independent microservices (Vector DB + RAG Engine) for better maintainability.

## 🚀 Live Demo

The project is live and can be accessed at the following link:

**[Enterprise Knowledge Copilot Live Demo](https://sayansm.dev/enterprise-copilot)**

### 🛡️ Deployment & Security
* **SSL/TLS Encryption:** Secured with Let's Encrypt SSL on a `.dev` domain, ensuring all data transmission is encrypted.
* **Architecture:** Orchestrated via **Docker Compose** with a multi-service setup.
* **Network Security:** Only the frontend is exposed via an **Nginx** reverse proxy, keeping the Flask backend and Vector Database protected within a private internal network.

## 📸 Demo Screenshots

Here is a glimpse of the Enterprise Knowledge Copilot in action.

### Landing page
*The clean and intuitive chat interface where users can upload documents and interact with the Copilot.*
<img width="1913" height="886" alt="image" src="https://github.com/user-attachments/assets/6aa44bc5-e6ad-467f-af9a-78cbeba6f7fb" />

### Configuring the Chatbot
*A dynamic configuration dialog to instantly customize the assistant's name, company, and behavioral instructions.*
<img width="593" height="558" alt="image" src="https://github.com/user-attachments/assets/f7ecac8b-74c8-4fb9-863e-8a84c764dd00" />

### Normal Mode (Dense Search)
*Fast, semantic answers for general queries.*
<img width="1914" height="876" alt="image" src="https://github.com/user-attachments/assets/33faa8af-1abf-4c40-bb52-a2c652a30da9" /> \

### Pro Mode (Hybrid Search)
*High-precision answers using SPLADE for technical terms.*
<img width="1919" height="869" alt="image" src="https://github.com/user-attachments/assets/d4f07ac9-5699-447c-bc48-b9567ffb78ce" /> \

### ⚙️ Document Ingestion
**Upload & Ingest** \
<img width="468" height="596" alt="image" src="https://github.com/user-attachments/assets/768bf5ed-eecd-4f18-8b6b-bd572bf446b7" /> \
*Simple sidebar UI to upload PDF/Markdown files.*

### 📦 Vector Database (Endee)
*Live status of the custom Endee Vector DB handling of SIngle and Hybrid indices.*
<img width="1920" height="875" alt="image" src="https://github.com/user-attachments/assets/5a07efd6-b96b-4bde-9524-d9aabc64bf57" /> \

## ✨ Key Features

- 🔍 **Advanced Hybrid Retrieval**: Combines **Dense Vectors** (semantic meaning) with **Sparse Vectors** (SPLADE keyword matching) for high-precision search.
- 🧠 **Powered by Endee**: Built on a custom, high-performance **Open-Source Vector Database** designed for efficient embedding storage.
- 🔗 **Robust RAG Pipeline**: Orchestrated via **LangChain** to seamlessly retrieve context and generate grounded LLM responses.
- 🤖 **Interactive Chat UI**: A user-friendly frontend built with **Streamlit** that makes document ingestion and querying effortless.
- ⚙️ **Dynamic Persona Configuration**: Instantly customize the assistant's name, company affiliation, and behavioral instructions directly from the UI—no code changes required.
- ⚡ **High-Performance Indexing**: Optimized for ultra-fast similarity search, ensuring low-latency query responses.
- 🧩 **Microservices Architecture**: Fully decoupled **Vector DB** and **LLM Reasoning** layers for better scalability and maintenance.


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

**1️⃣ Clone the Repository**

```bash
git clone https://github.com/Sayan-Mondal2022/enterprise-knowledge-copilot.git
cd enterprise-knowledge-copilot
```

**2️⃣ Environment Configuration**

```bash
# Required for the LLM (LangChain Service)
GROQ_API_KEY=your_groq_api_key_here
```

**🚀 Option A: Run with Docker (When you already have docker)**

```bash
docker-compose up --build
```

Services will be available at:

- Frontend (Streamlit): `http://localhost:8501`
- Endee Middleware API: `http://localhost:8000`
- Endee Vector DB: `http://localhost:8080`

**🛠 Option B: Manual Setup**

If you prefer to run the Python services locally for development, follow these steps.

> **Note:** You must still run the `endee-db` core via Docker or have it installed locally, as it is a compiled service.
> 
> For instructions on installing the core DB locally, refer to the main repository:  
> 👉 **[https://github.com/endee-io/endee.git](https://github.com/endee-io/endee.git)**

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
* **[GitLab Public Handbook](https://handbook.gitlab.com/)**: A special thanks to GitLab for maintaining an open-source company handbook. It served as an incredibly rich, real-world dataset for testing the document ingestion, hybrid retrieval, and RAG capabilities of this project. 
* **Open Source Community**: Thanks to the maintainers of LangChain, Streamlit, and sentence-transformers for building the tools that made this Copilot possible.

## ❤️ Thank You

Thank you for checking out **Enterprise Knowledge Copilot**! I hope this tool helps you build powerful internal knowledge assistants.

If you find this project useful, please consider giving it a ⭐ **Star** on GitHub! Your support motivates me to keep improving the system.

### 🌟 Show Your Support

* **Star the Repo**: It helps others discover the project.
* **Fork & Contribute**: Pull requests are welcome!
* **Open an Issue**: Found a bug or have a feature request? Let me know.

Happy Coding! 🚀
