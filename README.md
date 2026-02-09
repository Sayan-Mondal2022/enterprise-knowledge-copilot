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

## ▶️ How to Run the Full System

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Sayan-Mondal2022/enterprise-knowledge-copilot.git
cd enterprise-knowledge-copilot
```

### 2️⃣ Start All Services

```bash
docker-compose up --build
```

## 📚 Detailed Documentation

### 📦 Endee Vector Database Service  
👉 [README-Endee-Service.md](./Endee-service/README.md)

### 🧠 LangChain RAG Service  
👉 [README-LangChain-Service.md](./Langchain-service/README.md)

## Acknowledgement

> WIll be adding this by tomorrow

## 👨‍💻 Author

**Sayan Mondal**  
AI & ML Engineer | Full-Stack Developer  
🔗 GitHub: https://github.com/Sayan-Mondal2022
