import React from "react";
import { useState, useEffect } from "react";
import Login from "./Login.jsx";
import NewsFeed from "./NewsFeed.jsx";

function App() {

  const [user, setUser] = useState(null);

  // -----------------------------
  // LOAD USER FROM STORAGE
  // -----------------------------
  useEffect(() => {
    const savedUser = localStorage.getItem("user_id");
    if (savedUser) {
      setUser(savedUser);
    }
  }, []);

  // -----------------------------
  // HANDLE LOGIN
  // -----------------------------
  const handleSetUser = (userId) => {
    setUser(userId);
    localStorage.setItem("user_id", userId);
  };

  // -----------------------------
  // LOGOUT
  // -----------------------------
  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem("user_id");
  };

  return (
    <div>
      {user ? (
        <NewsFeed user={user} logout={handleLogout} />
      ) : (
        <Login setUser={handleSetUser} />
      )}
    </div>
  );
}

export default App;