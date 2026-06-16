import api from './api'

export interface LoginCredentials {
    username: string
    password: string
}

export interface RegisterData {
    username: string
    email: string
    password: string
    re_password: string
}

export interface User {
    id: number
    username: string
    email: string
}

export const authService = {
    async login(credentials: LoginCredentials) {
        const response = await api.post('http://127.0.0.1:8003/api/auth/token/login/', credentials)
        const token = response.data.auth_token
        localStorage.setItem('auth_token', token)
        return token
    },

    async logout() {
        try {
            await api.post('http://127.0.0.1:8003/api/auth/token/logout/')
        } finally {
            localStorage.removeItem('auth_token')
        }
    },

    async register(data: RegisterData) {
        const response = await api.post('http://127.0.0.1:8003/api/auth/users/', data)
        return response.data
    },

    async getCurrentUser(): Promise<User> {
        const response = await api.get('http://127.0.0.1:8003/api/auth/users/me/')
        return response.data
    },

    isAuthenticated(): boolean {
        return !!localStorage.getItem('auth_token')
    },
}
