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

        for item in root.findall(".//item"):
            title = item.find("title").text
            link = item.find("link").text
            desc = item.find("description").text

            articles.append({
                "title": title,
                "description": desc,
                "url": link
            })

        return articles[:10]

    except Exception as e:
        print("RSS ERROR:", str(e))
        return []
