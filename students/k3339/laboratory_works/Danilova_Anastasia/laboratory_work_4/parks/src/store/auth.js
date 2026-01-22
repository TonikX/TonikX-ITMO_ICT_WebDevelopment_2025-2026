import { defineStore } from "pinia";
import { getCurrentUser } from "@/services/authService";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token"),
    user: null,
    isLoading: false,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    setToken(token) {
      this.token = token;
      localStorage.setItem("token", token);
    },

    setUser(user) {
      this.user = user;
    },

    updateUser(updatedUserData) {
      if (this.user) {
        this.user = { ...this.user, ...updatedUserData };
      }
    },

    async fetchUser() {
      if (!this.token) return;

      this.isLoading = true;
      try {
        const user = await getCurrentUser(this.token);
        this.user = user;
      } catch (err) {
        this.logout();
      } finally {
        this.isLoading = false;
      }
    },

    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem("token");
    },
  },
});
