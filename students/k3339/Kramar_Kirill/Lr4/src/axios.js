import axios from 'axios';
import TokenStore from "@/stores/token";

const API = axios.create({
    baseURL: 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Origin': 'http://localhost:5173'
    },
    withCredentials: true,
    maxRedirects: 0
});

API.interceptors.request.use(
    (config) => {
        const token = TokenStore.getToken();
        if (token) {
            config.headers['Authorization'] = `Token ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

API.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        if (error.response && error.response.status === 301 && !originalRequest._retry) {
            originalRequest._retry = true;
            const token = TokenStore.getToken();
            if (token) {
                originalRequest.headers['Authorization'] = `Token ${token}`;
            }
            return axios(originalRequest);
        }
        return Promise.reject(error);
    }
);

export default API;