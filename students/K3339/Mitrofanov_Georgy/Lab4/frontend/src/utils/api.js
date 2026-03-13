import axios from 'axios'

const baseURL = '/api'

const instance = axios.create({
    baseURL,
    withCredentials: true
})

instance.interceptors.request.use(config => {
    const token = localStorage.getItem('token')
    console.log('Токен из localStorage:', token) // для проверки
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

function setAuth(token) {
    if (token) {
        localStorage.setItem('token', token)
        instance.defaults.headers.common['Authorization'] = `Bearer ${token}`
    } else {
        localStorage.removeItem('token')
        delete instance.defaults.headers.common['Authorization']
    }
}

export default Object.assign(instance, { setAuth })