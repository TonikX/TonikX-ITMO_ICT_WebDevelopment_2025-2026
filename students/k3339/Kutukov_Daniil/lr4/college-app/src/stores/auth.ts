import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService, type User, type LoginCredentials, type RegisterData } from '@/services/auth'

export const useAuthStore = defineStore('auth', () => {
    const user = ref<User | null>(null)
    const loading = ref(false)
    const error = ref<string | null>(null)

    const isAuthenticated = computed(() => !!user.value)

    async function login(credentials: LoginCredentials) {
        loading.value = true
        error.value = null
        try {
            await authService.login(credentials)
            await loadUser()
            return true
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Ошибка входа'
            return false
        } finally {
            loading.value = false
        }
    }

    async function register(data: RegisterData) {
        loading.value = true
        error.value = null
        try {
            await authService.register(data)
            return true
        } catch (err: any) {
            error.value = err.response?.data?.username?.[0] ||
                err.response?.data?.email?.[0] ||
                err.response?.data?.password?.[0] ||
                'Ошибка регистрации'
            return false
        } finally {
            loading.value = false
        }
    }

    async function logout() {
        await authService.logout()
        user.value = null
    }

    async function loadUser() {
        if (!authService.isAuthenticated()) return

        try {
            user.value = await authService.getCurrentUser()
        } catch (err) {
            user.value = null
            localStorage.removeItem('auth_token')
        }
    }

    return {
        user,
        loading,
        error,
        isAuthenticated,
        login,
        register,
        logout,
        loadUser,
    }
})
