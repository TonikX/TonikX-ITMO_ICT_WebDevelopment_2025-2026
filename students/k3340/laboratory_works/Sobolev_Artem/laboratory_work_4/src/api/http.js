import axios from "axios";

const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

let accessToken = null;

const savedToken = localStorage.getItem("token");
if (savedToken) {
  accessToken = savedToken;
}

export function setTokens({ token, refreshToken }) {
  accessToken = token;
  localStorage.setItem("refreshToken", refreshToken);
  localStorage.setItem("token", token);
}

export function clearTokens() {
  accessToken = null;
  localStorage.removeItem("refreshToken");
  localStorage.removeItem("token");
  sessionStorage.removeItem("refreshToken");
  sessionStorage.removeItem("token");
}

http.interceptors.request.use(cfg => {
  if (accessToken) {
    cfg.headers.Authorization = `Bearer ${accessToken}`;
  }
  return cfg;
});

let isRefreshing = false;
let queue = [];

http.interceptors.response.use(
  res => res,
  async err => {
    const original = err.config;

    if (err.response?.status !== 401 || original._retry) {
      return Promise.reject(err);
    }

    const refreshToken = localStorage.getItem("refreshToken");
    if (!refreshToken) {
      clearTokens();
      return Promise.reject(err);
    }

    original._retry = true;

    if (isRefreshing) {
      return new Promise(resolve => {
        queue.push(() => resolve(http(original)));
      });
    }

    isRefreshing = true;

    try {
      const res = await http.get(`/auth/refresh/token?token=${refreshToken}`);

      const newTokens = res.data.payload;
      setTokens({
        token: newTokens.token,
        refreshToken: newTokens.refreshToken
      });

      queue.forEach(cb => cb());
      queue = [];

      return http(original);

    } catch (e) {
      clearTokens();

      if (!window.location.pathname.includes('/sign')) {
        window.location.href = '/sign';
      }

      return Promise.reject(e);
    } finally {
      isRefreshing = false;
    }
  }
);

export default http;
