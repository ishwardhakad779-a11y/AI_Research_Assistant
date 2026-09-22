import tempfile

import streamlit as st

from backend import ask_question
from rag import add_document

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 AI Research Assistant")
st.caption("Upload a PDF, then ask questions. Answers use your document + live web search.")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("📄 Upload Document")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file and st.button("Add to Knowledge Base"):
        with st.spinner("Processing document..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            chunks_added = add_document(tmp_path, uploaded_file.name)
            st.success(f"Added {chunks_added} chunks from {uploaded_file.name}")

    st.divider()
    st.markdown(
        """
        **How it works:**
        1. Document Agent — searches your uploaded PDFs (RAG)
        2. Web Agent — searches the live web (Tavily)
        3. Answer Agent — combines both into one answer
        """
    )

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if question := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = ask_question(question)
            st.write(result["answer"])

    st.session_state.messages.append(
        {"role": "assistant", "content": result["answer"]}
    )
