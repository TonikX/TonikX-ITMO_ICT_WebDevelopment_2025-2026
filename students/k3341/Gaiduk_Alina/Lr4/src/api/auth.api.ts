import httpClient from './http'
import { LoginCredentials, TokenResponse, StaffRegister, Staff } from '../types'

// экспортируем для работы с аутентификацией
export const authAPI = {
  // метод для входа в систему принимает логин и пароль, возвращает токены
  login: async (credentials: LoginCredentials): Promise<TokenResponse> => {
    // отправляем POST запрос на эндпоинт /token/ с учетными данными пользователя
    const response = await httpClient.post<TokenResponse>('/token/', credentials)
    // данные из ответа содержат access и refresh токены
    return response.data
  },

  // метод для обновления access токена с помощью refresh токена
  refreshToken: async (refresh: string): Promise<{ access: string }> => {
    const response = await httpClient.post<{ access: string }>('/token/refresh/', {
      refresh, // передаем refresh токен в теле запроса
    })
    // возвращаем новый access токен из ответа сервера
    return response.data
  },

  // метод для регистрации нового сотрудника
  registerStaff: async (data: StaffRegister): Promise<Staff> => {
    const response = await httpClient.post<Staff>('/staff/register-staff/', data)
    // возвращаем данные созданного сотрудника из ответа сервера
    return response.data
  },
}


