import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def search_articles(vectorstore, query, k=3):
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    results = retriever.invoke(query)
    return [doc.page_content for doc in results]


def answer_query(vectorstore, query):
    context = "\n".join(search_articles(vectorstore, query))
    prompt = f"""You are a crypto news assistant. Use the context below to answer the user's question accurately.

Context: {context}

Question: {query} 
Answer:"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content.strip()  # type: ignore
