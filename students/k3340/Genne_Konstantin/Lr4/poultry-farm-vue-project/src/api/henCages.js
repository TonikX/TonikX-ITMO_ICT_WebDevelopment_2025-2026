import { axios } from './config'

const BASE = '/hen-cages'

export const getHenCages = (params = {}) => axios.get(BASE, { params }).then(r => r.data)
export const createHenCage = (data) => axios.post(BASE + '/', data).then(r => r.data)
export const updateHenCage = (id, data) => axios.patch(`/hen-cages/${id}/`, data).then(r => r.data)