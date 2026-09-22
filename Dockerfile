FROM python:3.11-slim

WORKDIR /app

# System deps needed for sentence-transformers / chromadb
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

# Use shell form so $PORT (set by Render) is expanded at runtime
CMD streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0
