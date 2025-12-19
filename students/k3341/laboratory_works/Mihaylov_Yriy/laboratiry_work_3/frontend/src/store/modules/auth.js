import axios from 'axios'
import { ENDPOINTS } from '../../api/endpoints'

const state = {
    user: null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token')
}

const mutations = {
    SET_USER(state, user) {
        state.user = user
    },
    SET_TOKEN(state, token) {
        state.token = token
        state.isAuthenticated = true
        localStorage.setItem('token', token)
    },
    LOGOUT(state) {
        state.user = null
        state.token = null
        state.isAuthenticated = false
        localStorage.removeItem('token')
    }
}

const actions = {
    async login({ commit, dispatch }, credentials) {
        try {
            const authAxios = axios.create({
                baseURL: 'http://localhost:8000/'  // Без /api/
            })
            // Используем Djoser JWT endpoint
            const response = await axios.post('http://localhost:8000/auth/jwt/create/', credentials)
            const token = response.data.access

            commit('SET_TOKEN', token)

            // Получаем данные пользователя
            await dispatch('fetchUser')

            return { success: true }
        } catch (error) {
            return {
                success: false,
                error: error.response?.data || 'Ошибка авторизации'
            }
        }
    },

    async register({ commit }, userData) {
        try {
            await axios.post('auth/users/', userData)
            return { success: true }
        } catch (error) {
            return {
                success: false,
                error: error.response?.data || 'Ошибка регистрации'
            }
        }
    },

    async fetchUser({ commit }) {
        try {
            const response = await axios.get('http://localhost:8000/auth/users/me/')
            commit('SET_USER', response.data)
            return response.data
        } catch (error) {
            commit('LOGOUT')
            throw error
        }
    },

    async updateProfile({ commit }, userData) {
        try {
            const response = await axios.put('auth/users/me/', userData)
            commit('SET_USER', response.data)
            return { success: true }
        } catch (error) {
            return {
                success: false,
                error: error.response?.data || 'Ошибка обновления'
            }
        }
    },

    async changePassword({ commit }, passwords) {
        try {
            await axios.post('auth/users/set_password/', passwords)
            return { success: true }
        } catch (error) {
            return {
                success: false,
                error: error.response?.data || 'Ошибка смены пароля'
            }
        }
    },

    logout({ commit }) {
        commit('LOGOUT')
    }
}

const getters = {
    user: state => state.user,
    token: state => state.token,
    isAuthenticated: state => state.isAuthenticated,
    isAdmin: state => state.user?.is_staff || false
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters
}