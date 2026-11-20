from sentence_transformers import SentenceTransformer
import numpy as np
from pypdf import PdfReader
from io import BytesIO

#loads the  embedding model
embedding_model=SentenceTransformer("all-MiniLM-L6-v2")

# Simple in-memory storage
documents = []
document_vectors = []


def split_text(text, chunk_size=500, overlap=50):
    # divides the extracted text into chunks
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def process_pdf(file_bytes):
    reader = PdfReader(BytesIO(file_bytes))
    # reads text from the pdf
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    chunks = split_text(text)
    if not chunks:
        raise ValueError("No extractable text found in PDF")

    vectors = embedding_model.encode(
        chunks,
        normalize_embeddings=True
    )
    documents.extend(chunks)
    document_vectors.extend(vectors)
    return len(chunks)


def retrieve(query, top_k=3):
    if not documents:
        return []
    # convert the query into embedding
    query_vector = embedding_model.encode(
        query,
        normalize_embeddings=True
    )
    #calculate cosine similarity
    # @ --> matrix multiplication
    scores = np.array(document_vectors) @ query_vector
    top_indices = np.argsort(scores)[::-1][:top_k]

    # argsort return the indices
    #[::-1] reverse
    #[:top_k]

    results = []
    for index in top_indices:
        results.append(documents[index])
    return results
    # return the related chunks
