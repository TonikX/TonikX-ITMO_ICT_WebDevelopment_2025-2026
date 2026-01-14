// simple auth helper: login, logout, tokens in localStorage, refresh
import api from "./api";

const ACCESS_KEY = "access_token";
const REFRESH_KEY = "refresh_token";

function saveTokens({ access, refresh }) {
  if (access) localStorage.setItem(ACCESS_KEY, access);
  if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
}

export default {
  async login(username, password) {
    const res = await api.post("api/token/", { username, password });
    // response expected: { access: "...", refresh: "..." }
    saveTokens(res.data);
    return res.data;
  },

  logout() {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
    // optionally notify server / revoke token if endpoint exists
  },

  getAccessToken() {
    return localStorage.getItem(ACCESS_KEY);
  },

  getRefreshToken() {
    return localStorage.getItem(REFRESH_KEY);
  },

  isAuthenticated() {
    return !!localStorage.getItem(ACCESS_KEY);
  },

  async refreshToken() {
    const refresh = this.getRefreshToken();
    if (!refresh) throw new Error("No refresh token");
    const res = await api.post("api/token/refresh/", { refresh });
    // { access: "..." }
    if (res.data && res.data.access) {
      localStorage.setItem(ACCESS_KEY, res.data.access);
      return res.data.access;
    }
    throw new Error("Refresh failed");
  },

  // optional helper to decode JWT payload (no dependency)
  decodeToken(token) {
    if (!token) return null;
    try {
      const payload = token.split(".")[1];
      const json = atob(payload.replace(/-/g, "+").replace(/_/g, "/"));
      return JSON.parse(decodeURIComponent(escape(json)));
    } catch {
      return null;
    }
  }
};