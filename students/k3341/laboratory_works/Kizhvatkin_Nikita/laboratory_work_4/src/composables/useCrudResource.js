import { ref } from 'vue'
import { http } from '../api/http'

export function useCrudResource(resourcePath) {
  const items = ref([])
  const loading = ref(false)
  const error = ref('')

  async function list(params = {}) {
    loading.value = true
    error.value = ''
    try {
      const res = await http.get(resourcePath, { params })
      // DRF pagination support
      items.value = Array.isArray(res.data) ? res.data : (res.data.results || [])
    } catch (e) {
      error.value = humanizeError(e)
    } finally {
      loading.value = false
    }
  }

  async function create(payload) {
    error.value = ''
    try {
      const res = await http.post(resourcePath, payload)
      return res.data
    } catch (e) {
      error.value = humanizeError(e)
      throw e
    }
  }

  async function update(id, payload) {
    error.value = ''
    try {
      const res = await http.put(`${resourcePath}${id}/`, payload)
      return res.data
    } catch (e) {
      error.value = humanizeError(e)
      throw e
    }
  }

  async function remove(id) {
    error.value = ''
    try {
      await http.delete(`${resourcePath}${id}/`)
    } catch (e) {
      error.value = humanizeError(e)
      throw e
    }
  }

  async function retrieve(id) {
    error.value = ''
    try {
      const res = await http.get(`${resourcePath}${id}/`)
      return res.data
    } catch (e) {
      error.value = humanizeError(e)
      throw e
    }
  }

  return { items, loading, error, list, create, update, remove, retrieve }
}

function humanizeError(e) {
  const data = e?.response?.data
  if (!data) return 'Ошибка сети или сервера'
  if (typeof data === 'string') return data
  if (data.detail) return data.detail
  // Flatten DRF errors
  const parts = []
  for (const [k, v] of Object.entries(data)) {
    if (Array.isArray(v)) parts.push(`${k}: ${v.join(', ')}`)
    else parts.push(`${k}: ${String(v)}`)
  }
  return parts.join(' | ') || 'Ошибка запроса'
}
