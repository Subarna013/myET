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
# BUILD FEED (FINAL FIXED)
# -----------------------------
def get_personalized_feed(interests):

    try:
        # fallback interests
        if not interests:
            interests = ["business", "economy"]

        # fetch news
        articles = fetch_news(interests + ["business"])

        # 🔥 HARD FALLBACK (NEVER EMPTY)
        if not articles:
            return [
                {
                    "title": "⚠️ No live news fetched",
                    "description": "Check API / backend. Showing fallback.",
                    "url": "#"
                },
                {
                    "title": "System working but no articles returned",
                    "description": "Your news source might be empty or blocked.",
                    "url": "#"
                }
            ]

        # score safely
        scored_articles = []
        for a in articles:
            try:
                score = score_article(a, interests)
                scored_articles.append((a, score))
            except:
                continue

        # 🔥 if scoring fails
        if not scored_articles:
            return articles[:5]

        # sort
        scored_articles.sort(key=lambda x: x[1], reverse=True)

        # diversity mix
        top = scored_articles[:7]
        mid = scored_articles[7:15]

        final = top + mid[:3]

        result = [a[0] for a in final[:10]]

        # 🔥 FINAL SAFETY
        if not result:
            return articles[:5]

        return result

    except Exception as e:
        print("RECOMMENDER ERROR:", str(e))

        # 🔥 ULTIMATE FALLBACK
        return [
            {
                "title": "⚠️ System error in recommender",
                "description": str(e),
                "url": "#"
            }
        ]
