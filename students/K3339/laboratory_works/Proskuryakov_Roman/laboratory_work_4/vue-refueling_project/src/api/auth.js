import api from './index'

export const authApi = {
  // Вход в систему
  login(credentials) {
    return api.post('/auth/token/login/', credentials)
  },
  
  // Выход из системы
  logout() {
    return api.post('/auth/token/logout/')
  },
  
  // Получение данных текущего пользователя
  getCurrentUser() {
    return api.get('/auth/users/me/')
  }
}