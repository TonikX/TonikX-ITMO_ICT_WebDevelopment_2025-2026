import { AUTH_BASE, axios } from './config'

export const login = (username, password) =>
  axios.post(`${AUTH_BASE}/token/login/`, { username, password }).then(res => res.data)

export const register = (data) =>
  axios.post(`${AUTH_BASE}/users/`, data)

export const getProfile = () =>
  axios.get(`${AUTH_BASE}/users/me/`).then(res => res.data)

export const updateUser = (data) =>
  axios.patch(`${AUTH_BASE}/users/me/`, data).then(r => r.data)

export const setPassword = (data) =>
  axios.post(`${AUTH_BASE}/users/set_password/`, data).then(r => r.data)