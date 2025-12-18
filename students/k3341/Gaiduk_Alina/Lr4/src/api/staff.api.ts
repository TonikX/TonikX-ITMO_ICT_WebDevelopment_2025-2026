import httpClient, { fetchAllPages } from './http'
import { Staff, Reader, ReaderCreate, BookCopy, BookAcceptData, MonthlyReport, StaffRegister } from '../types'

// объект с методами для работы с сотрудниками и их функциями
export const staffAPI = {
  getAll: async (): Promise<Staff[]> => {
    try {
      // используем функцию fetchAllPages для загрузки всех страниц
      return await fetchAllPages<Staff>('/staff/')
    } catch (error) {
      return []
    }
  },

  getById: async (id: number): Promise<Staff> => {
    const response = await httpClient.get<Staff>(`/staff/${id}/`)
    return response.data
  },

  update: async (id: number, data: Partial<Omit<Staff, 'staff_id' | 'created_at' | 'updated_at'>>): Promise<Staff> => {
    const response = await httpClient.patch<Staff>(`/staff/${id}/`, data)
    return response.data
  },

  delete: async (id: number): Promise<void> => {
    await httpClient.delete(`/staff/${id}/`)
  },

  registerReader: async (data: ReaderCreate): Promise<Reader> => {
    const response = await httpClient.post<Reader>('/staff/register-reader/', data)
    return response.data
  },

  registerStaff: async (data: StaffRegister): Promise<Staff> => {
    const response = await httpClient.post<Staff>('/staff/register-staff/', data)
    return response.data
  },

  deactivateOldReaders: async (): Promise<{ deactivated_count: number; message: string }> => {
    const response = await httpClient.post<{ deactivated_count: number; message: string }>(
      '/staff/deactivate-old-readers/'
    )
    return response.data
  },

  // списать книгу
  writeoffBook: async (copyId: number): Promise<BookCopy> => {
    const response = await httpClient.post<BookCopy>('/staff/writeoff-book/', {
      copy_id: copyId, // передаем ID экземпляра книги для списания
    })
    return response.data
  },

  // принять книгу в фонд (создать новый экземпляр или добавить к существующей книге)
  acceptBook: async (data: BookAcceptData): Promise<BookCopy> => {
    const response = await httpClient.post<BookCopy>('/staff/accept-book/', data)
    return response.data
  },

  // получить месячный отчёт по выдачам книг
  getMonthlyReport: async (year: number, month: number): Promise<MonthlyReport> => {
    // отправляем GET запрос с параметрами года и месяца в query string
    const response = await httpClient.get<MonthlyReport>(
      `/staff/monthly-report/?year=${year}&month=${month}`
    )
    return response.data
  },
}

