import { defineStore } from 'pinia'
import { clientsApi } from '../api/clients'
import { useAuthStore } from '../stores/auth'

export const useClientsStore = defineStore('clients', {
  state: () => ({
    // Данные нового клиента
    newClient: {
      surname: '',
      name: '',
      patronymic: '',
      phone_number: '',
      address: ''
    },
    
    // Флаг нового клиента
    isNewClient: false,
    
    // Поиск по телефону
    searchPhone: '',
    foundClients: [],
    selectedClient: null,
    
    // Создание карты
    cardPeriod: 'month', // month, year, forever
    creatingCard: false,
    createdCard: null,
    error: null,
    loading: false
  }),
  
  getters: {
    canIssueCard: (state) => {
      if (state.isNewClient) {
        const phoneNumber = state.newClient.phone_number.replace(/\D/g, '')
        return (
          state.newClient.surname.trim() &&
          state.newClient.name.trim() &&
          state.newClient.patronymic.trim() &&
          phoneNumber.length >= 10 &&
          state.newClient.address.trim()
        )
      } else {
        return !!state.selectedClient
      }
    },
    
    formattedPhone: (state) => {
      const phone = state.newClient.phone_number || state.searchPhone
      if (!phone) return ''
      
      const cleaned = phone.replace(/\D/g, '')
      if (cleaned.length === 11 && (cleaned.startsWith('7') || cleaned.startsWith('8'))) {
        return `+7 (${cleaned.substring(1, 4)}) ${cleaned.substring(4, 7)}-${cleaned.substring(7, 9)}-${cleaned.substring(9, 11)}`
      }
      return phone
    }
  },
  
  actions: {
    // Сбросить форму (только поля ввода)
    resetInputForm() {
      this.newClient = {
        surname: '',
        name: '',
        patronymic: '',
        phone_number: '',
        address: ''
      }
      this.searchPhone = ''
      this.foundClients = []
      this.selectedClient = null
      this.cardPeriod = 'month'
      this.error = null
    },
    
    // Сбросить всё (включая созданную карту)
    resetAll() {
      this.resetInputForm()
      this.createdCard = null
      this.isNewClient = false
    },
    
    // Переключить режим нового клиента
    toggleNewClient(isNew) {
      this.isNewClient = isNew
      this.resetInputForm()
    },
    
    // Поиск клиентов по телефону
    async searchClients() {
      if (!this.searchPhone.trim()) {
        this.foundClients = []
        return
      }
      
      this.loading = true
      this.error = null
      
      try {
        const phoneNumber = this.searchPhone.replace(/\D/g, '')
        const response = await clientsApi.getClientsByPhone(phoneNumber)
        this.foundClients = response.data
      } catch (error) {
        this.error = error.response?.data || error.message
        console.error('Ошибка поиска клиентов:', error)
      } finally {
        this.loading = false
      }
    },
    
    // Выбрать клиента
    selectClient(client) {
      this.selectedClient = client
      
      this.newClient = {
        surname: client.surname,
        name: client.name,
        patronymic: client.patronymic,
        phone_number: client.phone_number ? client.phone_number.toString() : '',
        address: client.address
      }
    },
    
    // Выдать карту
    async issueCard() {
      if (!this.canIssueCard) {
        this.error = 'Заполните все обязательные поля'
        return { success: false }
      }
      
      this.creatingCard = true
      this.error = null
      
      try {
        const authStore = useAuthStore()
        const companyId = authStore.companyId
        
        if (!companyId) {
          throw new Error('Не удалось определить компанию')
        }
        
        let clientId
        
        // Если это новый клиент, сначала создаем клиента
        if (this.isNewClient) {
          // Проверяем номер телефона
          const phoneDigits = this.newClient.phone_number.replace(/\D/g, '')
          if (phoneDigits.length !== 11) {
            throw new Error('Номер телефона должен содержать 11 цифр')
          }
          
          const clientResponse = await clientsApi.createClient({
            ...this.newClient,
            phone_number: parseInt(phoneDigits, 10)
          })
          clientId = clientResponse.data.id_client
        } else {
          if (!this.selectedClient) {
            throw new Error('Клиент не выбран')
          }
          clientId = this.selectedClient.id_client
        }
        
        // Определяем даты для карты
        const startDate = new Date()
        let endDate = null
        
        switch (this.cardPeriod) {
          case 'month':
            endDate = new Date()
            endDate.setMonth(endDate.getMonth() + 1)
            break
          case 'year':
            endDate = new Date()
            endDate.setFullYear(endDate.getFullYear() + 1)
            break
          case 'forever':
            endDate = null
            break
          default:
            endDate = new Date()
            endDate.setMonth(endDate.getMonth() + 1)
        }
        
        // Форматируем даты для API
        const formatDate = (date) => {
          if (!date) return null
          return date.toISOString().split('T')[0]
        }
        
        // Создаем карту
        const cardData = {
          id_client: clientId,
          id_company: companyId,
          start_date: formatDate(startDate),
          end_date: endDate ? formatDate(endDate) : null,
          balance: '0.00',
          discount_percent: '0.00',
          discount_rub: '0.00'
        }
        
        const cardResponse = await clientsApi.createClientCard(cardData)
        this.createdCard = cardResponse.data
        
        // Сбрасываем форму
        this.resetInputForm()
        
        return { 
          success: true, 
          cardId: cardResponse.data.id_card 
        }
        
      } catch (error) {
        this.error = error.response?.data || error.message
        console.error('Ошибка создания карты:', error)
        return { success: false }
      } finally {
        this.creatingCard = false
      }
    },
    
    // Установить период карты
    setCardPeriod(period) {
      this.cardPeriod = period
    },
    
    // Очистить ошибку
    clearError() {
      this.error = null
    },
    
    // Очистить созданную карту
    clearCreatedCard() {
      this.createdCard = null
    }
  }
})