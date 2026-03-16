import { apiClient } from './http'

// здесь собраны простые функции для работы с api

// блок авторизации и пользователя
export async function apiLogin(data) {
  // вход пользователя
  return apiClient.post('/auth/token/login/', data)
}

export async function apiLogout() {
  // выход пользователя
  return apiClient.post('/auth/token/logout/')
}

export async function apiRegister(data) {
  // регистрация нового пользователя
  return apiClient.post('/auth/users/', data)
}

export async function apiGetCurrentUser() {
  // получение данных текущего пользователя
  return apiClient.get('/auth/users/me/')
}

export async function apiUpdateCurrentUser(data) {
  // изменение данных текущего пользователя
  return apiClient.patch('/auth/users/me/', data)
}

// блок номеров и бронирований
export async function apiGetRooms(params = {}) {
  // получение списка всех номеров
  return apiClient.get('/api/rooms/', { params })
}

export async function apiGetAvailableRooms() {
  // получение списка свободных номеров на сегодня
  return apiClient.get('/api/rooms/available/')
}

export async function apiGetRoom(id) {
  // получение информации по одному номеру
  return apiClient.get(`/api/rooms/${id}/`)
}

export async function apiGetRoomHistory(id) {
  // история заселений в номер
  return apiClient.get(`/api/rooms/${id}/history/`)
}

export async function apiGetRoomCurrentGuest(id) {
  // кто сейчас живёт в номере
  return apiClient.get(`/api/rooms/${id}/current_guest/`)
}

export async function apiCreateBooking(data) {
  // создание бронирования (создание клиента)
  return apiClient.post('/api/clients/', data)
}

export async function apiGetClient(id) {
  // одна бронь по id (для редактирования)
  return apiClient.get(`/api/clients/${id}/`)
}

export async function apiUpdateBooking(id, data) {
  // обновление брони (редактирование)
  return apiClient.patch(`/api/clients/${id}/`, data)
}

export async function apiGetClientHistory(id) {
  // история конкретного клиента
  return apiClient.get(`/api/clients/${id}/history/`)
}

export async function apiGetMyBookings() {
  // брони, оформленные текущим пользователем
  return apiClient.get('/api/clients/my-bookings/')
}

