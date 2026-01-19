import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export const http = axios.create({
  baseURL: API_BASE,
});

// Подставляем access токен в Authorization
http.interceptors.request.use((config) => {
  const access = localStorage.getItem("access");
  if (access) config.headers.Authorization = `Bearer ${access}`;
  return config;
});

// Авто refresh токена при 401
http.interceptors.response.use(
  (resp) => resp,
  async (error) => {
    const original = error.config;

    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;

      const refresh = localStorage.getItem("refresh");
      if (!refresh) throw error;

      const res = await axios.post(`${API_BASE}/auth/jwt/refresh/`, { refresh });

      localStorage.setItem("access", res.data.access);
      original.headers.Authorization = `Bearer ${res.data.access}`;

      return axios(original);
    }

    throw error;
  }
);