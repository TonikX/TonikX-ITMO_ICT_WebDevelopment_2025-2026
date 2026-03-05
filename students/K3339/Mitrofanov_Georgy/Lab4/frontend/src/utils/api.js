import axios from 'axios'
const baseURL = '/api'

const instance = axios.create({
  baseURL,
  withCredentials: true
})

function setAuth(token) {
  if (token) instance.defaults.headers.common['Authorization'] = `Bearer ${token}`
  else delete instance.defaults.headers.common['Authorization']
}

export default Object.assign(instance, { setAuth })