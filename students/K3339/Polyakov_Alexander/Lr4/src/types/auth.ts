export interface User {
  id: number
  username: string
  email?: string
  is_staff?: boolean
  broker_id?: number | null
}

export interface LoginPayload {
  username: string
  password: string
}

export interface RegisterPayload {
  username: string
  password: string
  email?: string
}

