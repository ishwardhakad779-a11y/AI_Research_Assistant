import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph

from rag import retrieve
from tools.web_search import web_search

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.4,
)


class ResearchState(TypedDict):
    question: str
    doc_context: str
    web_context: str
    answer: str


# ------------------------------------------------------------
# Node 1: Document Agent (RAG)
# ------------------------------------------------------------
def document_agent(state: ResearchState):
    context = retrieve(state["question"])
    return {"doc_context": context}


# ------------------------------------------------------------
# Node 2: Web Search Agent
# ------------------------------------------------------------
def web_agent(state: ResearchState):
    results = web_search(state["question"])
    return {"web_context": results}


# ------------------------------------------------------------
# Node 3: Answer Agent
# ------------------------------------------------------------
def answer_agent(state: ResearchState):
    no_docs = "No documents have been uploaded" in state["doc_context"]

    prompt = f"""
You are a research assistant. Answer the user's question using the
context below. Prefer the document context if it directly answers
the question. Use the web context for extra or missing information.

IMPORTANT: If no document has been uploaded (see note below) and the
question refers to a specific unnamed person/entity (e.g. "this person",
"the candidate"), the web search results are NOT about that person and
must be ignored. In that case, simply tell the user no document has been
uploaded yet, instead of answering from unrelated web results.

Question: {state["question"]}

Document context:
{state["doc_context"]}
{"(NOTE: no document has been uploaded yet)" if no_docs else ""}

Web context:
{state["web_context"]}

Give a clear, concise answer. Mention whether the answer came from
the uploaded document, the web, or both.
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    return {"answer": response.content.strip()}


# ------------------------------------------------------------
# Graph: straight line, no loops (same pattern as TripMate AI)
# ------------------------------------------------------------
builder = StateGraph(ResearchState)

builder.add_node("document", document_agent)
builder.add_node("web", web_agent)
builder.add_node("answer", answer_agent)

builder.add_edge(START, "document")
builder.add_edge("document", "web")
builder.add_edge("web", "answer")
builder.add_edge("answer", END)

graph = builder.compile()


def ask_question(question: str) -> dict:
    result = graph.invoke(
        {
            "question": question,
            "doc_context": "",
            "web_context": "",
            "answer": "",
        }
    )
    return result