import axios from 'axios';
import { AUTH_URL } from './config';

export const login = async (username, password) => {
  const response = await axios.post(`${AUTH_URL}/token/login/`, {
    username,
    password,
  });
  return response.data;
};

export const logout = async (token) => {
  await axios.post(
    `${AUTH_URL}/token/logout/`,
    {},
    {
      headers: { Authorization: `Token ${token}` },
    }
  );
};

export const register = async (username, password, re_password) => {
  const response = await axios.post(`${AUTH_URL}/users/`, {
    username,
    password,
    re_password,
  });
  return response.data;
};

export const getCurrentUser = async (token) => {
  const response = await axios.get(`${AUTH_URL}/users/me/`, {
    headers: { Authorization: `Token ${token}` },
  });
  return response.data;
};

