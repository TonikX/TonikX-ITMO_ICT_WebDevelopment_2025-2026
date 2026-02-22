import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
    state: {
        auth: {
            token: localStorage.getItem('token') || null,
            user: JSON.parse(localStorage.getItem('user')) || null,
            isLoading: false,
            error: null
        }
    },

    mutations: {
        SET_TOKEN(state, token) {
            state.auth.token = token
            localStorage.setItem('token', token)
        },

        SET_USER(state, user) {
            state.auth.user = user
            localStorage.setItem('user', JSON.stringify(user))
        },

        SET_LOADING(state, isLoading) {
            state.auth.isLoading = isLoading
        },

        SET_ERROR(state, error) {
            state.auth.error = error
        },

        CLEAR_AUTH(state) {
            state.auth.token = null
            state.auth.user = null
            state.auth.error = null
            localStorage.removeItem('token')
            localStorage.removeItem('user')
        }
    },

    actions: {
        async login({ commit }, credentials) {
            commit('SET_LOADING', true)
            commit('SET_ERROR', null)

            try {
                // Логин через JWT
                const response = await axios.post('/auth/jwt/create/', {
                    username: credentials.email, // Вход по email как username
                    password: credentials.password
                })

                const token = response.data.access

                // Сохраняем токен
                commit('SET_TOKEN', token)

                // Получаем данные пользователя
                const userResponse = await axios.get('/auth/users/me/')
                commit('SET_USER', userResponse.data)

                return { success: true }

            } catch (error) {
                const errorData = error.response?.data || { detail: 'Ошибка авторизации' }
                commit('SET_ERROR', errorData)
                return { success: false, error: errorData }
            } finally {
                commit('SET_LOADING', false)
            }
        },

        async register({ commit, dispatch }, userData) {
            commit('SET_LOADING', true)
            commit('SET_ERROR', null)

            try {
                // Регистрация
                const registerResponse = await axios.post('/auth/users/', userData)

                // Автоматический логин после регистрации
                const loginResult = await dispatch('login', {
                    email: userData.email,
                    password: userData.password
                })

                return loginResult

            } catch (error) {
                const errorData = error.response?.data || { detail: 'Ошибка регистрации' }
                commit('SET_ERROR', errorData)
                return { success: false, error: errorData }
            } finally {
                commit('SET_LOADING', false)
            }
        },

        logout({ commit }) {
            commit('CLEAR_AUTH')
        },

        async checkAuth({ state, commit }) {
            if (!state.auth.token) return false

            try {
                // Проверяем токен
                await axios.post('/auth/jwt/verify/', { token: state.auth.token })

                // Обновляем данные пользователя
                const userResponse = await axios.get('/auth/users/me/')
                commit('SET_USER', userResponse.data)

                return true
            } catch (error) {
                commit('CLEAR_AUTH')
                return false
            }
        },

        async updateProfile({ commit, state }, userData) {
            commit('SET_LOADING', true)
            commit('SET_ERROR', null)

            try {
                const response = await axios.put('/auth/users/me/', userData)
                commit('SET_USER', response.data)
                return { success: true }
            } catch (error) {
                const errorData = error.response?.data || { detail: 'Ошибка обновления' }
                commit('SET_ERROR', errorData)
                return { success: false, error: errorData }
            } finally {
                commit('SET_LOADING', false)
            }
        }
    },

    getters: {
        isAuthenticated: state => !!state.auth.token,
        isAdmin: state => {
            const user = state.auth.user
            return user && (user.role === 'admin' || user.is_staff === true)
        },
        userName: state => state.auth.user?.first_name || state.auth.user?.username || 'Пользователь',
        userData: state => state.auth.user
    }
})