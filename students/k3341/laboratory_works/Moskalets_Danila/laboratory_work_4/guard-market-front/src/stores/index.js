import { createPinia } from 'pinia'

const pinia = createPinia()

export default pinia

// Экспортируем все stores для удобного импорта
export * from './auth'
export * from './companies'
export * from './services'
export * from './favorites'
export * from './reviews'