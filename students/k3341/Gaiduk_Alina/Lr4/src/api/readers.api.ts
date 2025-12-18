import httpClient, { fetchAllPages } from './http'
import { Reader, ReaderCreate, BookIssue, AgeStatistics, EducationStatistics } from '../types'

// объект с методами для работы с читателями
export const readersAPI = {
  getAll: async (): Promise<Reader[]> => {
    try {
      // используем функцию fetchAllPages для загрузки всех страниц пагинированных данных
      return await fetchAllPages<Reader>('/readers/')
    } catch (error) {
      return []
    }
  },

  getById: async (id: number): Promise<Reader> => {
    const response = await httpClient.get<Reader>(`/readers/${id}/`)
    return response.data
  },

  create: async (data: ReaderCreate): Promise<Reader> => {
    const response = await httpClient.post<Reader>('/readers/', data)
    return response.data
  },


  update: async (id: number, data: Partial<ReaderCreate & { is_active?: boolean; last_reregistration_date?: string | null }>): Promise<Reader> => {
    const response = await httpClient.patch<Reader>(`/readers/${id}/`, data)
    return response.data
  },

  delete: async (id: number): Promise<void> => {
    await httpClient.delete(`/readers/${id}/`)
  },

  getBooks: async (id: number): Promise<BookIssue[]> => {
    try {
      const response = await httpClient.get<any>(`/readers/${id}/books/`)
      // может возвращать массив напрямую (many=True в сериализаторе)
      // проверяем формат ответа: массив или объект с results
      const data = Array.isArray(response.data) ? response.data : (response.data?.results || [])
      // возвращаем массив выдач (проверяем, что это массив)
      return Array.isArray(data) ? data : []
    } catch (error) {
      return []
    }
  },

  // получить статистику по возрасту читателей
  getAgeStatistics: async (age: number): Promise<AgeStatistics> => {
    const response = await httpClient.get<AgeStatistics>(`/readers/statistics/age/?age=${age}`)
    return response.data
  },

  // получить статистику по образованию читателей
  getEducationStatistics: async (): Promise<EducationStatistics> => {
    const response = await httpClient.get<EducationStatistics>('/readers/statistics/education/')
    return response.data
  },
}


