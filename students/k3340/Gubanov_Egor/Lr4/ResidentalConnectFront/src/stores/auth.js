import { defineStore } from 'pinia'
import { authService } from '@/services/authService'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('auth_token') || null,
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    loading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userRole: (state) => state.user?.role || null,
    userName: (state) => {
      if (state.user?.first_name && state.user?.last_name) {
        return `${state.user.first_name} ${state.user.last_name}`
      }
      return state.user?.username || 'Пользователь'
    },
  },

  actions: {
    async login(username, password) {
      this.loading = true
      this.error = null
      try {
        const data = await authService.login(username, password)
        this.token = data.auth_token
        localStorage.setItem('auth_token', this.token)
        
        const user = await authService.getCurrentUser()
        this.user = user
        localStorage.setItem('user', JSON.stringify(user))
        
        return { success: true }
      } catch (error) {
        let errorMessage = 'Ошибка входа. Проверьте логин и пароль.'
        
        if (error.response?.data) {
          if (error.response.data.non_field_errors) {
            errorMessage = Array.isArray(error.response.data.non_field_errors)
              ? error.response.data.non_field_errors[0]
              : error.response.data.non_field_errors
          } else if (error.response.data.message) {
            errorMessage = error.response.data.message
          } else if (error.response.data.detail) {
            errorMessage = error.response.data.detail
          } else {
            const errors = []
            Object.keys(error.response.data).forEach((key) => {
              const messages = error.response.data[key]
              if (Array.isArray(messages)) {
                errors.push(...messages)
              } else {
                errors.push(messages)
              }
            })
            if (errors.length > 0) {
              errorMessage = errors.join(', ')
            }
          }
        } else if (error.message) {
          errorMessage = error.message
        }
        
        this.error = errorMessage
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async register(userData) {
      this.loading = true
      this.error = null
      try {
        await authService.register(userData)
        return await this.login(userData.username, userData.password)
      } catch (error) {
        const errorMessages = []
        const fieldErrors = {}
        
        if (error.response?.data) {
          Object.keys(error.response.data).forEach((key) => {
            const messages = error.response.data[key]
            if (Array.isArray(messages)) {
              fieldErrors[key] = messages
              messages.forEach(msg => {
                errorMessages.push(`${key}: ${msg}`)
              })
            } else if (typeof messages === 'string') {
              fieldErrors[key] = [messages]
              errorMessages.push(`${key}: ${messages}`)
            } else {
              fieldErrors[key] = [JSON.stringify(messages)]
              errorMessages.push(`${key}: ${JSON.stringify(messages)}`)
            }
          })
        } else if (error.message) {
          errorMessages.push(error.message)
        } else {
          errorMessages.push('Ошибка регистрации')
        }
        
        this.error = errorMessages.join(', ')
        return { 
          success: false, 
          error: this.error,
          fieldErrors: Object.keys(fieldErrors).length > 0 ? fieldErrors : null
        }
      } finally {
        this.loading = false
      }
    },

    async logout() {
      await authService.logout()
      this.token = null
      this.user = null
    },

    async fetchUser() {
      try {
        const user = await authService.getCurrentUser()
        this.user = user
        localStorage.setItem('user', JSON.stringify(user))
      } catch (error) {
        console.error('Error fetching user:', error)
      }
    },

    async updateProfile(userData) {
      this.loading = true
      this.error = null
      try {
        const updatedUser = await authService.updateUser(userData)
        this.user = updatedUser
        localStorage.setItem('user', JSON.stringify(updatedUser))
        return { success: true }
      } catch (error) {
        const errorMessages = []
        if (error.response?.data) {
          Object.keys(error.response.data).forEach((key) => {
            const messages = error.response.data[key]
            if (Array.isArray(messages)) {
              errorMessages.push(...messages)
            } else {
              errorMessages.push(messages)
            }
          })
        }
        this.error = errorMessages.join(', ') || 'Ошибка обновления профиля'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async changePassword(currentPassword, newPassword) {
      this.loading = true
      this.error = null
      try {
        await authService.changePassword(currentPassword, newPassword)
        return { success: true }
      } catch (error) {
        const errorMessages = []
        if (error.response?.data) {
          Object.keys(error.response.data).forEach((key) => {
            const messages = error.response.data[key]
            if (Array.isArray(messages)) {
              errorMessages.push(...messages)
            } else {
              errorMessages.push(messages)
            }
          })
        }
        this.error = errorMessages.join(', ') || 'Ошибка смены пароля'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },
  },
})

