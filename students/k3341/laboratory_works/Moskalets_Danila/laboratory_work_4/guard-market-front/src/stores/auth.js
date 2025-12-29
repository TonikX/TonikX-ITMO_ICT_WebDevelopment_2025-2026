import { defineStore } from 'pinia'
import apiClient from '@/api'
import router from '@/router'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: JSON.parse(localStorage.getItem('user')) || null,
        accessToken: localStorage.getItem('access_token') || null,
        refreshToken: localStorage.getItem('refresh_token') || null,
        isLoading: false,
        error: null
    }),

    getters: {
        isAuthenticated: (state) => !!state.accessToken,
        isAdmin: (state) => state.user?.is_staff || false,
        hasCompany: (state) => {
            const user = state.user
            if (!user) return false

            // Проверяем security_companies как объект (из вашего примера)
            if (user.security_companies && typeof user.security_companies === 'object') {
                return !!user.security_companies.id // Есть ID компании
            }

            return false
        },
        // Новый геттер для получения объекта компании
        company: (state) => {
            const user = state.user
            if (!user) return null

            if (user.security_companies && typeof user.security_companies === 'object' && user.security_companies.id) {
                return user.security_companies
            }

            return null
        }
    },

    actions: {
        async login(credentials) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.post('auth/jwt/create/', credentials)

                this.accessToken = response.data.access
                this.refreshToken = response.data.refresh

                localStorage.setItem('access_token', response.data.access)
                localStorage.setItem('refresh_token', response.data.refresh)

                // Получаем данные пользователя
                await this.fetchUser()

                router.push('/')
            } catch (error) {
                if (error.response?.status === 401) {
                    this.error = 'Неверный email или пароль'
                } else if (error.response?.data?.detail) {
                    this.error = error.response.data.detail
                } else if (error.response?.data) {
                    const errors = error.response.data
                    if (typeof errors === 'object') {
                        const errorMessages = []
                        for (const [field, messages] of Object.entries(errors)) {
                            if (Array.isArray(messages)) {
                                errorMessages.push(...messages.map(msg => `${field}: ${msg}`))
                            } else {
                                errorMessages.push(`${field}: ${messages}`)
                            }
                        }
                        this.error = errorMessages.join(', ')
                    } else {
                        this.error = 'Ошибка входа'
                    }
                } else {
                    this.error = 'Ошибка соединения с сервером'
                }

                console.error('Login error:', error)
            } finally {
                this.isLoading = false
            }
        },

        async register(userData) {
            this.isLoading = true
            this.error = null

            try {
                await apiClient.post('auth/users/', userData)

                await this.login({
                    email: userData.email,
                    password: userData.password
                })
            } catch (error) {
                this.error = error.response?.data || 'Ошибка регистрации'
                throw error
            } finally {
                this.isLoading = false
            }
        },

        async fetchUser() {
            try {
                const response = await apiClient.get('users/me/')
                this.user = response.data
                localStorage.setItem('user', JSON.stringify(response.data))
                return response.data
            } catch (error) {
                console.error('Error fetching user:', error)

                // Если не удалось получить пользователя, разлогиниваем
                if (error.response?.status === 401) {
                    this.logout()
                }
                throw error
            }
        },

        async updateProfile(userData) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.put('auth/users/me/', userData)
                this.user = response.data
                localStorage.setItem('user', JSON.stringify(response.data))
                return response.data
            } catch (error) {
                console.error('Update profile error:', error)

                if (error.response?.data) {
                    this.error = error.response.data.detail || 'Ошибка обновления профиля'
                } else {
                    this.error = 'Ошибка обновления профиля'
                }
                throw error
            } finally {
                this.isLoading = false
            }
        },

        logout() {
            this.user = null
            this.accessToken = null
            this.refreshToken = null
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
            localStorage.removeItem('user')
            router.push('/login')
        },

        initialize() {
            if (this.accessToken) {
                this.fetchUser()
            }
        }
    }
})