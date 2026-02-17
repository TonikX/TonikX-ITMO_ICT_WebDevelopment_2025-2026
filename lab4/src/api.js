import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8003'

export const api = axios.create({ baseURL })

function unwrapList(data) {
  if (Array.isArray(data)) {
    return data
  }
  if (data && Array.isArray(data.results)) {
    return data.results
  }
  return []
}

// Добавление токена в заголовки
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Обработка ошибок авторизации
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export function isNetworkError(e) {
  return !e.response && (
    e.message === 'Network Error' ||
    e.code === 'ERR_NETWORK' ||
    e.code === 'ERR_EMPTY_RESPONSE' ||
    (e.request && !e.response)
  )
}

export function apiErrorMessage(e) {
  if (isNetworkError(e)) {
    return 'Сервер API недоступен. Проверьте VITE_API_BASE в .env или подключение к сети.'
  }
  if (e.response?.data) {
    if (typeof e.response.data === 'string') {
      return e.response.data
    }
    if (e.response.data.detail) {
      return e.response.data.detail
    }
    if (e.response.data.error) {
      return e.response.data.error
    }
    if (e.response.data.non_field_errors) {
      return e.response.data.non_field_errors[0]
    }
    // Обработка ошибок валидации
    const errors = Object.values(e.response.data).flat()
    if (errors.length > 0) {
      return errors[0]
    }
  }
  return e.response?.statusText || e.message || 'Ошибка запроса'
}

// API методы для аутентификации
export const authAPI = {
  async register(data) {
    const response = await api.post('/api/auth/users/', data)
    return response.data
  },
  async login(email, password) {
    const response = await api.post('/api/auth/token/login/', { email, password })
    return response.data
  },
  async logout() {
    await api.post('/api/auth/token/logout/')
  },
  async getMe() {
    const response = await api.get('/api/auth/users/me/')
    return response.data
  },
  async updateMe(data) {
    const response = await api.patch('/api/auth/users/me/', data)
    return response.data
  }
}

// API методы для задач
export const tasksAPI = {
  async getList() {
    const response = await api.get('/api/tasks/')
    return unwrapList(response.data)
  },
  async getDetail(id) {
    const response = await api.get(`/api/tasks/${id}/`)
    return response.data
  },
  async create(data) {
    const response = await api.post('/api/tasks/', data)
    return response.data
  },
  async addFile(id, formData) {
    if (!formData.get('task')) {
      formData.append('task', id)
    }
    const response = await api.post(`/api/tasks/${id}/add_file/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },
  async addLink(id, data) {
    const response = await api.post(`/api/tasks/${id}/add_link/`, {
      ...data,
      task: id
    })
    return response.data
  },
  async setConsultationLink(id, consultationLink) {
    const response = await api.patch(`/api/tasks/${id}/set_consultation_link/`, {
      consultation_link: consultationLink
    })
    return response.data
  }
}

// API методы для команд
export const teamsAPI = {
  async getList() {
    const response = await api.get('/api/teams/')
    return unwrapList(response.data)
  },
  async getDetail(id) {
    const response = await api.get(`/api/teams/${id}/`)
    return response.data
  },
  async create(data) {
    const response = await api.post('/api/teams/', data)
    return response.data
  },
  async selectTask(id, taskId) {
    const response = await api.patch(`/api/teams/${id}/select_task/`, { task_id: taskId })
    return response.data
  },
  async addMember(id, data) {
    const response = await api.post(`/api/teams/${id}/add_member/`, data)
    return response.data
  }
}

// API методы для решений
export const solutionsAPI = {
  async getList() {
    const response = await api.get('/api/solutions/')
    return unwrapList(response.data)
  },
  async getDetail(id) {
    const response = await api.get(`/api/solutions/${id}/`)
    return response.data
  },
  async create(formData) {
    const response = await api.post('/api/solutions/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },
  async getEvaluations(id) {
    const response = await api.get(`/api/solutions/${id}/evaluations/`)
    return response.data
  }
}

// API методы для оценок
export const evaluationsAPI = {
  async getList() {
    const response = await api.get('/api/evaluations/')
    return unwrapList(response.data)
  },
  async getMyEvaluations() {
    const response = await api.get('/api/evaluations/my_evaluations/')
    return response.data
  },
  async getSolutionsByDate() {
    const response = await api.get('/api/evaluations/solutions_by_date/')
    return response.data
  },
  async create(data) {
    const response = await api.post('/api/evaluations/', data)
    return response.data
  }
}
