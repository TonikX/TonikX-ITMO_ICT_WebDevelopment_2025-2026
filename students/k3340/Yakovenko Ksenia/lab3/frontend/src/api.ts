const BASE = "http://127.0.0.1:8000/api"

export function getToken(): string {
  return localStorage.getItem("token") || ""
}

export function setToken(token: string) {
  localStorage.setItem("token", token)
}

export function clearToken() {
  localStorage.removeItem("token")
}

export async function fetchJson(url: string, options: RequestInit = {}) {
  const res = await fetch(url, {
    ...options,
    headers: {
      Accept: "application/json",
      ...(options.headers || {}),
    },
  })

  const text = await res.text()
  let data: any = null

  try {
    data = text ? JSON.parse(text) : null
  } catch {
    data = text
  }

  if (!res.ok) {
    throw new Error(
      typeof data === "string" ? data : data?.detail || JSON.stringify(data)
    )
  }

  return data
}

export async function apiFetchJson(path: string, options: RequestInit = {}) {
  const token = getToken()

  return fetchJson(`${BASE}${path}`, {
    ...options,
    headers: {
      Accept: "application/json",
      ...(token ? { Authorization: `Token ${token}` } : {}),
      ...(options.headers || {}),
    },
  })
}