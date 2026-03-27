import React from "react";
import { useEffect, useState } from "react";
import { getFeed } from "./api";

function NewsFeed({ user, logout }) {

  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // -----------------------------
  // FETCH NEWS
  // -----------------------------
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError("");

        const res = await getFeed(user);
        setArticles(res.articles || []);

      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [user]);

  // -----------------------------
  // UI
  // -----------------------------
  return (
    <div style={{ maxWidth: "800px", margin: "auto" }}>

      <h2>📰 Your Personalized News</h2>

      <button onClick={logout}>Logout</button>

      {loading && <p>Loading news...</p>}

      {error && <p style={{ color: "red" }}>{error}</p>}

      {!loading && articles.length === 0 && (
        <p>No news available. Try again later.</p>
      )}

      {articles.map((article, index) => (
        <div
          key={index}
          style={{
            borderBottom: "1px solid #ccc",
            padding: "10px",
            marginBottom: "10px"
          }}
        >
          <h3>{article.title}</h3>

          <p>{article.description}</p>

          <a href={article.url} target="_blank" rel="noreferrer">
            Read full article →
          </a>
        </div>
      ))}

    </div>
  );
}

export default NewsFeed;