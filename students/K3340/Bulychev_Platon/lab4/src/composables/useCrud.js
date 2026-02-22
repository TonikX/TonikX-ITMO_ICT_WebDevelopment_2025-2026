import { ref, onMounted } from 'vue'
import api from '../api'

export function useCrud(endpoint) {
  const items = ref([])
  const loading = ref(false)
  const load = async () => {
    loading.value = true
    const { data } = await api.get(`/api/${endpoint}/`)
    items.value = data
    loading.value = false
  }
  const create = async (item) => {
    await api.post(`/api/${endpoint}/`, item)
    await load()
  }
  const update = async (id, item) => {
    await api.put(`/api/${endpoint}/${id}/`, item)
    await load()
  }
  const remove = async (id) => {
    await api.delete(`/api/${endpoint}/${id}/`)
    await load()
  }
  onMounted(load)
  return { items, loading, load, create, update, remove }
}
