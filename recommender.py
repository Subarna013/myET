from news_engine import fetch_news

def score_article(article, interests):

    title = article["title"].lower()
    score = 0

    for t in interests:
        if t in title:
            score += 2

    keywords = ["market", "funding", "growth", "policy"]

    for k in keywords:
        if k in title:
            score += 1

    return score


def get_personalized_feed(interests):

    articles = fetch_news(interests + ["business"])

    scored = [(a, score_article(a, interests)) for a in articles]

    scored.sort(key=lambda x: x[1], reverse=True)

    return [a[0] for a in scored[:10]]