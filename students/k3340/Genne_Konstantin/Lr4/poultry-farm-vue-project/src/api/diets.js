import { axios } from './config'

const BASE = '/diets'

export const getDiets = () => axios.get(BASE).then(r => r.data)
export const getDiet = (id) => axios.get(`${BASE}/${id}/`).then(r => r.data)
export const createDiet = (data) => axios.post(BASE + '/', data).then(r => r.data)
export const updateDiet = (id, data) => axios.patch(`${BASE}/${id}/`, data).then(r => r.data)
export const deleteDiet = (id) => axios.delete(`${BASE}/${id}/`).then(r => r.data)