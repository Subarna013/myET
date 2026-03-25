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
        "pageSize": 30,
        "apiKey": NEWS_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=5)

        if response.status_code != 200:
            return []

        data = response.json()

        articles = []

        for a in data.get("articles", []):

            title = a.get("title")
            desc = a.get("description")

            # skip weak articles
            if not title or len(title) < 20:
                continue

            articles.append({
                "title": title,
                "description": desc,
                "url": a["url"]
            })

        return articles[:20]

    except:
        return []