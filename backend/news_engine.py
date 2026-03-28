import requests
import xml.etree.ElementTree as ET

def fetch_news(query):

    try:
        # convert list → string
        if isinstance(query, list):
            query = " ".join(query)

        url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            print("RSS error:", response.status_code)
            return []

        root = ET.fromstring(response.content)

        articles = []

        for item in root.findall(".//item")[:10]:
            articles.append({
                "title": item.find("title").text,
                "description": item.find("description").text,
                "url": item.find("link").text
            })

        return articles

    except Exception as e:
        print("RSS ERROR:", str(e))
        return []
