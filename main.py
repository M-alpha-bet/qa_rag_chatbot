import streamlit as st
import time
from services.news import fetch_crypto_news, load_and_preprocess
from services.vectorstore import chunk_text, init_faiss_store
from services.qa import answer_query


# --- TYPEWRITER EFFECT ---
def typewriter(text, delay=0.03, by="word"):
    container = st.empty()
    output = ""
    parts = text.split(" ") if by == "word" else list(text)
    for part in parts:
        output += part + (" " if by == "word" else "")
        container.markdown(output + "▌")  # cursor effect
        time.sleep(delay)
    container.markdown(output)  # final text


# --- PAGE CONFIG ---
st.set_page_config(page_title="Crypto QA Chatbot",
                   page_icon="💬", layout="centered")
st.title("💬 Crypto QA Chatbot")
st.markdown("""
Welcome! This chatbot answers questions about cryptocurrency using AI + my context(an API call to cryptopanic fetching news data).  
            
This is a demo project, the context can be a dedicated knowledge base to your own company documents etc.

It uses **LangChain**, **Faiss** (vector DB), and **OpenAI** to fetch relevant crypto info 
and provide intelligent answers.
""")


# --- INIT DATASTORE ---
def init_store():
    fetch_crypto_news()
    articles = load_and_preprocess()
    chunks = chunk_text(articles)
    return init_faiss_store(chunks)


if "vectorstore" not in st.session_state:
    with st.spinner("Loading knowledge base..."):
        st.session_state.vectorstore = init_store()

# --- REFRESH BUTTON ---
if st.button("🔄 Refresh News"):
    with st.spinner("Refreshing knowledge base..."):
        st.session_state.vectorstore = init_store()
    st.success("News updated!")


# --- INIT CHAT HISTORY ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# --- DISPLAY CHAT HISTORY ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])


# --- CHAT INPUT ---
if prompt := st.chat_input("Ask me anything about crypto..."):
    # Save + display user message
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            response = answer_query(st.session_state.vectorstore, prompt)

        # stream with typewriter effect
        typewriter(response, delay=0.01, by="letter")

    # Save assistant reply
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response})
