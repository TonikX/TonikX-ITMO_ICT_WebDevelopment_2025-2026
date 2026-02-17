import http from "./http";
import { EP } from "./endpoints";

export function isAuthed() {
  return !!localStorage.getItem("auth_token");
}

export async function login(username, password) {
  const res = await http.post(EP.login, { username, password });
  localStorage.setItem("auth_token", res.data.auth_token);
  return res.data;
}

export function logout() {
  localStorage.removeItem("auth_token");
}

export async function register(username, password, re_password, email = "") {
  const payload = { username, password, re_password };
  if (email) payload.email = email;
  const res = await http.post(EP.register, payload);
  return res.data;
}
