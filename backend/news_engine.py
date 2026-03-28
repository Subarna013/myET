import requests
import os

# get API key from environment
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(query):
    """
    Fetch news articles from NewsAPI
    """

    # 🔥 SAFETY: check API key
    if not NEWS_API_KEY:
        print("ERROR: NEWS_API_KEY not set")
        return []

    # convert list → query string
    if isinstance(query, list):
        query = " OR ".join(query)

    url = "https://newsapi.org/v2/top-headlines"

    params = {
    "country": "us",
    "category": "business",
    "apiKey": NEWS_API_KEY
    }
    try:
        response = requests.get(url, params=params, timeout=5)

        if response.status_code != 200:
            print("News API error:", response.text)
            return []

        data = response.json()

        articles = []

        for a in data.get("articles", []):
            title = a.get("title")
            desc = a.get("description")

            if not title:
                continue

            articles.append({
                "title": title,
                "description": desc,
                "url": a.get("url")
            })

        return articles

    except Exception as e:
        print("Error fetching news:", str(e))
        return []
