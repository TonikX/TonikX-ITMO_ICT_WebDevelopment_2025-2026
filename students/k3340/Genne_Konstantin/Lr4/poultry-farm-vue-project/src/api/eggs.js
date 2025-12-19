import { axios } from './config'

const BASE = '/hen-eggs'

export const getEggRecords = (params = {}) => axios.get(BASE, { params }).then(r => r.data)
export const createEggRecord = (data) => axios.post(BASE + '/', data).then(r => r.data)
export const deleteEggRecord = (id) => axios.delete(`${BASE}/${id}/`).then(r => r.data)