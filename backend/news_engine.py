import requests
import os

# get API key from environment (Render)
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def fetch_news(query):
    """
    Fetch news articles from NewsAPI based on query/interests
    """

    # convert list → query string
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

        # API error handling
        if response.status_code != 200:
            print("News API error:", response.text)
            return []

        data = response.json()

        articles = []

        for a in data.get("articles", []):

            title = a.get("title")
            desc = a.get("description")

            # skip weak / low-quality articles
            if not title or len(title) < 20:
                continue

            articles.append({
                "title": title,
                "description": desc,
                "url": a.get("url")
            })

        return articles[:20]

    except Exception as e:
        print("Error fetching news:", str(e))
        return []