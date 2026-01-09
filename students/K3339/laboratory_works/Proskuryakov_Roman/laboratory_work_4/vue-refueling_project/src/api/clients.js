import api from './index'

export const clientsApi = {
  // Получить клиентов по номеру телефона
  getClientsByPhone(phoneNumber) {
    return api.get('/clients/', { 
      params: { 
        phone_number: phoneNumber
      } 
    })
  },

  // Создать нового клиента
  createClient(clientData) {
    return api.post('/clients/', clientData)
  },
  
  // Создать карту клиента
  createClientCard(cardData) {
    return api.post('/client-cards/', cardData)
  },
  
  // Получить все карты клиента
  getClientCards(clientId) {
    return api.get('/client-cards/', { params: { id_client: clientId } })
  }
}