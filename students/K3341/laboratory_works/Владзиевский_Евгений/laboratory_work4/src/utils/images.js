import { api, API_BASE_URL } from '../api/http'

const apiBase = API_BASE_URL.replace(/\/+$/, '')
const cache = new Map()

const extractHash = (raw) => {
  if (!raw) return ''
  try {
    const url = new URL(raw)
    const parts = (url.pathname || '').split('/')
    return parts.pop() || parts.pop() || ''
  } catch (_) {
    return raw.includes('/') ? raw.split('/').pop() : raw
  }
}

export const resolveImageSrc = async (img) => {
  const raw = typeof img === 'string' ? img : img?.hash || img?.url
  const hash = extractHash(raw)
  if (!hash) return ''
  if (cache.has(hash)) return cache.get(hash)
  const { data } = await api.get(`/image/${hash}`, { responseType: 'blob' })
  const objectUrl = URL.createObjectURL(data)
  cache.set(hash, objectUrl)
  return objectUrl
}
