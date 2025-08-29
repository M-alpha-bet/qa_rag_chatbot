import os
import json
import re
import html
import requests
from dotenv import load_dotenv
from langchain.schema import Document

load_dotenv()
CRYPTOPANIC_API_KEY = os.getenv("CRYPTOPANIC_API_KEY")


def clean_text(text: str) -> str:
    """Helper function to clean HTML tags and special characters from text."""
    text = html.unescape(text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_crypto_news():
    url = f"https://cryptopanic.com/api/developer/v2/posts/?auth_token={CRYPTOPANIC_API_KEY}&public=true&filter=important"
    response = requests.get(url)
    data = response.json()

    os.makedirs("data", exist_ok=True)
    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return data


def load_and_preprocess():
    with open("data/news.json", "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    print("RAW API RESPONSE:", raw_data)

    if "results" not in raw_data:
        error_msg = raw_data.get("info", "Unknown API error")
        return [Document(
            page_content=f"⚠️ Failed to fetch fresh crypto news.\nReason: {error_msg}",
            metadata={"source": "cryptopanic",
                "status": raw_data.get("status", "error")}
        )]

    docs = []
    for item in raw_data["results"]:
        title = clean_text(item.get("title") or "")
        description = clean_text(item.get("description") or "")
        url = item.get("slug", "")
        id = item.get("id", "")

        text = f"{title}\n{description}\nSource: https://cryptopanic.com/news/{id}/{url}"
        docs.append(Document(page_content=text.strip(),
                             metadata={"id": id, "title": title}))
    return docs
