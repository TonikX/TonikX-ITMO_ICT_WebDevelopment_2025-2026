import { axios } from './config'

const BASE = '/employee-cages'

export const getEmployeeCages = (params = {}) => axios.get(BASE, { params }).then(r => r.data)
export const createEmployeeCage = (data) => axios.post(BASE + '/', data).then(r => r.data)
export const updateEmployeeCage = (id, data) => axios.patch(`${BASE}/${id}/`, data).then(r => r.data)