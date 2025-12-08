// src/auth.js
import { ref } from "vue";

const isAuthenticated = ref(!!localStorage.getItem("auth_token"));
const username = ref(localStorage.getItem("username") || null);
const token = ref(localStorage.getItem("auth_token") || null);

function setAuth(tokenValue, name) {
  if (tokenValue) {
    localStorage.setItem("auth_token", tokenValue);
    token.value = tokenValue;
    if (name) {
      localStorage.setItem("username", name);
      username.value = name;
    }
    isAuthenticated.value = true;
  }
}

function clearAuth() {
  localStorage.removeItem("auth_token");
  localStorage.removeItem("username");
  token.value = null;
  username.value = null;
  isAuthenticated.value = false;
}

export { isAuthenticated, username, token, setAuth, clearAuth };