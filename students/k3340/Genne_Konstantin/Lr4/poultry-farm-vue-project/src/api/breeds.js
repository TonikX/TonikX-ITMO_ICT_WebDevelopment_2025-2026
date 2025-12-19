import { axios } from './config'

const BASE = '/breeds'

export const getBreeds = () => axios.get(BASE).then(r => r.data)
export const getBreed = (id) => axios.get(`${BASE}/${id}/`).then(r => r.data)
export const createBreed = (data) => axios.post(BASE + '/', data).then(r => r.data)
export const updateBreed = (id, data) => axios.patch(`${BASE}/${id}/`, data).then(r => r.data)
export const deleteBreed = (id) => axios.delete(`${BASE}/${id}/`).then(r => r.data)