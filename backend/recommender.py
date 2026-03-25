from news_engine import fetch_news


# -----------------------------
# SCORE ARTICLE
# -----------------------------
def score_article(article, interests):

    title = article["title"].lower()
    description = (article.get("description") or "").lower()

    score = 0

    # normalize interests
    interests = [i.lower() for i in interests]

    for t in interests:
        if t in title:
            score += 3
        if t in description:
            score += 2

    # important keywords boost
    keywords = ["market", "funding", "growth", "policy", "stock", "startup"]

    for k in keywords:
        if k in title:
            score += 1

    return score


# -----------------------------
# BUILD FEED (WITH DIVERSITY)
# -----------------------------
def get_personalized_feed(interests):

    if not interests:
        interests = ["business", "economy"]

    articles = fetch_news(interests + ["business"])

    if not articles:
        return []

    scored_articles = [(a, score_article(a, interests)) for a in articles]

    # sort by score
    scored_articles.sort(key=lambda x: x[1], reverse=True)

    # 🔥 diversity: mix top + mid
    top = scored_articles[:7]
    mid = scored_articles[7:15]

    final = top + mid[:3]

    return [a[0] for a in final[:10]]