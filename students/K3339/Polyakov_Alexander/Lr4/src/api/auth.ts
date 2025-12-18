import api, { setAuthToken } from './http'
import type { LoginPayload, RegisterPayload, User } from '../types/auth'

interface LoginResponse {
  auth_token: string
}

export const loginRequest = async (payload: LoginPayload): Promise<string> => {
  const { data } = await api.post<LoginResponse>('auth/token/login', payload)
  setAuthToken(data.auth_token)
  return data.auth_token
}

export const registerRequest = async (payload: RegisterPayload): Promise<void> => {
  await api.post('auth/users/', payload)
}

export const logoutRequest = async (): Promise<void> => {
  await api.post('auth/token/logout')
  setAuthToken(null)
}

export const meRequest = async (): Promise<User> => {
  const { data } = await api.get<User>('auth/users/me/')
  return data
}

