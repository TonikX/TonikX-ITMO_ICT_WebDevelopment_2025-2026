import axios from "axios";

const API_URL = "http://127.0.0.1:8000/auth";

export const login = async (username, password) => {
  const response = await axios.post(`${API_URL}/token/login/`, {
    username,
    password,
  });
  return response.data;
};

export const logout = async (token) => {
  return await axios.post(`${API_URL}/token/logout/`, null, {
    headers: { Authorization: `Token ${token}` },
  });
};

export const register = async (username, password) => {
  const response = await axios.post(`${API_URL}/users/`, {
    username,
    password,
  });
  return response.data;
};

export const getCurrentUser = async (token) => {
  const response = await axios.get(`${API_URL}/users/me/`, {
    headers: { Authorization: `Token ${token}` },
  });
  return response.data;
};

export const updateUser = async (userId, userData, token) => {
  const response = await axios.patch(`${API_URL}/users/${userId}/`, userData, {
    headers: { Authorization: `Token ${token}` },
  });
  return response.data;
};

export const changePassword = async (currentPassword, newPassword, token) => {
  const response = await axios.post(
    `${API_URL}/users/set_password/`,
    {
      current_password: currentPassword,
      new_password: newPassword,
    },
    {
      headers: { Authorization: `Token ${token}` },
    }
  );
  return response.data;
};
