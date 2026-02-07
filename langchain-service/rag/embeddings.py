from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch

def load_embeddingModel(model_name = 'all-MiniLM-L6-v2'):
    return SentenceTransformer('all-MiniLM-L6-v2')

def load_tokenizer():
    return AutoTokenizer.from_pretrained("naver/splade-cocondenser-ensembledistil")

def load_sparse_model():
    return AutoModelForMaskedLM.from_pretrained("naver/splade-cocondenser-ensembledistil")

# This is for SPLADE (To compute Sparse Vectors and Indices)
tokenizer = load_tokenizer()
model = load_sparse_model()

def sparse_encoder(text, threshold=0.1):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)

    with torch.no_grad():
        logits = model(**inputs).logits

    # SPLADE pooling
    scores = torch.log1p(torch.relu(logits))
    scores = torch.max(scores, dim=1).values.squeeze()

    indices = []
    values = []

    for idx, score in enumerate(scores):
        if score > threshold:
            indices.append(idx)
            values.append(float(score))

    return indices, values