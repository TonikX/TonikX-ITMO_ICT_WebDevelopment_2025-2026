import httpClient, { fetchAllPages } from './http'
import { Hall, Reader } from '../types'

// Экспортируемый объект с методами для работы с залами
export const hallsAPI = {
  // Получить все залы (загружает все страницы при пагинации)
  getAll: async (): Promise<Hall[]> => {
    try {
      // Используем функцию fetchAllPages для загрузки всех страниц пагинированных данных
      return await fetchAllPages<Hall>('/halls/')
    } catch (error) {
      // В случае ошибки выводим в консоль и возвращаем пустой массив
      console.error('❌ Halls API getAll error:', error)
      return []
    }
  },

  // Получить зал по ID
  getById: async (id: number): Promise<Hall> => {
    // Отправляем GET запрос для получения конкретного зала
    const response = await httpClient.get<Hall>(`/halls/${id}/`)
    // Возвращаем данные зала из ответа
    return response.data
  },

  // Создать новый зал (без системных полей hall_id, created_at, updated_at)
  create: async (data: Omit<Hall, 'hall_id' | 'created_at' | 'updated_at'>): Promise<Hall> => {
    // Отправляем POST запрос с данными нового зала
    const response = await httpClient.post<Hall>('/halls/', data)
    // Возвращаем данные созданного зала
    return response.data
  },

  // Обновить данные зала (частичное обновление через PATCH)
  update: async (id: number, data: Partial<Omit<Hall, 'hall_id' | 'created_at' | 'updated_at'>>): Promise<Hall> => {
    // Отправляем PATCH запрос с обновленными данными
    const response = await httpClient.patch<Hall>(`/halls/${id}/`, data)
    // Возвращаем данные обновленного зала
    return response.data
  },

  // Удалить зал по ID
  delete: async (id: number): Promise<void> => {
    // Отправляем DELETE запрос для удаления зала
    await httpClient.delete(`/halls/${id}/`)
  },

  // Получить всех читателей конкретного зала
  getReaders: async (id: number): Promise<Reader[]> => {
    try {
      // Отправляем GET запрос для получения читателей зала
      const response = await httpClient.get<any>(`/halls/${id}/readers/`)
      // Этот endpoint может возвращать массив напрямую (many=True в сериализаторе)
      // Проверяем формат ответа: массив или объект с results
      const data = Array.isArray(response.data) ? response.data : (response.data?.results || [])
      // Возвращаем массив читателей (проверяем, что это массив)
      return Array.isArray(data) ? data : []
    } catch (error) {
      // В случае ошибки выводим в консоль и возвращаем пустой массив
      console.error('❌ Halls API getReaders error:', error)
      return []
    }
  },
}


