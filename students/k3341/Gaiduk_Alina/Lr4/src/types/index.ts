export * from './common'

// базовые поля с временными метками
export interface TimestampFields {
  created_at: string
  updated_at: string
}


export interface Author extends TimestampFields {
  author_id: number
  full_name: string
}

export interface Publisher extends TimestampFields {
  publisher_id: number
  name: string
}

export interface BookSection extends TimestampFields {
  section_id: number
  name: string
}

export interface Hall extends TimestampFields {
  hall_id: number
  hall_number: number
  name: string
  capacity: number
}

export interface Book extends TimestampFields {
  book_id: number
  title: string
  publisher: number | null
  publisher_name?: string
  publish_year: number | null
  section: number | null
  section_name?: string
  cipher: string
  authors: Author[]
}

// интерфейс для создания или обновления книги
export interface BookCreateUpdate {
  title: string
  publisher?: number | null
  publish_year?: number | null
  section?: number | null
  cipher: string
  author_ids?: number[]
}


export interface Reader extends TimestampFields {
  reader_id: number
  card_number: string
  full_name: string
  passport_number: string
  birth_date: string
  age: number
  address: string | null
  phone: string | null
  education_level: 'начальное' | 'среднее' | 'высшее' | null
  has_academic_degree: boolean
  hall: number | null
  hall_name?: string
  registration_date: string
  last_reregistration_date: string | null
  is_active: boolean
}

export interface ReaderCreate {
  card_number: string
  full_name: string
  passport_number: string
  birth_date: string
  address?: string | null
  phone?: string | null
  education_level?: 'начальное' | 'среднее' | 'высшее' | null
  has_academic_degree?: boolean
  hall?: number | null
  last_reregistration_date?: string | null
}


export interface BookCopy extends TimestampFields {
  copy_id: number
  book: number
  book_title?: string
  hall: number
  hall_name?: string
  inventory_number: string
  registration_date: string
  writeoff_date: string | null
  is_written_off: boolean
}

// интерфейс для создания или обновления экземпляра книги
export interface BookCopyCreate {
  book: number
  hall: number
  inventory_number: string
  writeoff_date?: string | null
  is_written_off?: boolean
}


export interface BookIssue extends TimestampFields {
  issue_id: number
  reader: number
  reader_name?: string
  reader_card?: string
  copy: number
  copy_inventory?: string
  book_title?: string
  hall: number
  hall_name?: string
  issue_date: string
  return_date: string | null
  is_returned: boolean
}

// интерфейс для создания выдачи книги
export interface BookIssueCreate {
  reader: number
  copy: number
  hall: number
}

// интерфейс для остатков книг по залам
export interface HallBookStock extends TimestampFields {
  id?: number
  hall: number
  hall_name?: string
  book: number
  book_title?: string
  copies_total: number
}


export interface HallBookStockCreate {
  hall: number
  book: number
  copies_total: number
}


export interface Staff extends TimestampFields {
  staff_id: number
  login: string
  email: string
}

export interface StaffRegister {
  login: string
  email: string
  password: string
  registration_key: string
}


export interface LoginCredentials {
  login: string
  password: string
}

// интерфейс для ответа с токенами аутентификации
export interface TokenResponse {
  access: string
  refresh: string
}

//интерфейс для данных принятия книги в фонд
export interface BookAcceptData {
  book_id?: number | null
  title?: string
  publisher?: number | null
  publish_year?: number | null
  section?: number | null
  cipher?: string
  author_ids?: number[]
  hall: number
  inventory_number: string
}

// интерфейс для статистики по образованию читателей
export interface EducationStatistics {
  total: number // Общее количество читателей
  percentages: {
    начальное: number
    среднее: number
    высшее: number
    не_указано: number
    учёная_степень: number
  }
}

export interface AgeStatistics {
  max_age: number
  readers_count: number
}

// интерфейс для периода месячного отчета
export interface MonthlyReportPeriod {
  year: number
  month: number
  start_date: string
  end_date: string
}

// интерфейс для статистики по залу за день
export interface HallDailyStats {
  hall_name: string
  books_count: number
  readers_count: number
}

// интерфейс для дневной статистики
export interface DailyStatistics {
  date: string
  halls: Record<number, HallDailyStats> // объект с статистикой по каждому залу (ключ - ID зала)
  total: {
    books_count: number
    readers_count: number
  }
}

// интерфейс для статистики новых читателей по залам
export interface NewReadersByHall {
  hall_id: number
  hall_name: string
  new_readers_count: number
}

// интерфейс для месячного отчета
export interface MonthlyReport {
  period: MonthlyReportPeriod
  daily_statistics: DailyStatistics[] // массив дневной статистики за весь период
  new_readers: {
    by_hall: NewReadersByHall[] // статистика новых читателей по каждому залу
    total: number
  }
}

