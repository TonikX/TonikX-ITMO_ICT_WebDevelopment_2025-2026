export const REQUEST_STATUSES = {
  NEW: 'new',
  IN_PROGRESS: 'in_progress',
  DONE: 'done',
  CANCELED: 'canceled',
}

export const REQUEST_STATUS_LABELS = {
  [REQUEST_STATUSES.NEW]: 'Новая',
  [REQUEST_STATUSES.IN_PROGRESS]: 'В работе',
  [REQUEST_STATUSES.DONE]: 'Выполнено',
  [REQUEST_STATUSES.CANCELED]: 'Отменена',
}

export const REQUEST_STATUS_COLORS = {
  [REQUEST_STATUSES.NEW]: 'info',
  [REQUEST_STATUSES.IN_PROGRESS]: 'warning',
  [REQUEST_STATUSES.DONE]: 'success',
  [REQUEST_STATUSES.CANCELED]: 'error',
}

export const REQUEST_PRIORITIES = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
  URGENT: 'urgent',
}

export const REQUEST_PRIORITY_LABELS = {
  [REQUEST_PRIORITIES.LOW]: 'Низкий',
  [REQUEST_PRIORITIES.MEDIUM]: 'Средний',
  [REQUEST_PRIORITIES.HIGH]: 'Высокий',
  [REQUEST_PRIORITIES.URGENT]: 'Срочный',
}

export const REQUEST_PRIORITY_COLORS = {
  [REQUEST_PRIORITIES.LOW]: 'grey',
  [REQUEST_PRIORITIES.MEDIUM]: 'primary',
  [REQUEST_PRIORITIES.HIGH]: 'orange',
  [REQUEST_PRIORITIES.URGENT]: 'error',
}

export const METER_TYPES = {
  HOT_WATER: 'hot_water',
  COLD_WATER: 'cold_water',
  ELECTRICITY: 'electricity',
  GAS: 'gas',
}

export const METER_TYPE_LABELS = {
  [METER_TYPES.HOT_WATER]: 'Горячая вода',
  [METER_TYPES.COLD_WATER]: 'Холодная вода',
  [METER_TYPES.ELECTRICITY]: 'Электричество',
  [METER_TYPES.GAS]: 'Газ',
}

export const METER_TYPE_COLORS = {
  [METER_TYPES.HOT_WATER]: 'error',
  [METER_TYPES.COLD_WATER]: 'info',
  [METER_TYPES.ELECTRICITY]: 'warning',
  [METER_TYPES.GAS]: 'success',
}

export function getRequestStatusLabel(status) {
  return REQUEST_STATUS_LABELS[status] || status
}

export function getRequestStatusColor(status) {
  return REQUEST_STATUS_COLORS[status] || 'grey'
}

export function getRequestPriorityLabel(priority) {
  return REQUEST_PRIORITY_LABELS[priority] || priority
}

export function getRequestPriorityColor(priority) {
  return REQUEST_PRIORITY_COLORS[priority] || 'grey'
}

export function getMeterTypeLabel(type) {
  return METER_TYPE_LABELS[type] || type
}

export function getMeterTypeColor(type) {
  return METER_TYPE_COLORS[type] || 'grey'
}

export function getRequestStatusOptions() {
  return Object.keys(REQUEST_STATUSES).map(key => ({
    value: REQUEST_STATUSES[key],
    title: REQUEST_STATUS_LABELS[REQUEST_STATUSES[key]],
  }))
}

export function getRequestPriorityOptions() {
  return Object.keys(REQUEST_PRIORITIES).map(key => ({
    value: REQUEST_PRIORITIES[key],
    title: REQUEST_PRIORITY_LABELS[REQUEST_PRIORITIES[key]],
  }))
}

export function getMeterTypeOptions() {
  return Object.keys(METER_TYPES).map(key => ({
    value: METER_TYPES[key],
    title: METER_TYPE_LABELS[METER_TYPES[key]],
  }))
}

