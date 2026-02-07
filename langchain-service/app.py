import streamlit as st
import tempfile
import os

# -------------------------------
# DATA INGESTION
from ingestion.loaders import load_markdown, load_pdf
from ingestion.preprocessing import filter_docs
from ingestion.chunking import text_split
from ingestion.vectorize_data import (
    vectorize_single_index,
    vectorize_hybrid_index
)
from ingestion.upsert import (
    upsert_single_index,
    upsert_hybrid_index
)

# -------------------------------
# RAG PIPELINE
from rag.rag_pipeline import (
    single_rag_chain, 
    hybrid_rag_chain
)

# -------------------------------
# PAGE CONFIG
st.set_page_config(
    page_title="GitLab Copilot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 GitLab Copilot")
st.caption("Your internal knowledge assistant")

# -------------------------------
# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []

if "mode" not in st.session_state:
    st.session_state.mode = "Normal"

# -------------------------------
# SIDEBAR
with st.sidebar:
    st.header("⚙️ Settings")

    st.session_state.mode = st.radio(
        "Choose model",
        ["Normal", "Pro"]
    )

    st.divider()

    st.subheader("📄 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF or Markdown files",
        type=["pdf", "md"],
        accept_multiple_files=True
    )

    if st.button("📥 Ingest Documents") and uploaded_files:
        with st.spinner("Processing documents..."):
            all_docs = []

            with tempfile.TemporaryDirectory() as tmpdir:
                for file in uploaded_files:
                    file_path = os.path.join(tmpdir, file.name)
                    with open(file_path, "wb") as f:
                        f.write(file.read())

                # Load documents
                all_docs.extend(load_pdf(tmpdir))
                all_docs.extend(load_markdown(tmpdir))

            # Preprocess → Chunk → Vectorize → Upsert
            minimal_docs = filter_docs(all_docs)
            chunks = text_split(minimal_docs)

            if st.session_state.mode == "Normal":
                vectors = vectorize_single_index(chunks)
                result = upsert_single_index(vectors)
            else:
                vectors = vectorize_hybrid_index(chunks)
                result = upsert_hybrid_index(vectors)

        st.success("✅ Documents ingested successfully")

# -------------------------------
# CHAT DISPLAY
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])  # preserves markdown styling

# -------------------------------
# CHAT INPUT
user_input = st.chat_input("Ask something...")

if user_input:
    # User message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if st.session_state.mode == "Normal":
                response = single_rag_chain.invoke(user_input)
            else:
                response = hybrid_rag_chain.invoke(user_input)

        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
