import { defineStore } from 'pinia'
import { authApi } from '../api/auth'
import router from '../router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('auth_token') || null,
    user: JSON.parse(localStorage.getItem('user_data')) || null,
    isLoading: false,
    error: null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    userData: (state) => state.user,
    // Получаем всю информацию о станции
    gasStation: (state) => state.user?.gas_station || null,
    // Получаем адрес станции
    stationAddress: (state) => state.user?.gas_station?.station_address || 'Не назначена',
    // Получаем ID станции
    stationId: (state) => state.user?.gas_station?.id_station || null,
    // Получаем информацию о компании
    company: (state) => state.user?.gas_station?.company || null,
    // Получаем ID компании
    companyId: (state) => state.user?.gas_station?.company?.id_company || null,
    // Получаем название компании
    companyTitle: (state) => state.user?.gas_station?.company?.company_title || 'Неизвестно'
  },
  
  actions: {
    async login(credentials) {
      this.isLoading = true
      this.error = null
      
      try {
        // Получаем токен от сервера
        const response = await authApi.login(credentials)
        const token = response.data.auth_token || response.data.token
        
        if (!token) {
          throw new Error('Токен не получен от сервера')
        }
        
        // Сохраняем токен
        this.token = token
        localStorage.setItem('auth_token', token)
        
        // Получаем данные пользователя
        const userResponse = await authApi.getCurrentUser()
        this.user = userResponse.data
        
        console.log('Получены данные пользователя:', this.user) // Для отладки
        
        // Сохраняем данные пользователя
        localStorage.setItem('user_data', JSON.stringify(userResponse.data))
        
        // Перенаправляем на главную страницу
        router.push('/')
        
        return { success: true }
        
      } catch (error) {
        this.error = error.response?.data || error.message
        console.error('Ошибка авторизации:', error)
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },
    
    async logout() {
      try {
        await authApi.logout()
      } catch (error) {
        console.error('Ошибка при выходе:', error)
      } finally {
        // Очищаем локальные данные в любом случае
        this.token = null
        this.user = null
        this.error = null
        localStorage.removeItem('auth_token')
        localStorage.removeItem('user_data')
        
        // Перенаправляем на страницу входа
        router.push('/login')
      }
    },
    
    async checkAuth() {
      if (!this.token) {
        return false
      }
      
      try {
        const response = await authApi.getCurrentUser()
        this.user = response.data
        console.log('Проверка авторизации, получен пользователь:', this.user) // Для отладки
        localStorage.setItem('user_data', JSON.stringify(response.data))
        return true
      } catch (error) {
        console.error('Ошибка проверки авторизации:', error)
        this.logout()
        return false
      }
    },
    
    // Дополнительный метод для обновления данных пользователя
    async refreshUserData() {
      try {
        const response = await authApi.getCurrentUser()
        this.user = response.data
        localStorage.setItem('user_data', JSON.stringify(response.data))
        return this.user
      } catch (error) {
        console.error('Ошибка обновления данных пользователя:', error)
        throw error
      }
    }
  }
})