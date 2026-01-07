import { defineStore } from 'pinia'
import { salesApi } from '../api/sales'

export const useSalesStore = defineStore('sales', {
  state: () => ({
    stationPrices: [],
    selectedPrice: null,
    liters: '',
    cardId: '',
    cardApplied: false,
    calculation: {
      initialAmount: 0,
      finalAmount: 0,
      discount: 0,
      sufficientBalance: false,
      cardActive: false,
      cardFound: false
    },
    loading: false,
    error: null,
    successMessage: null
  }),
  
  getters: {
    // Рассчитать начальную сумму
    calculatedInitialAmount: (state) => {
      if (!state.selectedPrice || !state.liters) return 0
      const liters = parseFloat(state.liters)
      if (isNaN(liters) || liters <= 0) return 0
      return state.selectedPrice.per_liter * liters
    },
    
    // Можно ли оплатить
    canPay: (state) => {
      return (
        state.selectedPrice &&
        state.liters &&
        parseFloat(state.liters) > 0 &&
        state.cardApplied &&
        state.cardId &&
        state.calculation.finalAmount > 0 &&
        state.calculation.sufficientBalance &&
        state.calculation.cardActive
      )
    },
    
    // Форматированная строка для отображения
    paymentString: (state) => {
      if (!state.calculation.initialAmount) return ''
      const discount = state.calculation.initialAmount - state.calculation.finalAmount
      return `${state.calculation.initialAmount.toFixed(2)} - ${discount.toFixed(2)} = ${state.calculation.finalAmount.toFixed(2)}`
    }
  },
  
  actions: {
    async loadStationPrices() {
      this.loading = true
      this.error = null
      
      try {
        const response = await salesApi.getStationPrices()
        this.stationPrices = response.data
        
        // Добавляем дополнительную информацию для отображения
        this.stationPrices = this.stationPrices.map(price => ({
          ...price,
          fuel_info: this.extractFuelInfo(price)
        }))
        
      } catch (error) {
        this.error = error.response?.data || error.message
        console.error('Ошибка загрузки цен:', error)
      } finally {
        this.loading = false
      }
    },
    
    // Извлечь информацию о топливе из объекта
    extractFuelInfo(price) {
      if (!price.sold_fuel?.id_produced_fuel?.id_kind_fuel) return 'Неизвестное топливо'
      
      const fuel = price.sold_fuel.id_produced_fuel.id_kind_fuel
      return `${fuel.title} (${fuel.brand}, ${this.getSeasonText(fuel.season)})`
    },
    
    getSeasonText(season) {
      const seasons = {
        1: 'Летнее',
        2: 'Зимнее',
        3: 'Всесезонное'
      }
      return seasons[season] || `Сезон ${season}`
    },
    
    // Выбрать цену
    selectPrice(price) {
      this.selectedPrice = price
      this.recalculateInitialAmount()
    },
    
    // Изменить количество литров
    setLiters(value) {
      this.liters = value
      this.recalculateInitialAmount()
    },
    
    // Применить карту
    async applyCard() {
      if (!this.cardId) {
        this.cardApplied = false
        this.calculation = {
          initialAmount: this.calculatedInitialAmount,
          finalAmount: this.calculatedInitialAmount,
          discount: 0,
          sufficientBalance: false,
          cardActive: false,
          cardFound: false
        }
        return
      }
      
      this.loading = true
      this.error = null
      
      try {
        const response = await salesApi.calculatePayment({
          id_card: parseInt(this.cardId),
          initial_amount: this.calculatedInitialAmount
        })
        
        this.cardApplied = true
        this.calculation = {
          initialAmount: this.calculatedInitialAmount,
          finalAmount: response.data.final_amount,
          discount: this.calculatedInitialAmount - response.data.final_amount,
          sufficientBalance: response.data.sufficient_balance,
          cardActive: true,
          cardFound: true
        }
        
      } catch (error) {
        this.cardApplied = false
        
        // Обработка ошибок
        if (error.response?.status === 404) {
          this.calculation.cardFound = false
          this.error = 'Карта не найдена'
        } else if (error.response?.status === 400 && error.response.data?.detail) {
          this.calculation.cardActive = false
          this.error = error.response.data.detail
        } else {
          this.error = error.response?.data || error.message
        }
        
        this.calculation = {
          initialAmount: this.calculatedInitialAmount,
          finalAmount: this.calculatedInitialAmount,
          discount: 0,
          sufficientBalance: false,
          cardActive: false,
          cardFound: false
        }
      } finally {
        this.loading = false
      }
    },
    
    // Пересчитать начальную сумму
    recalculateInitialAmount() {
      const initialAmount = this.calculatedInitialAmount
      
      // Если карта не применена, просто обновляем начальную сумму
      if (!this.cardApplied) {
        this.calculation.initialAmount = initialAmount
        this.calculation.finalAmount = initialAmount
        this.calculation.discount = 0
        return
      }
      
      // Если карта применена, нужно пересчитать скидку
      // Для этого нужно вызвать API снова
      this.applyCard()
    },
    
    // Выполнить оплату
    async executePayment() {
      if (!this.canPay) {
        this.error = 'Невозможно выполнить оплату. Проверьте все поля.'
        return { success: false }
      }
      
      this.loading = true
      this.error = null
      this.successMessage = null
      
      try {
        const response = await salesApi.executeFuelPayment({
          id_fuel_price: this.selectedPrice.id_fuel_price,
          liters: parseFloat(this.liters),
          id_card: parseInt(this.cardId)
        })
        
        if (response.data.success) {
          this.successMessage = 'Платёж прошёл успешно'
          
          // Очищаем все поля
          this.resetForm()
          
          // Перезагружаем цены (на случай если они изменились)
          await this.loadStationPrices()
          
          return { success: true }
        } else {
          this.error = response.data.detail || 'Ошибка при выполнении платежа'
          return { success: false }
        }
        
      } catch (error) {
        this.error = error.response?.data?.detail || error.message || 'Ошибка при выполнении платежа'
        console.error('Ошибка оплаты:', error)
        return { success: false }
      } finally {
        this.loading = false
      }
    },
    
    // Сбросить форму
    resetForm() {
      this.selectedPrice = null
      this.liters = ''
      this.cardId = ''
      this.cardApplied = false
      this.calculation = {
        initialAmount: 0,
        finalAmount: 0,
        discount: 0,
        sufficientBalance: false,
        cardActive: false,
        cardFound: false
      }
    },
    
    // Очистить ошибку
    clearError() {
      this.error = null
    },
    
    // Очистить сообщение об успехе
    clearSuccessMessage() {
      this.successMessage = null
    }
  }
})