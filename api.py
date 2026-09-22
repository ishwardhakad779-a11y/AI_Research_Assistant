import shutil
import tempfile

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

from backend import ask_question
from rag import add_document

app = FastAPI(title="AI Research Assistant API")


class QuestionRequest(BaseModel):
    question: str


@app.post("/ask")
def ask(request: QuestionRequest):
    result = ask_question(request.question)
    return {
        "question": request.question,
        "answer": result["answer"],
        "used_document_context": bool(
            result["doc_context"]
            and "No documents" not in result["doc_context"]
        ),
    }


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    chunks_added = add_document(tmp_path, file.filename)

    return {
        "filename": file.filename,
        "chunks_added": chunks_added,
    }


@app.get("/health")
def health():
    return {"status": "ok"}
