import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useTokenStore = defineStore('token', () => {
  const token = ref(localStorage.getItem('auth_token') || null);

  const setToken = (newToken) => {
    token.value = newToken;
    localStorage.setItem('auth_token', newToken);
  };

  const deleteToken = () => {
    token.value = null;
    localStorage.removeItem('auth_token');
  };

  return { token, setToken, deleteToken };
});
