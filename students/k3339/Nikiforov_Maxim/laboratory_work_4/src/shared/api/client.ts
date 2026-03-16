import { API_BASE_URL, AUTH_TOKEN_KEY } from '../config/api'

export type RequestOptions = Omit<RequestInit, 'body'> & {
  body?: RequestInit['body'] | object
  params?: Record<string, string>
  token?: string | null
}

function buildUrl(path: string, params?: Record<string, string>): string {
  const base = path.startsWith('http') ? path : `${API_BASE_URL}${path}`
  if (!params || Object.keys(params).length === 0) return base
  const search = new URLSearchParams(params).toString()
  return `${base}${base.includes('?') ? '&' : '?'}${search}`
}

function getStoredToken(): string | null {
  return localStorage.getItem(AUTH_TOKEN_KEY)
}

/**
 * Универсальный клиент на fetch. Подставляет Authorization: Token и базовый URL.
 */
export async function request<T = unknown>(
  path: string,
  options: RequestOptions = {}
): Promise<{ data: T; status: number; ok: boolean }> {
  const { params, token = getStoredToken(), ...init } = options
  const url = buildUrl(path, params)
  const headers = new Headers(init.headers as HeadersInit)
  if (token) {
    headers.set('Authorization', `Token ${token}`)
  }
  let body = init.body
  const contentType = headers.get('Content-Type')
  if (
    !contentType &&
    body &&
    typeof body === 'object' &&
    !(body instanceof FormData) &&
    !(body instanceof URLSearchParams)
  ) {
    headers.set('Content-Type', 'application/json')
    body = JSON.stringify(body)
  }

  const response = await fetch(url, {
    ...init,
    headers,
    body: body as BodyInit | null | undefined,
  })

  let data: T
  const text = await response.text()
  if (text) {
    try {
      data = JSON.parse(text) as T
    } catch {
      data = text as unknown as T
    }
  } else {
    data = undefined as unknown as T
  }

  return {
    data,
    status: response.status,
    ok: response.ok,
  }
}

export function setToken(token: string | null): void {
  if (token) localStorage.setItem(AUTH_TOKEN_KEY, token)
  else localStorage.removeItem(AUTH_TOKEN_KEY)
}

export { getStoredToken }
