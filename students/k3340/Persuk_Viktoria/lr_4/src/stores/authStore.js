import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as authAPI from '@/api/auth'
import * as profileAPI from '@/api/profile'
import router from '@/router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: null,
    refreshToken: null,
    user: null,
    profile: null,
    isLoading: false,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken && !!state.user,
    displayName: (state) => {
      if (state.profile?.display_name) {
        return state.profile.display_name
      }
      return state.user?.username || state.user?.email || 'Пользователь'
    },
  },

  actions: {
    /**
     * Вход пользователя
     * @param {string} usernameOrEmail - Username или email пользователя
     * @param {string} password - Пароль
     */
    async login(usernameOrEmail, password) {
      this.isLoading = true
      try {
        const tokens = await authAPI.login(usernameOrEmail, password)
        this.accessToken = tokens.access
        this.refreshToken = tokens.refresh

        // Загружаем данные пользователя
        await this.loadUser()

        // Загружаем профиль
        await this.loadProfile()

        return { success: true }
      } catch (error) {
        const message = error.response?.data?.detail ||
                       error.response?.data?.non_field_errors?.[0] ||
                       'Ошибка входа. Проверьте email и пароль.'
        return { success: false, error: message }
      } finally {
        this.isLoading = false
      }
    },

    /**
     * Регистрация нового пользователя
     */
    async register(email, username, password, rePassword) {
      this.isLoading = true
      try {
        await authAPI.register(email, username, password, rePassword)
        // После регистрации автоматически входим
        // Используем email или username для входа (username приоритетнее если указан)
        const loginField = username || email
        return await this.login(loginField, password)
      } catch (error) {
        const errors = error.response?.data || {}
        let message = 'Ошибка регистрации.'

        // Формируем сообщение об ошибке из ответа API
        if (errors.email) {
          message = `Email: ${Array.isArray(errors.email) ? errors.email[0] : errors.email}`
        } else if (errors.username) {
          message = `Username: ${Array.isArray(errors.username) ? errors.username[0] : errors.username}`
        } else if (errors.password) {
          message = `Пароль: ${Array.isArray(errors.password) ? errors.password[0] : errors.password}`
        } else if (errors.non_field_errors) {
          message = Array.isArray(errors.non_field_errors)
            ? errors.non_field_errors[0]
            : errors.non_field_errors
        }

        return { success: false, error: message }
      } finally {
        this.isLoading = false
      }
    },

    /**
     * Обновление JWT токена
     */
    async refresh() {
      if (!this.refreshToken) {
        throw new Error('Нет refresh токена')
      }

      try {
        const tokens = await authAPI.refreshToken(this.refreshToken)
        this.accessToken = tokens.access
        return { success: true }
      } catch (error) {
        // Если не удалось обновить токен - выходим
        this.logout()
        throw error
      }
    },

    /**
     * Загрузка данных текущего пользователя
     */
    async loadUser() {
      try {
        const userData = await authAPI.getCurrentUser()
        this.user = userData
        return userData
      } catch (error) {
        console.error('Ошибка загрузки пользователя:', error)
        throw error
      }
    },

    /**
     * Загрузка профиля текущего пользователя
     */
    async loadProfile() {
      try {
        const profileData = await profileAPI.getProfile()
        this.profile = profileData
        return profileData
      } catch (error) {
        // Профиль может не существовать - это нормально
        if (error.response?.status === 404) {
          this.profile = null
          return null
        }
        console.error('Ошибка загрузки профиля:', error)
        throw error
      }
    },

    /**
     * Обновление данных пользователя
     */
    async updateUser(userData) {
      this.isLoading = true
      try {
        const updatedUser = await authAPI.updateCurrentUser(userData)
        this.user = { ...this.user, ...updatedUser }
        return { success: true, data: updatedUser }
      } catch (error) {
        const errors = error.response?.data || {}
        let message = 'Ошибка обновления данных.'

        if (errors.email) {
          message = `Email: ${Array.isArray(errors.email) ? errors.email[0] : errors.email}`
        } else if (errors.username) {
          message = `Username: ${Array.isArray(errors.username) ? errors.username[0] : errors.username}`
        }

        return { success: false, error: message }
      } finally {
        this.isLoading = false
      }
    },

    /**
     * Выход пользователя
     */
    logout() {
      this.accessToken = null
      this.refreshToken = null
      this.user = null
      this.profile = null
      router.push('/login')
    },
  },

  persist: {
    enabled: true,
    strategies: [
      {
        key: 'auth',
        storage: localStorage,
        paths: ['accessToken', 'refreshToken', 'user', 'profile'],
      },
    ],
  },
})
