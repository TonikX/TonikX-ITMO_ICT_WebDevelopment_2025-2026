import api from './axios'

export const authAPI = {
  register(data) {
    return api.post('/auth/users/', data)
  },
  login(data) {
    return api.post('/auth/token/login/', data)
  },
  logout() {
    return api.post('/auth/token/logout/')
  },
  getCurrentUser() {
    return api.get('/auth/users/me/')
  }
}

