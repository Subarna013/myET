import React, { useState } from "react";
import { signup, login } from "./api";

function Login({ setUser }) {

  const [mode, setMode] = useState("login");

  const [form, setForm] = useState({
    name: "",
    phone: "",
    password: "",
    persona: "Student",
    interests: ""
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // -----------------------------
  // HANDLE CHANGE
  // -----------------------------
  const handleChange = (key, value) => {
    setForm({ ...form, [key]: value });
  };

  // -----------------------------
  // SIGNUP
  // -----------------------------
  const handleSignup = async () => {
    try {
      setLoading(true);
      setError("");

      // ✅ SAFE SPLIT (handles empty input also)
      const interestsArray = form.interests
        ? form.interests.split(",").map(i => i.trim())
        : [];

      const res = await signup({
        ...form,
        interests: interestsArray
      });

      setUser(res.user_id);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // -----------------------------
  // LOGIN
  // -----------------------------
  const handleLogin = async () => {
    try {
      setLoading(true);
      setError("");

      const res = await login({
        phone: form.phone,
        password: form.password
      });

      setUser(res.user_id);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "auto" }}>

      <h2>{mode === "login" ? "Login" : "Signup"}</h2>

      {/* Toggle */}
      <button onClick={() => setMode(mode === "login" ? "signup" : "login")}>
        Switch to {mode === "login" ? "Signup" : "Login"}
      </button>

      {/* Inputs */}
      {mode === "signup" && (
        <input
          placeholder="Name"
          value={form.name}
          onChange={e => handleChange("name", e.target.value)}
        />
      )}

      <input
        placeholder="Phone"
        value={form.phone}
        onChange={e => handleChange("phone", e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        value={form.password}
        onChange={e => handleChange("password", e.target.value)}
      />

      {mode === "signup" && (
        <>
          <select
            value={form.persona}
            onChange={e => handleChange("persona", e.target.value)}
          >
            <option>Student</option>
            <option>Startup Founder</option>
            <option>Investor</option>
            <option>Executive</option>
          </select>

          <input
            placeholder="Interests (comma separated)"
            value={form.interests}
            onChange={e => handleChange("interests", e.target.value)}
          />
        </>
      )}

      {/* Error */}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Button */}
      <button
        onClick={mode === "login" ? handleLogin : handleSignup}
        disabled={loading}
      >
        {loading ? "Please wait..." : mode === "login" ? "Login" : "Signup"}
      </button>

    </div>
  );
}

export default Login;
