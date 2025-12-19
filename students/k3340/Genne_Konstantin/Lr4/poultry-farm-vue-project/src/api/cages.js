import { axios } from './config'

const BASE = '/cages'

export const getCages = () => axios.get(BASE).then(r => r.data)
export const getCage = (id) => axios.get(`${BASE}/${id}/`).then(r => r.data)
export const getCageDetail = (id) => axios.get(`/cages/${id}/detail/`).then(r => r.data)
export const createCage = (data) => axios.post(BASE + '/', data).then(r => r.data)
export const deleteCage = (id) => axios.delete(`${BASE}/${id}/`).then(r => r.data)

// Обновление запрещено