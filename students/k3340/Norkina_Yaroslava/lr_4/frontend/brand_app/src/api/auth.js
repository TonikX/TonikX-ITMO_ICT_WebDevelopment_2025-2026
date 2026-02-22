import api from './index'

export default {
    // Регистрация
    register(data) {
        return api.post('/auth/users/', data)
    },

    // Авторизация
    login(credentials) {
        return api.post('/auth/jwt/create/', credentials)
    },

    // Получить данные пользователя
    getMe() {
        return api.get('/auth/users/me/')
    },

    // Обновить данные пользователя
    updateMe(data) {
        return api.patch('/auth/users/me/', data)
    },

    // Обновить пароль
    changePassword(data) {
        return api.post('/auth/users/set_password/', data)
    },

    // Выход
    logout() {
        // На бэкенде JWT stateless, так что просто удаляем токен на фронте
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
    }
}