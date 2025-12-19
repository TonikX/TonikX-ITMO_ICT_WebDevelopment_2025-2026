import axios from 'axios';
import store from '@/store/index';

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  timeout: 10000,
});

axiosInstance.interceptors.request. use(
  (config) => {
    const token = store.state.auth.token;
    if (token) {
      config.headers. Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const getFlights = () => {
  return axiosInstance.get('/api/flights/');
};

export const getFlight = (flightId) => {
  return axiosInstance.get(`/api/flights/${flightId}/`);
};

export const updateFlight = (flightId, flightData) => {
  return axiosInstance.put(`/api/flights/${flightId}/`, flightData);
};

export const getCrewDetail = (crewId) => {
  return axiosInstance.get(`/api/crews/${crewId}/`);
};

export const getRouteDetail = (routeId) => {
  return axiosInstance.get(`/api/routes/${routeId}/`);
}

export const getAirlineCompanies = () => {
  return axiosInstance.get('/api/airline-companies/');
};

export const getRoutes = () => {
  return axiosInstance.get('/api/routes/');
};

export const getPlanes = () => {
  return axiosInstance.get('/api/planes/');
};

export const getCrews = () => {
  return axiosInstance.get('/api/crews/');
};

export const getCrewDetails = (crewId) => {
  return axiosInstance.get(`/api/crews/${crewId}/`);
};

export const updateCrew = (crewId, crewData) => {
  return axiosInstance.put(`/api/crews/${crewId}/`, crewData);
};

export const getCrewMemberDetails = (memberId) => {
  return axiosInstance.get(`/api/crew-members/${memberId}/`);
};

export const updateCrewMember = (memberId, memberData) => {
  return axiosInstance.put(`/api/crew-members/${memberId}/`, memberData);
};

export const getCrewMembers = () => {
  return axiosInstance.get('/api/crew-members/');
};

export const getCompanyDetails = (companyId) => {
  return axiosInstance.get(`/api/airline-companies/${companyId}/`);
};

export const getPlaneDetails = (planeId) => {
  return axiosInstance.get(`/api/planes/${planeId}/`);
};

export const updateCompany = (companyId, companyData) => {
  return axiosInstance.put(`/api/airline-companies/${companyId}/`, companyData);
};

export const updatePlane = (planeId, planeData) => {
  return axiosInstance.put(`/api/planes/${planeId}/`, planeData);
};

export const createCompany = (companyData) => {
  return axiosInstance.post('/api/airline-companies/', companyData);
};

export const createPlane = (planeData) => {
  return axiosInstance.post('/api/planes/', planeData);
};

export const createRoute = (routeData) => {
  return axiosInstance.post('/api/routes/', routeData);
};

export const createFlight = (flightData) => {
  return axiosInstance.post('/api/flights/', flightData);
};

export const createCrewMember = (crewMemberData) => {
  return axiosInstance.post('/api/crew-members/', crewMemberData);
};

export const createCrew = (crewData) => {
  return axiosInstance.post('/api/crews/', crewData);
};

export const deleteCrewMember = (memberId) => {
  return axiosInstance.delete(`/api/crew-members/${memberId}/`);
};

export const deleteCrew = (crewId) => {
  return axiosInstance.delete(`/api/crews/${crewId}/`);
};

export const deletePlane = (planeId) => {
  return axiosInstance.delete(`/api/planes/${planeId}/`);
};

export const deleteFlight = (flightId) => {
  return axiosInstance.delete(`/api/flights/${flightId}/`);
};

export const deleteRoute = (routeId) => {
  return axiosInstance.delete(`/api/routes/${routeId}/`);
};

export const deleteCompany = (companyId) => {
  return axiosInstance.delete(`/api/airline-companies/${companyId}/`);
};

export default axiosInstance;