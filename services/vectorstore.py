from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


def chunk_text(docs):
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return text_splitter.split_documents(docs)


def init_faiss_store(docs):
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(docs, embeddings)
