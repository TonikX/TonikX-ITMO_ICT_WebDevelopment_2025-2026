import { defineStore } from 'pinia'
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token'),
  }),
  actions: {
    async login(credentials) {
      delete axios.defaults.headers.common['Authorization'];
      const response = await axios.post('http://localhost:8000/auth/token/login/', credentials);
      this.token = response.data.auth_token;
      localStorage.setItem('token', response.data.auth_token);
      const user = await axios.get('http://localhost:8000/auth/users/me/', {headers: {"Authorization": `Token ${localStorage.getItem('token')}`}})
      //console.log(user.data.id)
      const user_data = await axios.get(`http://localhost:8000/core/users/${user.data.id}`)
      //console.log(user_data.data)
      localStorage.setItem('is_superuser', user_data.data.is_superuser);
      this.isAuthenticated = true;
    },
    async register(userData) {
      delete axios.defaults.headers.common['Authorization'];
      return await axios.post('http://localhost:8000/auth/users/', userData);
    },
    async logout() {
      //console.log(localStorage.getItem('token'));
      axios.defaults.headers.common['Authorization'] = `Token ${this.token}`;
      const response = await axios.post('http://localhost:8000/auth/token/logout/');
      delete axios.defaults.headers.common['Authorization'];
      this.isAuthenticated = false;
      localStorage.removeItem('token');
      localStorage.removeItem('is_superuser');
    }
  }
});