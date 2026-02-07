from rag.embeddings import load_embeddingModel, sparse_encoder

embeddingModel = load_embeddingModel()

def vectorize_single_index(chunks):
    start_idx = 6000
    documents = []

    for id, chunk in enumerate(chunks):
        source = chunk.metadata.get('source', "")
        title = chunk.metadata.get("title", "")
        description = chunk.metadata.get("description", "")
        text = chunk.page_content
        embedding = embeddingModel.encode(text).tolist()

        data = {
            "id": id + start_idx,
            "vector": embedding,
            "meta": {
                "title": title,
                "description": description,
                "source": source,
                "text": text
            }
        }
        documents.append(data)
    return documents


def vectorize_hybrid_index(chunks):
    start_idx = 6000
    documents = []
    skipped = 0

    for id, chunk in enumerate(chunks):
        source = chunk.metadata.get('source', "")
        title = chunk.metadata.get("title", "")
        description = chunk.metadata.get("description", "")
        text = chunk.page_content

        # Vector Embeddings 
        embedding = embeddingModel.encode(text).tolist()
        if len(embedding) != embeddingModel.get_sentence_embedding_dimension():
            skipped += 1
            continue

        # Sparse Indices and Values for Hybrid Search
        sparse_indices, sparse_values = sparse_encoder(text)
        if len(sparse_indices) != len(sparse_values):
            skipped += 1
            continue

        data = {
            "id": id + start_idx,
            "vector": embedding,
            "sparse_indices": sparse_indices,
            "sparse_values": sparse_values,
            "meta": {
                "title": title,
                "description": description,
                "source": source,
                "text": text
            }
        }
        documents.append(data)

    return documents