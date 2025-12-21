import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/core/',
  headers: {
    'Content-Type': 'application/json',
  }
})

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Token ${token}`;
        //config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const carInfoApi = {
  getAll() {
    return apiClient.get('car_infos/')
  },
  getById(id) {
    return apiClient.get(`car_infos/${id}/`)
  },
  create(data) {
    return apiClient.post('car_infos/', data)
  },
  update(id, data) {
    return apiClient.patch(`car_infos/${id}/`, data)
  },
  delete(id) {
    return apiClient.delete(`car_infos/${id}/`)
  }
}

export const carApi = {
  getAll() {
    return apiClient.get('cars/')
  },
  getById(id) {
    return apiClient.get(`cars/${id}/`)
  },
  create(data) {
    return apiClient.post('cars/', data)
  },
  update(id, data) {
    return apiClient.patch(`cars/${id}/`, data)
  },
  delete(id) {
    return apiClient.delete(`cars/${id}/`)
  }
}

export const carInstanceApi = {
  getAll() {
    return apiClient.get('car_instances/')
  },
  getById(id) {
    return apiClient.get(`car_instances/${id}/`)
  },
  create(data) {
    return apiClient.post('car_instances/', data)
  },
  update(id, data) {
    return apiClient.patch(`car_instances/${id}/`, data)
  },
  delete(id) {
    return apiClient.delete(`car_instances/${id}/`)
  }
}

export const finesApi = {
  getAll() {
    return apiClient.get('fines/')
  }
}

export const carCrashesApi = {
  getAll() {
    return apiClient.get('car_crashes/')
  }
}

export const clientsApi = {
  getAll() {
    return apiClient.get('clients/')
  },
  getById(id) {
    return apiClient.get(`clients/${id}/`)
  },
  create(data) {
    return apiClient.post('clients/', data)
  },
  update(id, data) {
    return apiClient.patch(`clients/${id}/`, data)
  },
  delete(id) {
    return apiClient.delete(`clients/${id}/`)
  }
}

export const workersApi = {
  getAll() {
    return apiClient.get('workers/')
  },
  getById(id) {
    return apiClient.get(`workers/${id}/`)
  },
  create(data) {
    return apiClient.post('workers/', data)
  },
  update(id, data) {
    return apiClient.patch(`workers/${id}/`, data)
  },
  delete(id) {
    return apiClient.delete(`workers/${id}/`, {headers: {"Authorization": `Token ${localStorage.getItem('token')}`}})
  }
}

export const usersApi = {
  getAll() {
    return apiClient.get('users/')
  },
  getById(id) {
    return apiClient.get(`users/${id}/`)
  },
  update(id, data) {
    return apiClient.patch(`users/${id}/`, data)
  },
  delete(id) {
    return apiClient.delete(`users/${id}/`)
  }
}

export const rentContractsApi = {
  getAll() {
    return apiClient.get('rent_contracts/')
  },
  getById(id) {
    return apiClient.get(`rent_contracts/${id}/`)
  },
  create(data) {
    return apiClient.post('rent_contracts/', data)
  },
  update(id, data) {
    return apiClient.patch(`rent_contracts/${id}/`, data)
  },
  delete(id) {
    return apiClient.delete(`rent_contracts/${id}/`)
  }
}

export const analyticsApi = {
  getTimesRented() {
    return apiClient.get('times_rented/')
  },
  getDaysRented() {
    return apiClient.get('days_rented/')
  },
  getProfitByCar() {
    return apiClient.get('profit_by_car/')
  },
  getFinesByClient() {
    return apiClient.get('fines_by_client/')
  }
}

export default apiClient