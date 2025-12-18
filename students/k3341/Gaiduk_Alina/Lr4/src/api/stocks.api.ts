import httpClient, { fetchAllPages } from './http'
import { HallBookStock, HallBookStockCreate } from '../types'

// объект с методами для работы с остатками книг по залам
export const stocksAPI = {
  getAll: async (): Promise<HallBookStock[]> => {
    try {
      return await fetchAllPages<HallBookStock>('/hall-book-stocks/')
    } catch (error) {
      return []
    }
  },


  getById: async (id: number): Promise<HallBookStock> => {
    const response = await httpClient.get<HallBookStock>(`/hall-book-stocks/${id}/`)
    return response.data
  },

  create: async (data: HallBookStockCreate): Promise<HallBookStock> => {
    const response = await httpClient.post<HallBookStock>('/hall-book-stocks/', data)
    return response.data
  },

  update: async (id: number, data: Partial<HallBookStockCreate>): Promise<HallBookStock> => {
    const response = await httpClient.patch<HallBookStock>(`/hall-book-stocks/${id}/`, data)
    return response.data
  },

  delete: async (id: number): Promise<void> => {
    await httpClient.delete(`/hall-book-stocks/${id}/`)
  },
}


