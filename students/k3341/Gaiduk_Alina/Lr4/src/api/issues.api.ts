import httpClient, { fetchAllPages } from './http'
import { BookIssue, BookIssueCreate } from '../types'

// объект с методами для работы с выдачами книг
export const issuesAPI = {
  getAll: async (): Promise<BookIssue[]> => {
    try {
      // используем функцию fetchAllPages для загрузки всех страниц
      return await fetchAllPages<BookIssue>('/book-issues/')
    } catch (error) {
      return []
    }
  },

  getById: async (id: number): Promise<BookIssue> => {
    const response = await httpClient.get<BookIssue>(`/book-issues/${id}/`)
    return response.data
  },

  create: async (data: BookIssueCreate): Promise<BookIssue> => {
    const response = await httpClient.post<BookIssue>('/book-issues/', data)
    return response.data
  },

  update: async (id: number, data: Partial<BookIssue>): Promise<BookIssue> => {
    const response = await httpClient.patch<BookIssue>(`/book-issues/${id}/`, data)
    return response.data
  },

  delete: async (id: number): Promise<void> => {
    await httpClient.delete(`/book-issues/${id}/`)
  },

  // получить список просроченных выдач
  getOverdue: async (): Promise<BookIssue[]> => {
    try {
      const response = await httpClient.get<any>('/book-issues/overdue/')
      // может возвращать массив напрямую (many=True в сериализаторе)
      // проверяем формат ответа: массив или объект с results
      const data = Array.isArray(response.data) ? response.data : (response.data?.results || [])
      // возвращаем массив просроченных выдач (проверяем, что это массив)
      return Array.isArray(data) ? data : []
    } catch (error) {
      return []
    }
  },

  // получить список редких книг
  getRareBooks: async (): Promise<BookIssue[]> => {
    try {
      const response = await httpClient.get<any>('/book-issues/rare-books/')
      // может возвращать массив напрямую (many=True в сериализаторе)
      // проверяем формат ответа: массив или объект с results
      const data = Array.isArray(response.data) ? response.data : (response.data?.results || [])
      // возвращаем массив редких книг (проверяем, что это массив)
      return Array.isArray(data) ? data : []
    } catch (error) {
      return []
    }
  },

  // вернуть книгу (записать дату возврата)
  returnBook: async (id: number, return_date: string): Promise<BookIssue> => {
    // PATCH запрос для обновления даты возврата книги
    const response = await httpClient.patch<BookIssue>(`/book-issues/${id}/`, {
      return_date, // передаем дату возврата в теле запроса
    })
    return response.data
  },
}


