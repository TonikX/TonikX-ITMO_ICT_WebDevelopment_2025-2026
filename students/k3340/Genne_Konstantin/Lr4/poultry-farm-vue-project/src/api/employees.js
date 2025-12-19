import { axios } from './config'

const BASE = '/employees'

export const getEmployees = () => axios.get(BASE).then(r => r.data)
export const getEmployee = (id) => axios.get(`/employees/${id}/`).then(r => r.data)
export const getEmployeeDetail = (id) => axios.get(`/employees/${id}/detail/`).then(r => r.data)
export const createEmployee = (data) => axios.post(BASE + '/', data).then(r => r.data)
export const updateEmployee = (id, data) => axios.patch(`${BASE}/${id}/`, data).then(r => r.data)