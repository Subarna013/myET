from db import get_connection


# -----------------------------
# INIT TABLES
# -----------------------------
def init_db():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        persona TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS interests (
        user_id INT,
        topic TEXT,
        weight FLOAT,
        PRIMARY KEY (user_id, topic)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS interactions (
        id SERIAL PRIMARY KEY,
        user_id INT,
        article_title TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()


# -----------------------------
# USER
# -----------------------------
def create_user(persona):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (persona) VALUES (%s) RETURNING id",
        (persona,)
    )

    user_id = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return user_id


# -----------------------------
# INTERESTS
# -----------------------------
def save_interest(user_id, topic, weight):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO interests (user_id, topic, weight)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id, topic)
        DO UPDATE SET weight = %s
    """, (user_id, topic, weight, weight))

    conn.commit()
    conn.close()


def load_interests(user_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT topic, weight FROM interests
        WHERE user_id = %s
    """, (user_id,))

    data = cur.fetchall()

    conn.close()

    return {t: w for t, w in data}


# -----------------------------
# INTERACTIONS
# -----------------------------
def log_interaction(user_id, title):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO interactions (user_id, article_title)
        VALUES (%s, %s)
    """, (user_id, title))

    conn.commit()
    conn.close()