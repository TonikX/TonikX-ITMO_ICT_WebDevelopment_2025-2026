import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  timeout: 10000,
});

export const getFlights = () => {
  return axiosInstance.get('/api/flights/');
};

export const getCrewDetail = (crewId) => {
  return axiosInstance.get(`/api/crews/${crewId}/`);
};

export const getRouteDetail = (routeId) => {
  return axiosInstance.get(`/api/routes/${routeId}/`);
}

export default axiosInstance;