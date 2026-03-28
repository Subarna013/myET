import requests
import os

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

def fetch_news(query):

    if not GNEWS_API_KEY:
        print("NO GNEWS API KEY")
        return []

    try:
        if isinstance(query, list):
            query = " OR ".join(query)

        url = "https://gnews.io/api/v4/search"

        params = {
            "q": query,
            "lang": "en",
            "max": 10,
            "token": GNEWS_API_KEY
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print("GNews error:", response.text)
            return []

        data = response.json()

        articles = []

        for a in data.get("articles", []):
            articles.append({
                "title": a.get("title"),
                "description": a.get("description"),
                "url": a.get("url")
            })

        return articles

    except Exception as e:
        print("Error:", e)
        return []
