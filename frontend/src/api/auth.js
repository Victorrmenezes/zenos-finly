// src/api/auth.js
import api from "./axios";

export async function login(username, password) {
  const response = await api.post("/token/", { username, password });
  const { access, refresh } = response.data;
  localStorage.setItem("access", access);
  localStorage.setItem("refresh", refresh);
  return response.data;
}

export function logout() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
}
