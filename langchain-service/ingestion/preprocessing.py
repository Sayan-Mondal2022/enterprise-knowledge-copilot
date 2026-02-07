import os
import re
import markdown
from bs4 import BeautifulSoup
from langchain_core.documents import Document

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

# Filters documents to only include page_content and source metadata.
def filter_docs(docs):
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