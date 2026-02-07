from langchain_text_splitters import RecursiveCharacterTextSplitter

# Split the documents into smaller chunks
def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    split_docs = text_splitter.split_documents(minimal_docs)
    return split_docs