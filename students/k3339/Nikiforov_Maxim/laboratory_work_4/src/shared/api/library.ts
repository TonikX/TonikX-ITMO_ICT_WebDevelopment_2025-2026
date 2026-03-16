import { request } from './client'

export interface ReadingRoom {
  id: number
  number: string
  name: string
  capacity: number
  readers_count?: number
  total_books_count?: number
  created_at?: string
}

export interface Reader {
  id: number
  ticket_number: string
  full_name: string
  passport_number: string
  birth_date: string
  age?: number
  address: string
  phone_number: string
  education: string
  has_degree: boolean
  reading_room: number | null
  reading_room_name?: string | null
  registration_date: string
  unregistration_date?: string | null
  is_active: boolean
  active_books_count?: number
}

export interface Book {
  id: number
  title: string
  authors: string
  publisher: string
  publication_year: number
  section: string
  code: string
  total_copies?: number
  active_assignments_count?: number
  is_active: boolean
}

export interface BookCopy {
  id: number
  book: number
  book_title?: string
  reading_room: number
  reading_room_name?: string
  quantity: number
}

export interface BookAssignment {
  id: number
  book: number
  book_title?: string
  reader: number
  reader_name?: string
  reader_ticket?: string
  assignment_date: string
  return_date?: string | null
  is_returned: boolean
  days_since_assignment?: number | null
}

export interface Paginated<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export const readingRoomsApi = {
  list: (params?: { search?: string; ordering?: string }) =>
    request<Paginated<ReadingRoom>>('/api/reading-rooms/', { params: params as Record<string, string> }).then((r) => r.data),
  get: (id: number) => request<ReadingRoom>(`/api/reading-rooms/${id}/`).then((r) => r.data),
  create: (body: Partial<ReadingRoom>) =>
    request<ReadingRoom>('/api/reading-rooms/', { method: 'POST', body }).then((r) => r.data),
  update: (id: number, body: Partial<ReadingRoom>) =>
    request<ReadingRoom>(`/api/reading-rooms/${id}/`, { method: 'PATCH', body }).then((r) => r.data),
  delete: (id: number) => request(`/api/reading-rooms/${id}/`, { method: 'DELETE' }),
}

export const readersApi = {
  list: (params?: { is_active?: string; search?: string }) =>
    request<Paginated<Reader>>('/api/readers/', { params: params as Record<string, string> }).then((r) => r.data),
  get: (id: number) => request<Reader>(`/api/readers/${id}/`).then((r) => r.data),
  books: (id: number) => request<BookAssignment[]>(`/api/readers/${id}/books/`).then((r) => r.data),
  oldAssignments: () => request<Reader[]>('/api/readers/old_assignments/').then((r) => r.data),
  withRareBooks: () => request<Reader[]>('/api/readers/with_rare_books/').then((r) => r.data),
  youngReaders: () => request<{ count: number }>('/api/readers/young_readers/').then((r) => r.data),
  educationStats: () =>
    request<{ primary: number; secondary: number; higher: number; degree: number }>('/api/readers/education_stats/').then((r) => r.data),
  create: (body: Partial<Reader>) =>
    request<Reader>('/api/readers/', { method: 'POST', body }).then((r) => r.data),
  update: (id: number, body: Partial<Reader>) =>
    request<Reader>(`/api/readers/${id}/`, { method: 'PATCH', body }).then((r) => r.data),
  delete: (id: number) => request(`/api/readers/${id}/`, { method: 'DELETE' }),
}

export const booksApi = {
  list: (params?: { is_active?: string; search?: string }) =>
    request<Paginated<Book>>('/api/books/', { params: params as Record<string, string> }).then((r) => r.data),
  get: (id: number) => request<Book>(`/api/books/${id}/`).then((r) => r.data),
  create: (body: Partial<Book>) =>
    request<Book>('/api/books/', { method: 'POST', body }).then((r) => r.data),
  update: (id: number, body: Partial<Book>) =>
    request<Book>(`/api/books/${id}/`, { method: 'PATCH', body }).then((r) => r.data),
  delete: (id: number) => request(`/api/books/${id}/`, { method: 'DELETE' }),
}

export const bookCopiesApi = {
  list: (params?: Record<string, string>) =>
    request<Paginated<BookCopy>>('/api/book-copies/', { params }).then((r) => r.data),
  create: (body: Partial<BookCopy>) =>
    request<BookCopy>('/api/book-copies/', { method: 'POST', body }).then((r) => r.data),
  update: (id: number, body: Partial<BookCopy>) =>
    request<BookCopy>(`/api/book-copies/${id}/`, { method: 'PATCH', body }).then((r) => r.data),
}

export const bookAssignmentsApi = {
  list: (params?: { is_returned?: string }) =>
    request<Paginated<BookAssignment>>('/api/book-assignments/', { params: params as Record<string, string> }).then((r) => r.data),
  get: (id: number) => request<BookAssignment>(`/api/book-assignments/${id}/`).then((r) => r.data),
  create: (body: { book: number; reader: number }) =>
    request<BookAssignment>('/api/book-assignments/', { method: 'POST', body }).then((r) => r.data),
  returnBook: (id: number) =>
    request<BookAssignment>(`/api/book-assignments/${id}/return_book/`, { method: 'POST' }).then((r) => r.data),
  delete: (id: number) => request(`/api/book-assignments/${id}/`, { method: 'DELETE' }),
}

export const librarianApi = {
  registerReader: (body: Partial<Reader>) =>
    request<Reader>('/api/librarian-operations/register_reader/', { method: 'POST', body }).then((r) => r.data),
  unregisterOldReaders: () =>
    request<{ message: string; count: number }>('/api/librarian-operations/unregister_old_readers/', { method: 'POST' }).then((r) => r.data),
  writeOffBook: (bookId: number) =>
    request<{ message: string; book: Book }>('/api/librarian-operations/write_off_book/', {
      method: 'POST',
      body: { book_id: bookId },
    }).then((r) => r.data),
  acceptBook: (body: Partial<Book> & { reading_room_id?: number; quantity?: number }) =>
    request<Book>('/api/librarian-operations/accept_book/', { method: 'POST', body }).then((r) => r.data),
  monthlyReport: (month: number, year: number) =>
    request<{
      month: number
      year: number
      daily_stats: Array<{
        date: string
        books_count: number
        readers_count: number
        new_readers_count: number
        rooms: Array<{ room_id: number; room_name: string; books_count: number; readers_count: number; new_readers_count: number }>
      }>
      total_new_readers: number
    }>('/api/librarian-operations/monthly_report/', { params: { month: String(month), year: String(year) } }).then((r) => r.data),
}
