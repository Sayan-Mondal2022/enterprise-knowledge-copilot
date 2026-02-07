from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import frontmatter
from pathlib import Path
import re
import markdown
from bs4 import BeautifulSoup
import os


# Function to load PDF files from a specified directory
def load_pdf_file(file_path):
    if not os.path.isdir(file_path):
        print(f"Error: The provided path '{file_path}' is not a directory.")
        return []

    try:
        loader = DirectoryLoader(
            file_path,
            glob="*.pdf",
            loader_cls=PyPDFLoader,
            recursive=True,
        )
        documents = loader.load()
        return documents
    except Exception as e:
        print(f"Failed to load PDFs: {e}")
        return []


# Function to load Markdown files from a specified directory
def load_markdown_file(file_path):
    if not os.path.isdir(file_path):
        print(f"Error: The provided path '{file_path}' is not a directory.")
        return []

    loader = DirectoryLoader(
        file_path,
        glob="**/*.md",           
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )

    docs = loader.load()
    return docs

# This will be the Function to load MARKDOWN FILES
def load_md_with_metadata(file_path):
    docs = []

    for file in Path(file_path).rglob("*.md"):
        try:
            post = frontmatter.load(file)
        except Exception as e:
            print(f"Skipping {file}: {e}")
            continue

        docs.append(
            Document(
                page_content=post.content,
                metadata={
                    "title": post.get("title"),
                    "description": post.get("description"),
                    "source": str(file)
                }
            )
        )

    return docs

# Filters documents to only include page_content and source metadata.
def filter_to_minimal_docs(docs):
    minimal_docs = []

    for doc in docs:
        full_path = doc.metadata.get("source", "")
        file_name = os.path.basename(full_path)

        minimal_doc = Document(
            page_content=clean_markdown(doc.page_content),
            metadata={
                "title": doc.metadata.get("title"),
                "description": doc.metadata.get("description"),
                "source": file_name
            }
        )

        minimal_docs.append(minimal_doc)

    return minimal_docs

# Split the documents into smaller chunks
def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    split_docs = text_splitter.split_documents(minimal_docs)
    return split_docs


# Function to clean markdown text
def clean_markdown(md_text: str) -> str:
    try:
        # 1. Remove YAML front matter
        md_text = re.sub(r"^---.*?---", "", md_text, flags=re.DOTALL)

        # 2. Convert markdown → HTML
        html = markdown.markdown(md_text)

        # 3. Parse HTML
        soup = BeautifulSoup(html, "html.parser")

        # 4. Remove unwanted tags
        for tag in soup(["script", "style", "iframe", "img", "table"]):
            tag.decompose()

        # 5. Get text
        text = soup.get_text(separator=" ")

        # 6. Remove markdown links but keep text
        text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)

        # 7. Normalize whitespace
        text = re.sub(r"\n{2,}", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)

        return text.strip()
    
    except Exception:
        return md_text.strip()