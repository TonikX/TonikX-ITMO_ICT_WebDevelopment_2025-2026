import { ref } from "vue";

export const isLoggedIn = ref(!!localStorage.getItem("auth_token"));

export function login(token) {
  localStorage.setItem("auth_token", token);
  isLoggedIn.value = true;
}

export function logout() {
  localStorage.removeItem("auth_token");
  isLoggedIn.value = false;
}