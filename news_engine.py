import requests
import streamlit as st
from config import NEWS_API_KEY

@st.cache_data(ttl=300)
def fetch_news(query):

    if isinstance(query, list):
        query = " OR ".join(query)

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 20,
        "apiKey": NEWS_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=5)

        if response.status_code != 200:
            return []

        data = response.json()

        articles = []

        for a in data.get("articles", []):
            if not a.get("title"):
                continue

            articles.append({
                "title": a["title"],
                "description": a.get("description"),
                "url": a["url"]
            })

        return articles[:20]

    except:
        return []