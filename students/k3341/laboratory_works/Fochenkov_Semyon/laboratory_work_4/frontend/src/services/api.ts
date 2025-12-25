import axios, { type AxiosInstance } from 'axios'

const API_BASE_URL = 'http://localhost:8000'

class ApiService {
  private api: AxiosInstance

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Добавляем токен к каждому запросу
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('auth_token')
      if (token) {
        config.headers.Authorization = `Token ${token}`
      }
      return config
    })

    // Обработка ошибок
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Токен недействителен, удаляем его
          localStorage.removeItem('auth_token')
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }

  // Аутентификация
  async login(username: string, password: string) {
    const response = await this.api.post('/auth/token/login/', {
      username,
      password,
    })
    return response.data
  }

  async register(username: string, password: string, password_retype: string) {
    const response = await this.api.post('/auth/users/', {
      username,
      password,
      password_retype,
    })
    return response.data
  }

  async getCurrentUser() {
    const response = await this.api.get('/auth/users/me/')
    return response.data
  }

  async updateUser(data: { username?: string; email?: string }) {
    const response = await this.api.patch('/auth/users/me/', data)
    return response.data
  }

  async changePassword(current_password: string, new_password: string, re_new_password: string) {
    const response = await this.api.post('/auth/users/set_password/', {
      current_password,
      new_password,
      re_new_password,
    })
    return response.data
  }

  // Газеты (Newspapers)
  async getNewspapers(params?: { page?: number; page_size?: number }) {
    const response = await this.api.get('/api/newspapers/', { params })
    return response.data
  }

  async getNewspaper(id: number) {
    const response = await this.api.get(`/api/newspapers/${id}/`)
    return response.data
  }

  async createNewspaper(data: {
    title: string
    publication_index: string
    editor_first_name: string
    editor_last_name: string
    editor_middle_name?: string
    price_per_copy: string
  }) {
    const response = await this.api.post('/api/newspapers/', data)
    return response.data
  }

  async updateNewspaper(id: number, data: Partial<{
    title: string
    publication_index: string
    editor_first_name: string
    editor_last_name: string
    editor_middle_name: string
    price_per_copy: string
  }>) {
    const response = await this.api.patch(`/api/newspapers/${id}/`, data)
    return response.data
  }

  async deleteNewspaper(id: number) {
    const response = await this.api.delete(`/api/newspapers/${id}/`)
    return response.data
  }

  async getNewspaperFullDetail(id: number) {
    const response = await this.api.get(`/api/newspapers/${id}/full_detail/`)
    return response.data
  }

  async getNewspapersByName(name: string) {
    const response = await this.api.get('/api/newspapers/by_name/', { params: { name } })
    return response.data
  }

  async getNewspaperInfo(params: { id?: number; name?: string }) {
    const response = await this.api.get('/api/newspapers/info/', { params })
    return response.data
  }

  // Типографии (Printing Houses)
  async getPrintingHouses(params?: { page?: number; page_size?: number }) {
    const response = await this.api.get('/api/printing-houses/', { params })
    return response.data
  }

  async getPrintingHouse(id: number) {
    const response = await this.api.get(`/api/printing-houses/${id}/`)
    return response.data
  }

  async createPrintingHouse(data: {
    name: string
    address: string
    is_active: boolean
  }) {
    const response = await this.api.post('/api/printing-houses/', data)
    return response.data
  }

  async updatePrintingHouse(id: number, data: Partial<{
    name: string
    address: string
    is_active: boolean
  }>) {
    const response = await this.api.patch(`/api/printing-houses/${id}/`, data)
    return response.data
  }

  async deletePrintingHouse(id: number) {
    const response = await this.api.delete(`/api/printing-houses/${id}/`)
    return response.data
  }

  async getPrintingHouseFullDetail(id: number) {
    const response = await this.api.get(`/api/printing-houses/${id}/full_detail/`)
    return response.data
  }

  async getLargestCirculationEditor(id: number) {
    const response = await this.api.get(`/api/printing-houses/${id}/largest_circulation_editor/`)
    return response.data
  }

  async getPrintingHousesReport() {
    const response = await this.api.get('/api/printing-houses/report/')
    return response.data
  }

  // Почтовые отделения (Post Offices)
  async getPostOffices(params?: { page?: number; page_size?: number }) {
    const response = await this.api.get('/api/post-offices/', { params })
    return response.data
  }

  async getPostOffice(id: number) {
    const response = await this.api.get(`/api/post-offices/${id}/`)
    return response.data
  }

  async createPostOffice(data: {
    number: string
    address: string
  }) {
    const response = await this.api.post('/api/post-offices/', data)
    return response.data
  }

  async updatePostOffice(id: number, data: Partial<{
    number: string
    address: string
  }>) {
    const response = await this.api.patch(`/api/post-offices/${id}/`, data)
    return response.data
  }

  async deletePostOffice(id: number) {
    const response = await this.api.delete(`/api/post-offices/${id}/`)
    return response.data
  }

  async getPostOfficeFullDetail(id: number) {
    const response = await this.api.get(`/api/post-offices/${id}/full_detail/`)
    return response.data
  }

  async getPostOfficesByPrice(min_price: number) {
    const response = await this.api.get('/api/post-offices/by_price/', { params: { min_price } })
    return response.data
  }

  async getPostOfficesLowQuantity(max_quantity: number) {
    const response = await this.api.get('/api/post-offices/low_quantity/', { params: { max_quantity } })
    return response.data
  }

  // Распределения (Distributions)
  async getDistributions(params?: { page?: number; page_size?: number }) {
    const response = await this.api.get('/api/distributions/', { params })
    return response.data
  }

  async getDistribution(id: number) {
    const response = await this.api.get(`/api/distributions/${id}/`)
    return response.data
  }

  async createDistribution(data: {
    post_office: number
    newspaper: number
    printing_house: number
    quantity: number
  }) {
    const response = await this.api.post('/api/distributions/', data)
    return response.data
  }

  async updateDistribution(id: number, data: Partial<{
    post_office: number
    newspaper: number
    printing_house: number
    quantity: number
  }>) {
    const response = await this.api.patch(`/api/distributions/${id}/`, data)
    return response.data
  }

  async deleteDistribution(id: number) {
    const response = await this.api.delete(`/api/distributions/${id}/`)
    return response.data
  }

  async getDistributionByNewspaperAndAddress(params: {
    newspaper_id?: number
    newspaper_name?: string
    address: string
  }) {
    const response = await this.api.get('/api/distributions/by_newspaper_and_address/', { params })
    return response.data
  }

  // Метод для прямого доступа к axios instance
  get axiosInstance(): AxiosInstance {
    return this.api
  }
}

export default new ApiService()

