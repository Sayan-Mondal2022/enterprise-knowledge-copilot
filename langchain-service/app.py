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
from rag.rag_helper import create_load_dbs

# -------------------------------
# RAG PIPELINE
from rag.rag_pipeline import (
    single_rag_chain, 
    hybrid_rag_chain
)

@st.cache_resource
def startup_logic():
    print("startup_logic executed")
    create_load_dbs()

# -------------------------------
# PAGE CONFIG
st.set_page_config(
    page_title="Enterprise Copilot",
    page_icon="🤖",
    layout="centered"
)

@st.dialog("📖 How to use Enterprise Knowledge Copilot", width="large")
def docs_dialog():
    st.markdown("""
    **Welcome to the Enterprise Knowledge Copilot!** 🤖
    
    This intelligent assistant helps you instantly find answers hidden within your company's internal documentation, policies, and technical guides.

    ### 🔍 Choose Your Search Mode
    * **Normal Mode (Semantic Search):** Best for general questions, summaries, and understanding broad concepts. It searches based on the *meaning* of your query.
    * **Pro Mode (Hybrid Search):** Best for highly technical questions, specific error codes, acronyms, or exact IDs. It combines semantic understanding with exact keyword matching (SPLADE) for maximum precision.

    ### 📥 How to Add Knowledge (Ingestion)
    1. **Select Files:** Use the uploader in the sidebar to choose your documents (`.pdf` or `.md` formats are supported).
    2. **Ingest:** Click **'Ingest Documents'**. The system will automatically read, clean, and securely store the knowledge in our custom vector database.
    3. *Note: The Copilot will only answer based on the documents you have ingested.*

    ### 💡 Tips for Best Results
    * **Be Specific:** Instead of asking *"tell me about leaves"*, ask *"What is the policy for remote work annual leave?"*
    * **Formatting:** You can ask the bot to reply in bullet points, or provide step-by-step instructions.
    * **Verify:** While the Copilot uses Retrieval-Augmented Generation (RAG) to ground its answers in your documents, it is always good practice to double-check critical information.
    """)

# -------------------------------
# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []

if "mode" not in st.session_state:
    st.session_state.mode = "Normal"

if "company_name" not in st.session_state:
    st.session_state.company_name = "Enterprise Inc."

if "bot_name" not in st.session_state:
    st.session_state.bot_name = "Enterprise Copilot"

if "custom_prompt" not in st.session_state:
    st.session_state.custom_prompt = "If a user asks whether they can upload a Document, respond with 'Yes, you can upload a PDF or Markdown Document.'"


@st.dialog("⚙️ Configure Chatbot")
def configure_bot_dialog():
    st.markdown("Customize the assistant's persona and instructions.")
    
    # Input fields pre-filled with current session state values
    new_company = st.text_input("Company Name", value=st.session_state.company_name)
    new_bot = st.text_input("Bot Name", value=st.session_state.bot_name)
    new_prompt = st.text_area(
        "Additional Instructions (Optional)", 
        value=st.session_state.custom_prompt,
        height=100
    )
    
    # Save button
    if st.button("Save Configuration", type="primary", use_container_width=True):
        st.session_state.company_name = new_company
        st.session_state.bot_name = new_bot
        st.session_state.custom_prompt = new_prompt
        st.rerun()

# WELCOME MESSAGE
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h2>👋 Welcome to Enterprise Copilot!</h2>
        <p style="font-size: 1.1rem; color: #555;">Your intelligent assistant for navigating internal enterprise knowledge.</p>
    </div>
    
    **How to get started:**
    1. 📄 **Upload Documents:** Use the sidebar to ingest your PDFs or Markdown files.
    2. ⚙️ **Select Mode:** Choose **Normal** for general queries or **Pro** for technical/keyword-heavy searches.
    3. 💬 **Start Chatting:** Ask your question in the text box below!
    
    ---
    """, unsafe_allow_html=True)
else:
    st.title(f"🤖 {st.session_state.bot_name}")

# -------------------------------
# SIDEBAR
with st.sidebar:
    st.header("⚙️ Settings")

    # --- NEW DOCS SECTION ---
    if st.button("ℹ️ How to use this Copilot", use_container_width=True):
        docs_dialog()
    
    # --- NEW: Button to open Config Dialog ---
    if st.button("🤖 Configure Chatbot", use_container_width=True):
        configure_bot_dialog()

    st.divider()

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

# 1. Show a loading animation and initialize DBs before rendering the input
if "db_initialized" not in st.session_state:
    with st.spinner("Initializing Vector Databases... Please wait."):
        create_load_dbs()
    st.session_state.db_initialized = True

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

            invoke_payload = {
                "input": user_input,
                "company_name": st.session_state.company_name,
                "bot_name": st.session_state.bot_name,
                "custom_prompt": st.session_state.custom_prompt
            }

            if st.session_state.mode == "Normal":
                response = single_rag_chain.invoke(invoke_payload)
            else:
                response = hybrid_rag_chain.invoke(invoke_payload)

        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
