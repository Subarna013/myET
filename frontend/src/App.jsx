import React, { useState, useEffect } from "react";
import Login from "./Login.jsx";
import NewsFeed from "./NewsFeed.jsx";

function App() {

  const [user, setUser] = useState(null);

  // -----------------------------
  // LOAD USER FROM STORAGE
  // -----------------------------
  useEffect(() => {
    const savedUser = localStorage.getItem("user_id");

    if (savedUser && savedUser !== "undefined" && savedUser !== "null") {
      setUser(Number(savedUser)); // 🔥 ensure it's a number
    }
  }, []);

  // -----------------------------
  // HANDLE LOGIN
  // -----------------------------
  const handleSetUser = (userId) => {
    const id = Number(userId); // 🔥 ensure number

    setUser(id);
    localStorage.setItem("user_id", id);
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
