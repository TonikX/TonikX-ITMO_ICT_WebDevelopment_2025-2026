import httpClient, { fetchAllPages } from './http'
import { BookCopy, BookCopyCreate } from '../types'

// объект с методами для работы с экземплярами книг
export const copiesAPI = {
  getAll: async (): Promise<BookCopy[]> => {
    try {
      // используем функцию fetchAllPages для загрузки всех страниц пагинированных данных
      return await fetchAllPages<BookCopy>('/book-copies/')
    } catch (error) {
      return []
    }
  },

  getById: async (id: number): Promise<BookCopy> => {
    const response = await httpClient.get<BookCopy>(`/book-copies/${id}/`)
    return response.data
  },

  create: async (data: BookCopyCreate): Promise<BookCopy> => {
    const response = await httpClient.post<BookCopy>('/book-copies/', data)
    return response.data
  },

  update: async (id: number, data: Partial<BookCopyCreate>): Promise<BookCopy> => {
    const response = await httpClient.patch<BookCopy>(`/book-copies/${id}/`, data)
    return response.data
  },

  delete: async (id: number): Promise<void> => {
    await httpClient.delete(`/book-copies/${id}/`)
  },
}


