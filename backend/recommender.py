from news_engine import fetch_news


# -----------------------------
# SCORE ARTICLE (SAFE)
# -----------------------------
def score_article(article, interests):

    title = (article.get("title") or "").lower()
    description = (article.get("description") or "").lower()

    score = 0

    interests = [i.lower() for i in interests]

    for t in interests:
        if t in title:
            score += 3
        if t in description:
            score += 2

    keywords = ["market", "funding", "growth", "policy", "stock", "startup"]

    for k in keywords:
        if k in title:
            score += 1

    return score


# -----------------------------
# BUILD FEED (SAFE + FALLBACK)
# -----------------------------
def get_personalized_feed(interests):

    # fallback interests
    if not interests:
        interests = ["business", "economy"]

    # fetch news
    articles = fetch_news(interests + ["business"])

    # 🔥 fallback if API fails
    if not articles:
        return [
            {"title": "No live news. Showing fallback.", "description": "", "url": "#"},
            {"title": "Try again later for latest updates.", "description": "", "url": "#"}
        ]

    # score articles
    scored_articles = [(a, score_article(a, interests)) for a in articles]

    scored_articles.sort(key=lambda x: x[1], reverse=True)

    # diversity mix
    top = scored_articles[:7]
    mid = scored_articles[7:15]

    final = top + mid[:3]

    return [a[0] for a in final[:10]]
