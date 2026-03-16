/**
 * Базовый URL API бэкенда (laboratory_work_3).
 * Для dev: http://localhost:8000 (Vite dev на 5173).
 */
export const API_BASE_URL =
  (import.meta as unknown as { env: { VITE_API_BASE_URL?: string } }).env
    .VITE_API_BASE_URL ?? 'http://localhost:8000'

export const AUTH_TOKEN_KEY = 'library_auth_token'
