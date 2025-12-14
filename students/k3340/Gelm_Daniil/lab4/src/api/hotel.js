import api from './axios'

export const hotelAPI = {
  rooms: {
    list() {
      return api.get('/api/rooms/')
    },
    get(id) {
      return api.get(`/api/rooms/${id}/`)
    },
    create(data) {
      return api.post('/api/rooms/', data)
    },
    update(id, data) {
      return api.put(`/api/rooms/${id}/`, data)
    },
    delete(id) {
      return api.delete(`/api/rooms/${id}/`)
    },
    available() {
      return api.get('/api/rooms/available/')
    }
  },
  guests: {
    list() {
      return api.get('/api/guests/')
    },
    get(id) {
      return api.get(`/api/guests/${id}/`)
    },
    create(data) {
      return api.post('/api/guests/', data)
    },
    update(id, data) {
      return api.put(`/api/guests/${id}/`, data)
    },
    delete(id) {
      return api.delete(`/api/guests/${id}/`)
    }
  },
  stays: {
    list() {
      return api.get('/api/stays/')
    },
    get(id) {
      return api.get(`/api/stays/${id}/`)
    },
    create(data) {
      return api.post('/api/stays/', data)
    },
    update(id, data) {
      return api.put(`/api/stays/${id}/`, data)
    },
    delete(id) {
      return api.delete(`/api/stays/${id}/`)
    },
    current() {
      return api.get('/api/stays/current/')
    }
  }
}

