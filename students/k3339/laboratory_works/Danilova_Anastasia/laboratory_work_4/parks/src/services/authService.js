import axios from "axios";

const API_URL = "http://127.0.0.1:8000/auth/";

export const login = async (email, password) => {
  const response = await axios.post(`${API_URL}token/login/`, {
    email,
    password,
  });
  return response.data;
};

export const logout = async (token) => {
  return await axios.post(`${API_URL}token/logout/`, null, {
    headers: { Authorization: `Token ${token}` },
  });
};

export const register = async (email, password) => {
  const response = await axios.post(`${API_URL}users/`, { email, password });
  return response.data;
};

export const getCurrentUser = async (token) => {
  const response = await axios.get(`${API_URL}users/me/`, {
    headers: { Authorization: `Token ${token}` },
  });
  return response.data;
};
