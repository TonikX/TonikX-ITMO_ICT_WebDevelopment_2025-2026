import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export const authAPI = {
  login: (credentials) => api.post('/auth/token/login/', credentials),
  register: (userData) => api.post('/auth/users/', userData),
  logout: () => api.post('/auth/token/logout/'),
  getCurrentUser: () => api.get('/auth/users/me/'),
}

export const restaurantAPI = {
  getPositions: () => api.get('/positions/'),
  createPosition: (data) => api.post('/positions/', data),
  updatePosition: (id, data) => api.put(`/positions/${id}/`, data),
  deletePosition: (id) => api.delete(`/positions/${id}/`),

  getEmployees: () => api.get('/employees/'),
  createEmployee: (data) => api.post('/employees/', data),
  updateEmployee: (id, data) => api.put(`/employees/${id}/`, data),
  deleteEmployee: (id) => api.delete(`/employees/${id}/`),

  getIngredients: () => api.get('/ingredients/'),
  createIngredient: (data) => api.post('/ingredients/', data),
  updateIngredient: (id, data) => api.put(`/ingredients/${id}/`, data),
  deleteIngredient: (id) => api.delete(`/ingredients/${id}/`),
  getLowStockIngredients: () => api.get('/ingredients/low-stock/'),

  getDishes: () => api.get('/dishes/'),
  createDish: (data) => api.post('/dishes/', data),
  updateDish: (id, data) => api.put(`/dishes/${id}/`, data),
  deleteDish: (id) => api.delete(`/dishes/${id}/`),

  getTables: () => api.get('/tables/'),
  createTable: (data) => api.post('/tables/', data),
  updateTable: (id, data) => api.put(`/tables/${id}/`, data),
  deleteTable: (id) => api.delete(`/tables/${id}/`),
  updateTableStatus: (id, status) => api.post(`/tables/${id}/status/`, { status }),

  getOrders: () => api.get('/orders/'),
  createOrder: (data) => api.post('/orders/', data),
  updateOrder: (id, data) => api.put(`/orders/${id}/`, data),
  deleteOrder: (id) => api.delete(`/orders/${id}/`),
  updateOrderStatus: (id, status) => api.post(`/orders/${id}/status/`, { status }),
  getOrdersByStatus: (status) => api.get(`/orders/status/${status}/`),

  getChefDishes: () => api.get('/chef-dishes/'),
  createChefDish: (data) => api.post('/chef-dishes/', data),
  deleteChefDish: (id) => api.delete(`/chef-dishes/${id}/`),
  getChefAvailableDishes: (chefId) => api.get(`/chefs/${chefId}/dishes/`),
}

export default api