import httpClient, { fetchAllPages } from './http'
import { Publisher, Book } from '../types'

// объект с методами для работы с издательствами
export const publishersAPI = {
  getAll: async (): Promise<Publisher[]> => {
    try {
      // используем функцию fetchAllPages для загрузки всех страниц
      return await fetchAllPages<Publisher>('/publishers/')
    } catch (error) {
      return []
    }
  },

  getById: async (id: number): Promise<Publisher> => {
    const response = await httpClient.get<Publisher>(`/publishers/${id}/`)
    return response.data
  },

  create: async (data: Omit<Publisher, 'publisher_id' | 'created_at' | 'updated_at'>): Promise<Publisher> => {
    const response = await httpClient.post<Publisher>('/publishers/', data)
    return response.data
  },

  update: async (id: number, data: Partial<Omit<Publisher, 'publisher_id' | 'created_at' | 'updated_at'>>): Promise<Publisher> => {
    const response = await httpClient.patch<Publisher>(`/publishers/${id}/`, data)
    return response.data
  },

  delete: async (id: number): Promise<void> => {
    await httpClient.delete(`/publishers/${id}/`)
  },

  // получить все книги конкретного издательства
  getBooks: async (id: number): Promise<Book[]> => {
    try {
      // Отправляем GET запрос для получения книг издательства
      const response = await httpClient.get<any>(`/publishers/${id}/books/`)
      // может возвращать массив напрямую (many=True в сериализаторе)
      // проверяем формат ответа: массив или объект с results
      const data = Array.isArray(response.data) ? response.data : (response.data?.results || [])
      // возвращаем массив книг (проверяем, что это массив)
      return Array.isArray(data) ? data : []
    } catch (error) {
      return []
    }
  },
}


