import { axios } from './config'

const BASE = '/hens'

export const getHens = () => axios.get(BASE).then(r => r.data)
export const getHenDetail = (id) => axios.get(`/hens/${id}/detail/`).then(r => r.data)
export const createHen = (data) => axios.post(BASE + '/', data).then(r => r.data)
export const updateHen = (id, data) => axios.patch(`${BASE}/${id}/`, data).then(r => r.data)
// Удаление запрещено