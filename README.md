# 🧠 AI Research Assistant

A multi-agent research assistant that answers questions using **your uploaded
documents (RAG)** combined with **live web search**, and exposes document
search as a tool through a **custom MCP server**.

---

## ✨ Features

- 📄 Upload a PDF and it's chunked, embedded, and stored in a vector database (ChromaDB)
- 🔍 Ask a question → the assistant retrieves relevant chunks from your document AND searches the live web
- 🧩 A LangGraph pipeline (Document Agent → Web Agent → Answer Agent) combines both sources into one answer
- 🔌 A custom **MCP server** exposes your document knowledge base as a tool that any MCP client (e.g. Claude Desktop) can call
- ⚡ REST API (FastAPI) available for programmatic access
- 🎨 Streamlit chat interface
- 🐳 Fully containerized with Docker

---

## 🛠️ Tech Stack

| Layer              | Tool                              |
|---------------------|------------------------------------|
| Orchestration        | LangGraph                        |
| LLM                  | Groq (`openai/gpt-oss-120b`)     |
| Vector DB (RAG)       | ChromaDB                         |
| Embeddings            | sentence-transformers (local, free) |
| Web Search             | Tavily API                       |
| Tool Protocol           | MCP (Model Context Protocol)     |
| Backend API               | FastAPI                          |
| Frontend                    | Streamlit                        |
| Containerization              | Docker                           |
| Deployment                       | Render                           |

---

## 📂 Project Structure

```
.
├── app.py              # Streamlit chat UI
├── api.py               # FastAPI REST API
├── backend.py            # LangGraph pipeline (3 agents)
├── rag.py                 # PDF chunking, embeddings, ChromaDB
├── tools/
│   └── web_search.py       # Tavily web search tool
├── mcp_server/
│   └── server.py             # Custom MCP server (document search tool)
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ How It Works

1. User uploads a PDF → `rag.py` extracts text, splits it into chunks, embeds
   each chunk with a local sentence-transformer model, and stores them in
   ChromaDB.
2. User asks a question → the LangGraph pipeline in `backend.py` runs:
   - **Document Agent** — retrieves the most relevant chunks from ChromaDB
   - **Web Agent** — searches the live web using Tavily
   - **Answer Agent** — combines both contexts and generates a final answer
     using the LLM
3. The same document search logic is also exposed as an **MCP tool**
   (`search_my_documents`) via `mcp_server/server.py`, so external MCP
   clients like Claude Desktop can query your documents directly.

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Add your API keys

Create a `.env` file (copy `.env.example`) and fill in:

```
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. Run the Streamlit app

```bash
streamlit run app.py
```

### 4. (Optional) Run the FastAPI backend

```bash
uvicorn api:app --reload
```

### 5. (Optional) Run the MCP server

```bash
python mcp_server/server.py
```

To connect it to Claude Desktop, add this to your
`claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "doc-search": {
      "command": "python",
      "args": ["/absolute/path/to/mcp_server/server.py"]
    }
  }
}
```

---

## 🐳 Run with Docker

```bash
docker build -t ai-research-assistant .
docker run -p 8501:8501 --env-file .env ai-research-assistant
```

---

## 📄 License

Open for personal and educational use.
