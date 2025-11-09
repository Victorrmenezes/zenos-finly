import React, { createContext, useContext, useEffect, useState } from 'react';
import { login as apiLogin, logout as apiLogout } from '../api/auth';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Initialize auth state from localStorage tokens/username
  useEffect(() => {
    const access = localStorage.getItem('access');
    const storedUsername = localStorage.getItem('username');
    if (access) {
      setUser(storedUsername ? { username: storedUsername } : { username: null });
    } else {
      setUser(null);
    }
    setLoading(false);
  }, []);

  async function handleLogin(username, password) {
    // Use JWT token endpoint via axios instance
    await apiLogin(username, password);
    // Persist username to show in UI (Navbar/Profile)
    localStorage.setItem('username', username);
    setUser({ username });
  }

  async function handleLogout() {
    try { apiLogout(); } catch (_) {}
    setUser(null);
  }

  const value = { user, loading, handleLogin, handleLogout };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
