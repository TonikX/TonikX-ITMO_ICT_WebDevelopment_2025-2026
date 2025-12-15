import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    headers: {
        'Content-Type': 'application/json',
    }
});

// Добавляем интерсептор для автоматического прикрепления токена
api.interceptors.request.use(config => {
    const token = localStorage.getItem('authToken');
    if (token) {
        // Django DRF ожидает префикс 'Token '
        config.headers.Authorization = `Token ${token}`;
    }
    return config;
}, error => {
    return Promise.reject(error);
});

export default api;