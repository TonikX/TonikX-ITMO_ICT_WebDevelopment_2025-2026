import axios from "axios";

const apiBaseURL = "http://127.0.0.1:8000/api/auth/";

export default {
  namespaced: true,
  state: {
    token: localStorage.getItem('token') || null,
    user: null,
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
      localStorage.setItem('token', token);
    },
    setUser(state, user) {
      state.user = user;
    },
    clearAuthData(state) {
      state.token = null;
      state.user = null;
      localStorage.removeItem('token');
    },
  },
  actions: {
    async register(_, userData) {
      await axios.post(apiBaseURL + "users/", userData);
    },
    async login({ commit }, credentials) {
      const response = await axios.post(apiBaseURL + "token/login/", credentials);
      commit("setToken", response.data.auth_token);
    },
    async logout({ commit }) {
      await axios.post(apiBaseURL + "token/logout/", {
        headers: {
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      });
      commit("clearAuthData");
    },
    async getProfile({ commit, state }) {
      if (!state.token) return;
      const response = await axios.get(apiBaseURL + "users/me/", {
        headers: {
          Authorization: `Token ${state.token}`,
        },
      });
      console.log("Получен профиль:", response.data);
      commit("setUser", response.data);
    },
    async logout({ commit }) {
      commit('clearAuthData');
    },
    async updateProfile({ state, dispatch }, userData) {
      console.log("Отправка данных для обновления профиля:", userData);

      if (userData.email && userData.email !== state.user. email) {
        await axios. patch(
          apiBaseURL + "users/me/",
          { email: userData.email },
          {
            headers: {
              Authorization: `Token ${state.token}`,
            },
          }
        );
        console.log("Email обновлён");
      }

      if (userData.username && userData.username !== state.user.username) {
        await axios.post(
          apiBaseURL + "users/set_username/",
          {
            current_password: userData.current_password,
            new_username: userData.username
          },
          {
            headers: {
              Authorization: `Token ${state.token}`,
            },
          }
        );
        console.log("Username обновлён");
      }

      await dispatch("getProfile");
    },
    async changePassword({ state }, passwords) {
      console.log("Смена пароля")
      await axios.post(apiBaseURL + "users/set_password/", passwords, {
        headers: {
          Authorization: `Token ${state.token}`,
        },
      });
    },
  },
};