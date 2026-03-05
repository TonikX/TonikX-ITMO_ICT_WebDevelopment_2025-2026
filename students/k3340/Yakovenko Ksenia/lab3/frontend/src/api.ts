const BASE = "http://127.0.0.1:8000/api"

export function getToken(): string {
  return localStorage.getItem("token") || ""
}
export function setToken(t: string) {
  localStorage.setItem("token", t)
}
export function clearToken() {
  localStorage.removeItem("token")
}

export async function fetchJson(url: string, options: RequestInit = {}) {
  const res = await fetch(url, {
    ...options,
    headers: { Accept: "application/json", ...(options.headers || {}) },
  })

  const text = await res.text()
  let data: any
  try {
    data = JSON.parse(text)
  } catch {
    data = { detail: text }
  }

  if (!res.ok) {
    throw new Error(data?.detail || JSON.stringify(data))
  }
  return data
}

export async function apiFetchJson(path: string, options: RequestInit = {}) {
  const token = getToken()
  const headers: Record<string, string> = { Accept: "application/json" }
  if (token) headers.Authorization = `Token ${token}`

  return fetchJson(`${BASE}${path}`, {
    ...options,
    headers: { ...headers, ...(options.headers as any) },
  })
}