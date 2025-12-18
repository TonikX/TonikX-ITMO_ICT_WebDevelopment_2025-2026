import httpClient, { fetchAllPages } from './http'
import { BookSection } from '../types'

// объект с методами для работы с разделами книг
export const sectionsAPI = {
  getAll: async (): Promise<BookSection[]> => {
    try {
      // используем функцию fetchAllPages для загрузки всех страниц
      return await fetchAllPages<BookSection>('/book-sections/')
    } catch (error) {
      return []
    }
  },

  getById: async (id: number): Promise<BookSection> => {
    const response = await httpClient.get<BookSection>(`/book-sections/${id}/`)
    return response.data
  },

  create: async (data: Omit<BookSection, 'section_id' | 'created_at' | 'updated_at'>): Promise<BookSection> => {
    const response = await httpClient.post<BookSection>('/book-sections/', data)
    return response.data
  },

  update: async (id: number, data: Partial<Omit<BookSection, 'section_id' | 'created_at' | 'updated_at'>>): Promise<BookSection> => {
    const response = await httpClient.patch<BookSection>(`/book-sections/${id}/`, data)
    return response.data
  },

  delete: async (id: number): Promise<void> => {
    await httpClient.delete(`/book-sections/${id}/`)
  },
}


