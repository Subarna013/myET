const BASE_URL = "https://myet.onrender.com";

// -----------------------------
const handleResponse = async (res) => {
  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || data.error || "Something went wrong");
  }

  return data;
};

// -----------------------------
export const signup = async (data) => {
  const res = await fetch(`${BASE_URL}/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  return handleResponse(res);
};

// -----------------------------
export const login = async (data) => {
  const res = await fetch(`${BASE_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  return handleResponse(res);
};

// -----------------------------
export const getFeed = async (user_id) => {
  const res = await fetch(`${BASE_URL}/feed/${user_id}`);
  return handleResponse(res);
};
