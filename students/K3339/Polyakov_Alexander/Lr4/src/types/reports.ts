export interface ProductQuantityRow {
  product_id: number
  product__code: string
  product__name: string
  total_quantity: string
}

export interface TopManufacturerRow {
  product__manufacturer_id: number
  product__manufacturer__name: string
  revenue: string
}

export interface BrokerSalaryRow {
  broker_id: number
  company: string
  turnover: string
  commission: string
  monthly_fee: string
  salary: string
}

export interface LatestTradeRow {
  product_id: number
  product_code: string
  product_name: string
  manufacturer: string
  last_batch_number: string
  last_batch_date: string
  last_batch_quantity: string
  offered_by_company: string
  total_quantity: string
}

