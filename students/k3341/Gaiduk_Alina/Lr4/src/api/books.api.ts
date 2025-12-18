import httpClient, { fetchAllPages } from './http'
import { Book, BookCreateUpdate, BookCopy } from '../types'

// объект с методами для работы с книгами
export const booksAPI = {
  // получить все книги
  getAll: async (): Promise<Book[]> => {
    try {
      //  fetchAllPages для загрузки всех страниц пагинированных данных
      const result = await fetchAllPages<Book>('/books/')
      // Возвращаем полученные книги
      return result
    } catch (error) {
      // загружаем хотя бы первую страницу, если не удалось загрузить все
      try {
        const response = await httpClient.get<any>('/books/')
        // извлекаем данные из ответа (может быть массив или объект с results)
        const data = response.data?.results || []
        // возвращаем массив
        return Array.isArray(data) ? data : []
      } catch (fallbackError) {
        return []
      }
    }
  },

  getById: async (id: number): Promise<Book> => {
    const response = await httpClient.get<Book>(`/books/${id}/`)
    return response.data
  },

  create: async (data: BookCreateUpdate): Promise<Book> => {
    const response = await httpClient.post<Book>('/books/', data)
    return response.data
  },

  update: async (id: number, data: Partial<BookCreateUpdate>): Promise<Book> => {
    const response = await httpClient.patch<Book>(`/books/${id}/`, data)
    return response.data
  },

  delete: async (id: number): Promise<void> => {
    await httpClient.delete(`/books/${id}/`)
  },

  // получить все экземпляры конкретной книги
  getCopies: async (id: number): Promise<BookCopy[]> => {
    try {
      // отправляем GET запрос для получения экземпляров книги
      const response = await httpClient.get<any>(`/books/${id}/copies/`)
      // этот endpoint может возвращать массив напрямую (many=True в сериализаторе)
      // Проверяем формат ответа: массив или объект с results
      const data = Array.isArray(response.data) ? response.data : (response.data?.results || [])
      // Возвращаем массив экземпляров
      return Array.isArray(data) ? data : []
    } catch (error) {
      return []
    }
  },
}


