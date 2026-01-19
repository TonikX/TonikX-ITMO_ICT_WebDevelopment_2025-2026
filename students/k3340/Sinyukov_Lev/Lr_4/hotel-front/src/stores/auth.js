import { defineStore } from "pinia";
import { http } from "@/api/http";
import { endpoints } from "@/api/endpoints";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    loading: false,
    error: null,
  }),

  getters: {
    isAuthed: () => !!localStorage.getItem("access"),
  },

  actions: {
    async login(username, password) {
      this.loading = true;
      this.error = null;

      try {
        const res = await http.post(endpoints.auth.login, { username, password });
        localStorage.setItem("access", res.data.access);
        localStorage.setItem("refresh", res.data.refresh);
        await this.fetchMe();
      } catch (e) {
        this.error = e.response?.data || e.message;
        throw e;
      } finally {
        this.loading = false;
      }
    },

    async register(payload) {
      this.loading = true;
      this.error = null;

      try {
        await http.post(endpoints.auth.register, payload);
      } catch (e) {
        this.error = e.response?.data || e.message;
        throw e;
      } finally {
        this.loading = false;
      }
    },

    async fetchMe() {
      const res = await http.get(endpoints.auth.me);
      this.user = res.data;
    },

    async changePassword(current_password, new_password, re_new_password) {
      await http.post(endpoints.auth.setPassword, {
        current_password,
        new_password,
        re_new_password,
      });
    },

    logout() {
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      this.user = null;
    },
  },
});