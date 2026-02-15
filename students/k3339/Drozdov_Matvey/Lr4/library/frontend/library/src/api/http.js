import axios from "axios";
import { useAuthStore } from "@/stores/auth";

const API_URL = "http://127.0.0.1:8000";

export const http = axios.create({
  baseURL: API_URL,
});

http.interceptors.request.use((config) => {
  const auth = useAuthStore();
  if (auth.token) {
    config.headers.Authorization = `Token ${auth.token}`;
  }
  return config;
});