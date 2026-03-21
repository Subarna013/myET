import streamlit as st
from models import init_db, create_user
from profiler import Profiler
from recommender import get_personalized_feed
from models import log_interaction

init_db()

st.title("🧠 My ET — Personalized Newsroom")

# -----------------------------
# USER CREATION
# -----------------------------
if "user_id" not in st.session_state:

    persona = st.selectbox(
        "Who are you?",
        ["Student", "Startup Founder", "Investor", "Executive"]
    )

    if st.button("Create My Newsroom"):

        user_id = create_user(persona)

        st.session_state.user_id = user_id
        st.session_state.persona = persona

        st.success("Account created!")

# -----------------------------
# LOAD USER
# -----------------------------
if "user_id" in st.session_state:

    user_id = st.session_state.user_id
    persona = st.session_state.persona

    profiler = Profiler(user_id, persona)

    top_interests = profiler.get_top_interests()

    st.subheader("🎯 Your Interests")
    st.write(top_interests)

    st.subheader("📰 Your News Feed")

    articles = get_personalized_feed(top_interests or ["business"])

    for idx, article in enumerate(articles):

        st.markdown(f"### {article['title']}")
        st.write(article.get("description", ""))

        if st.button(f"Read {idx}"):

            log_interaction(user_id, article["title"])

            for topic in top_interests:
                if topic in article["title"].lower():
                    profiler.update_interest(topic)

            st.success("Learning your preference...")