import axios from 'axios';
import router from './router'; 
import { useAuthStore } from './stores/auth'; 

const api = axios.create({
  baseURL: 'http://localhost:8010/', 
});

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`; 
  }
  return config;
});

api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
      console.warn('Токен недействителен или доступ запрещен. Выходим...');
      
      const auth = useAuthStore();
      auth.logout(); 
      
      router.push('/login');
    }
    return Promise.reject(error);
  }
);

export default api;
