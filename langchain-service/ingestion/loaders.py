import os
import frontmatter
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_core.documents import Document

# Function to load PDF files from a specified directory
def load_pdf(file_path):
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
def load_textFile(file_path):
    if not os.path.isdir(file_path):
        print(f"Error: The provided path '{file_path}' is not a directory.")
        return []

    try:
        loader = DirectoryLoader(
            file_path,
            glob="**/*.md",           
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        )

        docs = loader.load()
        return docs
    
    except Exception as e:
        print(f"Failed to load PDFs: {e}")
        return []

# This will be the Function to load MARKDOWN FILES
def load_markdown(file_path):
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