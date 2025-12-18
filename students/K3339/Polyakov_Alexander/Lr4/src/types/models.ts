export interface Manufacturer {
  id: number
  name: string
  tax_id?: string | null
  country?: string | null
  contact_info?: string
}

export interface Product {
  id: number
  code: string
  name: string
  manufacturer: number
  unit: 'piece' | 'kg' | 'ton'
  shelf_life_days: number
}

export interface BrokerCompany {
  id: number
  name: string
  monthly_fee: string | number
  contact_info?: string
}

export interface Broker {
  id: number
  company: number
  commission_rate: string | number
  active: boolean
  user?: number | null
}

export interface Batch {
  id: number
  number: string
  broker: number
  contract_date: string
  shipment_date?: string | null
  prepayment: boolean
  notes?: string
}

export interface BatchItem {
  id: number
  batch: number
  product: number
  production_date: string
  quantity: string | number
  unit_price: string | number
  is_expired?: boolean
  total_price?: string
}

