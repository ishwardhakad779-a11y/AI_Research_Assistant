import os
import uuid

import chromadb


chroma_client = chromadb.PersistentClient(path="./chroma_store")
collection = chroma_client.get_or_create_collection(name="documents")


def extract_pdf_text(file_path: str) -> str:
    from pypdf import PdfReader

    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return [c.strip() for c in chunks if c.strip()]


def add_document(file_path: str, doc_name: str):
    text = extract_pdf_text(file_path)
    chunks = chunk_text(text)

    if not chunks:
        return 0

    ids = [str(uuid.uuid4()) for _ in chunks]
    metadatas = [{"source": doc_name} for _ in chunks]

   
    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas,
    )

    return len(chunks)


def retrieve(query: str, top_k: int = 5) -> str:
    if collection.count() == 0:
        return "No documents have been uploaded yet."

    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, collection.count()),
    )

    docs = results.get("documents", [[]])[0]

    if not docs:
        return "No relevant information found in the documents."

    return "\n\n---\n\n".join(docs)
