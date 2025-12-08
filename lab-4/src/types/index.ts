// Типы для API ответов

export interface Newspaper {
  id: number
  title: string
  publication_index: string
  editor_first_name: string
  editor_last_name: string
  editor_middle_name?: string
  editor_full_name: string
  price_per_copy: string
}

export interface PrintingHouse {
  id: number
  name: string
  address: string
  is_active: boolean
}

export interface PostOffice {
  id: number
  number: string
  address: string
}

export interface Distribution {
  id: number
  post_office: number
  newspaper: number
  printing_house: number
  quantity: number
  post_office_number?: string
  post_office_address?: string
  newspaper_title?: string
  newspaper_index?: string
  printing_house_name?: string
  printing_house_address?: string
}

export interface PrintingRun {
  id: number
  newspaper: Newspaper
  circulation: number
}

export interface DistributionDetail {
  id: number
  newspaper: Newspaper
  printing_house: PrintingHouse
  quantity: number
}

// Типы для детальных представлений
export interface NewspaperFullDetail extends Newspaper {
  printing_runs: PrintingRun[]
  distributions: DistributionDetail[]
}

export interface PrintingHouseFullDetail extends PrintingHouse {
  printing_runs: PrintingRun[]
}

export interface PostOfficeFullDetail extends PostOffice {
  distributions: DistributionDetail[]
}

// Типы для пагинации
export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

// Типы для форм
export interface NewspaperForm {
  title: string
  publication_index: string
  editor_first_name: string
  editor_last_name: string
  editor_middle_name: string
  price_per_copy: string
}

export interface PrintingHouseForm {
  name: string
  address: string
  is_active: boolean
}

export interface PostOfficeForm {
  number: string
  address: string
}

export interface DistributionForm {
  post_office: number | null
  newspaper: number | null
  printing_house: number | null
  quantity: string
}

// Типы для отчетов
export interface PrintingHouseReport {
  printing_house: PrintingHouse
  total_newspapers: number
  newspapers: {
    newspaper: string
    circulation: number
    distributions: {
      post_office_number: string
      post_office_address: string
      quantity: number
    }[]
    total_distributed: number
  }[]
}

// Типы для опций таблицы
export interface TableOptions {
  page?: number
  itemsPerPage?: number
  sortBy?: { key: string; order: string }[]
}

// Типы для правил валидации
export type ValidationRule = (v: string | number | null | undefined) => boolean | string

