import api from '../../api/auth'

const state = {
  token: localStorage.getItem('token') || null,
  user: JSON.parse(localStorage.getItem('user')) || null,
  isAuthenticated: !!localStorage.getItem('token')
}

const getters = {
  isAuthenticated: state => state.isAuthenticated,
  currentUser: state => state.user,
  token: state => state.token
}

const mutations = {
  SET_TOKEN(state, token) {
    state.token = token
    localStorage.setItem('token', token)
  },
  SET_USER(state, user) {
    state.user = user
    localStorage.setItem('user', JSON.stringify(user))
  },
  SET_AUTH(state, auth) {
    state.isAuthenticated = auth
  },
  CLEAR_AUTH(state) {
    state.token = null
    state.user = null
    state.isAuthenticated = false
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }
}

const actions = {
  async login({ commit }, credentials) {
    try {
      const response = await api.login(credentials)
      commit('SET_TOKEN', response.data.auth_token)
      commit('SET_AUTH', true)

      // Получаем информацию о пользователе
      const userResponse = await api.getCurrentUser()
      commit('SET_USER', userResponse.data)

      return { success: true }
    } catch (error) {
      console.error('Login error:', error)
      return {
        success: false,
        error: error.response?.data || {
          non_field_errors: ['Ошибка входа. Проверьте учетные данные.']
        }
      }
    }
  },

  async register({ commit }, userData) {
    try {
      const response = await api.register(userData)
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Register error:', error)
      return {
        success: false,
        error: error.response?.data || {
          detail: 'Ошибка регистрации.'
        }
      }
    }
  },

  async logout({ commit }) {
    try {
      await api.logout()
    } catch (error) {
      console.error('Logout error:', error)
    }
    commit('CLEAR_AUTH')
  },

  async updateProfile({ commit }, userData) {
    try {
      const response = await api.updateProfile(userData)
      commit('SET_USER', response.data)
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Update profile error:', error)
      return {
        success: false,
        error: error.response?.data || {
          detail: 'Ошибка обновления профиля.'
        }
      }
    }
  },

  async checkAuth({ commit }) {
    const token = localStorage.getItem('token')
    if (token) {
      try {
        const userResponse = await api.getCurrentUser()
        commit('SET_USER', userResponse.data)
        commit('SET_AUTH', true)
        return true
      } catch (error) {
        // Если токен невалидный, очищаем
        commit('CLEAR_AUTH')
        return false
      }
    }
    return false
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}