import api from './index'

export const fuelApi = {
  // Получить справочник топлива
  getFuelReference() {
    return api.get('/fuel-reference/')
  },
  
  // Получить проданное топливо
  getSoldFuel() {
    return api.get('/sold-fuel/')
  },
  
  // Получить цены на топливо
  getFuelPrices() {
    return api.get('/fuel-prices/')
  }
}