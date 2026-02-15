import { defineStore } from "pinia";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || "",
    username: localStorage.getItem("username") || "",
  }),

  getters: {
    isLoggedIn: (s) => !!s.token,
  },

  actions: {
    saveToken(token, username) {
      this.token = token;
      this.username = username;
      localStorage.setItem("token", token);
      localStorage.setItem("username", username);
    },

    async login(username, password) {
      const { data } = await axios.post(`${API_URL}/auth/token/login/`, {
        username,
        password,
      });

      this.saveToken(data.auth_token, username);
    },

    async logout() {
      try {
        if (this.token) {
          await axios.post(
            `${API_URL}/auth/token/logout/`,
            {},
            { headers: { Authorization: `Token ${this.token}` } }
          );
        }
      } catch (e) {
        
      } finally {
        this.token = "";
        this.username = "";
        localStorage.removeItem("token");
        localStorage.removeItem("username");
      }
    },
  },
});