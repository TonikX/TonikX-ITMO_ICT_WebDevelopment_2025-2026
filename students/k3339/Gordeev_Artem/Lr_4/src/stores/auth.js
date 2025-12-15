import { defineStore } from 'pinia';
import { authApi } from '@/api/axios';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        token: localStorage.getItem('token') || null,
    }),
    getters: {
        isAuthenticated: (state) => !!state.token,
        isManager: (state) => state.user?.role === 'manager' || state.user?.role === 'admin',
        isEditor: (state) => state.user?.role === 'editor' || state.user?.role === 'admin',
    },
    actions: {
        async login(credentials) {
            try {
                const response = await authApi.post('/token/login/', credentials);
                this.token = response.data.auth_token;
                localStorage.setItem('token', this.token);
                await this.fetchUser();
                return true;
            } catch (error) {
                console.error('Login failed:', error);
                throw error;
            }
        },
        async register(userData) {
            try {
                await authApi.post('/users/', userData);
                return true;
            } catch (error) {
                console.error('Registration failed:', error);
                throw error;
            }
        },
        async fetchUser() {
            try {
                const response = await authApi.get('/users/me/');
                this.user = response.data;
            } catch (error) {
                console.error('Fetch user failed:', error);
                this.logout();
            }
        },
        logout() {
            this.token = null;
            this.user = null;
            localStorage.removeItem('token');
        },
    },
});
