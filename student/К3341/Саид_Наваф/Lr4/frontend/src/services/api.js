import axios from "axios";
import auth from "./auth";

const baseURL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const api = axios.create({
  baseURL: baseURL.replace(/\/$/, "") + "/",
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach access token if present
api.interceptors.request.use((config) => {
  const token = auth.getAccessToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Response interceptor to handle 401 by trying token refresh once
let isRefreshing = false;
let refreshQueue = [];

function processQueue(error, token = null) {
  refreshQueue.forEach(prom => {
    if (error) prom.reject(error);
    else prom.resolve(token);
  });
  refreshQueue = [];
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (!originalRequest) return Promise.reject(error);

    // If 401 and not a token endpoint, try refresh once
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      if (isRefreshing) {
        // queue the request until refresh finished
        return new Promise(function(resolve, reject) {
          refreshQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers.Authorization = "Bearer " + token;
            return api(originalRequest);
          })
          .catch((err) => Promise.reject(err));
      }

      isRefreshing = true;
      try {
        const newAccess = await auth.refreshToken();
        processQueue(null, newAccess);
        originalRequest.headers.Authorization = "Bearer " + newAccess;
        return api(originalRequest);
      } catch (err) {
        processQueue(err, null);
        auth.logout();
        // redirect to login page (client-side)
        if (typeof window !== "undefined") window.location = "/login";
        return Promise.reject(err);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default api;