import httpClient, { fetchAllPages } from './http'
import { Author } from '../types'

//  объект с методами для работы с авторами
export const authorsAPI = {
  // получить всех авторов
  getAll: async (): Promise<Author[]> => {
    try {
      // используем функцию fetchAllPages для загрузки всех страниц пагинированных данных
      return await fetchAllPages<Author>('/authors/')
    } catch (error) {
      // в случае ошибки возвращаем пустой массив
      return []
    }
  },

  // получить автора по ID
  getById: async (id: number): Promise<Author> => {
    // отправляем GET запрос для получения конкретного автора
    const response = await httpClient.get<Author>(`/authors/${id}/`)
    return response.data
  },

  // создать нового автора
  create: async (data: Omit<Author, 'author_id' | 'created_at' | 'updated_at'>): Promise<Author> => {
    const response = await httpClient.post<Author>('/authors/', data)
    return response.data
  },

  // обновить (PATCH)
  update: async (id: number, data: Partial<Omit<Author, 'author_id' | 'created_at' | 'updated_at'>>): Promise<Author> => {
    // отправляем PATCH запрос с обновленными данными
    const response = await httpClient.patch<Author>(`/authors/${id}/`, data)
    return response.data
  },

  // удалить по ID
  delete: async (id: number): Promise<void> => {
    await httpClient.delete(`/authors/${id}/`)
  },
}


