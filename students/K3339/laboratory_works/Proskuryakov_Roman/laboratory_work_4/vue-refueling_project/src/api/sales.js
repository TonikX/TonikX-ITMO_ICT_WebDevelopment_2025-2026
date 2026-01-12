import api from './index'

export const salesApi = {
  // Получить цены на топливо текущей станции
  getStationPrices() {
    return api.get('/my-station-prices/')
  },
  
  // Рассчитать оплату с учетом скидки
  calculatePayment(data) {
    return api.post('/calculate-payment/', data)
  },
  
  // Выполнить оплату топлива
  executeFuelPayment(data) {
    return api.post('/execute-fuel-payment/', data)
  }
}