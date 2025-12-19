import { axios } from './config'

const BASE = '/breed-diets'

export const getBreedDiets = (params = {}) => axios.get(BASE, { params }).then(r => r.data)
export const getBreedDiet = (id) => axios.get(`${BASE}/${id}/`).then(r => r.data)
export const createBreedDiet = (data) => axios.post(BASE + '/', data).then(r => r.data)
export const updateBreedDiet = (id, data) => axios.patch(`${BASE}/${id}/`, data).then(r => r.data)
export const deleteBreedDiet = (id) => axios.delete(`${BASE}/${id}/`).then(r => r.data)