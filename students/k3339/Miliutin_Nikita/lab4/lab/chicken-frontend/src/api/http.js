import axios from "axios";
import { getToken } from "../utils/token";

const API_BASE_URL = "http://localhost:8000";

export const http = axios.create({
  baseURL: API_BASE_URL,
});

http.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

