import { axios } from './config'

const BASE = '/employments'

export const getEmployments = (params = {}) => axios.get(BASE, { params }).then(r => r.data)
export const createEmployment = (data) => axios.post(BASE + '/', data).then(r => r.data)
export const updateEmployment = (id, data) => axios.patch(`${BASE}/${id}/`, data).then(r => r.data)