import api from './http'
import type {
  Batch,
  BatchItem,
  Broker,
  BrokerCompany,
  Manufacturer,
  Product,
} from '../types/models'
import type {
  BrokerSalaryRow,
  LatestTradeRow,
  ProductQuantityRow,
  TopManufacturerRow,
} from '../types/reports'

// Manufacturers
export const fetchManufacturers = async (): Promise<Manufacturer[]> => {
  const { data } = await api.get<Manufacturer[]>('api/manufacturers/')
  return data
}
export const createManufacturer = async (payload: Partial<Manufacturer>) => {
  const { data } = await api.post<Manufacturer>('api/manufacturers/', payload)
  return data
}
export const updateManufacturer = async (id: number, payload: Partial<Manufacturer>) => {
  const { data } = await api.put<Manufacturer>(`api/manufacturers/${id}/`, payload)
  return data
}
export const deleteManufacturer = async (id: number) => {
  await api.delete(`api/manufacturers/${id}/`)
}

// Products
export const fetchProducts = async (): Promise<Product[]> => {
  const { data } = await api.get<Product[]>('api/products/')
  return data
}
export const createProduct = async (payload: Partial<Product>) => {
  const { data } = await api.post<Product>('api/products/', payload)
  return data
}
export const updateProduct = async (id: number, payload: Partial<Product>) => {
  const { data } = await api.put<Product>(`api/products/${id}/`, payload)
  return data
}
export const deleteProduct = async (id: number) => {
  await api.delete(`api/products/${id}/`)
}

// Broker companies
export const fetchBrokerCompanies = async (): Promise<BrokerCompany[]> => {
  const { data } = await api.get<BrokerCompany[]>('api/broker-companies/')
  return data
}
export const createBrokerCompany = async (payload: Partial<BrokerCompany>) => {
  const { data } = await api.post<BrokerCompany>('api/broker-companies/', payload)
  return data
}
export const updateBrokerCompany = async (id: number, payload: Partial<BrokerCompany>) => {
  const { data } = await api.put<BrokerCompany>(`api/broker-companies/${id}/`, payload)
  return data
}
export const deleteBrokerCompany = async (id: number) => {
  await api.delete(`api/broker-companies/${id}/`)
}

// Brokers
export const fetchBrokers = async (): Promise<Broker[]> => {
  const { data } = await api.get<Broker[]>('api/brokers/')
  return data
}
export const createBroker = async (payload: Partial<Broker>) => {
  const { data } = await api.post<Broker>('api/brokers/', payload)
  return data
}
export const updateBroker = async (id: number, payload: Partial<Broker>) => {
  const { data } = await api.put<Broker>(`api/brokers/${id}/`, payload)
  return data
}
export const deleteBroker = async (id: number) => {
  await api.delete(`api/brokers/${id}/`)
}

// Batches
export const fetchBatches = async (): Promise<Batch[]> => {
  const { data } = await api.get<Batch[]>('api/batches/')
  return data
}
export const createBatch = async (payload: Partial<Batch>) => {
  const { data } = await api.post<Batch>('api/batches/', payload)
  return data
}
export const updateBatch = async (id: number, payload: Partial<Batch>) => {
  const { data } = await api.put<Batch>(`api/batches/${id}/`, payload)
  return data
}
export const deleteBatch = async (id: number) => {
  await api.delete(`api/batches/${id}/`)
}

// Batch items
export const fetchBatchItems = async (): Promise<BatchItem[]> => {
  const { data } = await api.get<BatchItem[]>('api/batch-items/')
  return data
}
export const createBatchItem = async (payload: Partial<BatchItem>) => {
  const { data } = await api.post<BatchItem>('api/batch-items/', payload)
  return data
}
export const updateBatchItem = async (id: number, payload: Partial<BatchItem>) => {
  const { data } = await api.put<BatchItem>(`api/batch-items/${id}/`, payload)
  return data
}
export const deleteBatchItem = async (id: number) => {
  await api.delete(`api/batch-items/${id}/`)
}

// Reports
export const fetchProductQuantities = async (date?: string) => {
  const { data } = await api.get<ProductQuantityRow[]>('api/reports/product-quantities/', {
    params: { date },
  })
  return data
}

export const fetchTopManufacturer = async (params: { start?: string; end?: string }) => {
  const { data } = await api.get<TopManufacturerRow | Record<string, never>>(
    'api/reports/top-manufacturer/',
    { params },
  )
  return data
}

export const fetchUnsoldProducts = async (params: { company_id?: string; company_name?: string }) => {
  const { data } = await api.get('api/reports/unsold-products/', { params })
  return data as Array<{ id: number; code: string; name: string }>
}

export const fetchExpiredItems = async () => {
  const { data } = await api.get('api/reports/expired-items/')
  return data as Array<{
    batch_number: string
    product_code: string
    product_name: string
    broker_id: number
    broker_company: string
  }>
}

export const fetchBrokerSalaries = async (params: {
  company_id?: string
  company_name?: string
  start?: string
  end?: string
}) => {
  const { data } = await api.get<BrokerSalaryRow[]>('api/reports/broker-salaries/', { params })
  return data
}

export const fetchLatestTrades = async () => {
  const { data } = await api.get('api/reports/latest-trades/')
  return data as { total_products: number; total_quantity: string; items: LatestTradeRow[] }
}

