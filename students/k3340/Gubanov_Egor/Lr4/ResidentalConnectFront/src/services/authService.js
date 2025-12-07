import api from './api'

export const authService = {
  async register(userData) {
    const response = await api.post('/api/auth/users/', userData)
    return response.data
  },

  async login(username, password) {
    const response = await api.post('/api/auth/token/login/', {
      username,
      password,
    })
    return response.data
  },

  async logout() {
    try {
      await api.post('/api/auth/token/logout/')
    } catch (error) {
      console.error('Logout error:', error)
    }
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user')
  },

  async getCurrentUser() {
    const response = await api.get('/api/auth/users/me/')
    return response.data
  },

  async updateUser(userData) {
    const response = await api.patch('/api/auth/users/me/', userData)
    return response.data
  },

  async changePassword(currentPassword, newPassword) {
    const response = await api.post('/api/auth/users/set_password/', {
      current_password: currentPassword,
      new_password: newPassword,
    })
    return response.data
  },
}

