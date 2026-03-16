import { request, setToken } from './client'

export interface LoginPayload {
  username: string
  password: string
}

export interface RegisterPayload {
  username: string
  password: string
  re_password: string
}

export interface User {
  id: number
  username: string
  email?: string
}

export interface UpdateMePayload {
  username?: string
  email?: string
  current_password?: string
  new_password?: string
  re_new_password?: string
}

export async function login(payload: LoginPayload) {
  const res = await request<{ auth_token: string }>('/auth/token/login/', {
    method: 'POST',
    body: payload,
    token: null,
  })
  if (res.ok && res.data && typeof res.data === 'object' && 'auth_token' in res.data) {
    setToken((res.data as { auth_token: string }).auth_token)
    return res.data
  }
  const err = res.data as { detail?: string; non_field_errors?: string[] }
  const msg = err?.detail ?? err?.non_field_errors?.[0] ?? 'Ошибка входа'
  throw new Error(msg)
}

export async function logout() {
  await request('/auth/token/logout/', { method: 'POST' })
  setToken(null)
}

export async function register(payload: RegisterPayload) {
  const res = await request<User>('/auth/users/', {
    method: 'POST',
    body: payload,
    token: null,
  })
  if (!res.ok) {
    const err = res.data as unknown as Record<string, unknown>
    const msg = typeof err.detail === 'string' ? err.detail : JSON.stringify(err)
    throw new Error(msg)
  }
  return res.data
}

export async function fetchMe(): Promise<User | null> {
  const res = await request<User>('/auth/users/me/')
  if (res.ok && res.data) return res.data
  return null
}

export async function updateMe(payload: UpdateMePayload): Promise<User> {
  const res = await request<User>('/auth/users/me/', {
    method: 'PATCH',
    body: payload,
  })
  if (!res.ok) {
    const err = res.data as unknown as Record<string, unknown>
    const msg = typeof err.detail === 'string' ? err.detail : JSON.stringify(err)
    throw new Error(msg)
  }
  return res.data!
}
