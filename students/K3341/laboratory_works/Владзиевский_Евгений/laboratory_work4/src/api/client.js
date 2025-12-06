import axios from 'axios'
import { api, API_BASE_URL, setTokens } from './http'

// Auth
export const registerUser = async (payload) => {
  const { data } = await axios.post(`${API_BASE_URL}/register`, payload)
  setTokens(data)
  return data
}

export const loginUser = async (payload) => {
  const { data } = await axios.post(`${API_BASE_URL}/login`, payload)
  setTokens(data)
  return data
}

export const getMe = async () => {
  const { data } = await api.get('/user/me')
  return data
}

export const updateProfile = async (payload) => {
  const { data } = await api.post('/user/edit', payload)
  return data
}

export const getUserById = async (id) => {
  const { data } = await api.get(`/user/${id}`)
  return data
}

// Posts
export const addPost = async (payload) => {
  const { data } = await api.post('/post/add', payload)
  return data
}

export const getLatestPosts = async ({ page = 1, perPage = 10 } = {}) => {
  const { data } = await api.get('/post/latests', { params: { page, per_page: perPage } })
  return data
}

export const getRecommendedPosts = async ({ page = 1, perPage = 10 } = {}) => {
  const { data } = await api.get('/post/recommended', { params: { page, per_page: perPage } })
  return data
}

export const getUserPosts = async ({ userId, page = 1, perPage = 10 }) => {
  const { data } = await api.get(`/post/user/${userId}`, { params: { page, per_page: perPage } })
  return data
}

export const getPostById = async (id) => {
  const { data } = await api.get(`/post/${id}`)
  return data
}

export const likePost = async (id) => api.post(`/post/${id}/like`)
export const unlikePost = async (id) => api.delete(`/post/${id}/like`)

// Comments
export const addComment = async (postId, text) => {
  const { data } = await api.post(`/post/${postId}/comment`, { text })
  return data
}

export const fetchComments = async (postId, { page = 1, perPage = 10 } = {}) => {
  const { data } = await api.get(`/post/${postId}/comments`, { params: { page, per_page: perPage } })
  return data
}

export const removeComment = async (postId, commentId) => api.delete(`/post/${postId}/comment/${commentId}`)

// Images
export const uploadImage = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  const { data } = await api.post('/image/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}
