/**
 * Утилиты для форматирования дат
 */

/**
 * Форматирует дату в формат DD.MM.YYYY
 */
export function formatDate(dateString) {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return dateString
  
  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const year = date.getFullYear()
  
  return `${day}.${month}.${year}`
}

/**
 * Форматирует дату и время в формат DD.MM.YYYY HH:MM
 */
export function formatDateTime(dateString) {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return dateString
  
  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const year = date.getFullYear()
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  
  return `${day}.${month}.${year} ${hours}:${minutes}`
}

/**
 * Форматирует дату для input type="date" (YYYY-MM-DD)
 */
export function formatDateForInput(dateString) {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return ''
  
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  
  return `${year}-${month}-${day}`
}

/**
 * Получает относительное время (например, "2 часа назад")
 */
export function getRelativeTime(dateString) {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return dateString
  
  const now = new Date()
  const diffMs = now - date
  const diffSec = Math.floor(diffMs / 1000)
  const diffMin = Math.floor(diffSec / 60)
  const diffHour = Math.floor(diffMin / 60)
  const diffDay = Math.floor(diffHour / 24)
  
  if (diffSec < 60) {
    return 'только что'
  } else if (diffMin < 60) {
    return `${diffMin} ${pluralize(diffMin, 'минуту', 'минуты', 'минут')} назад`
  } else if (diffHour < 24) {
    return `${diffHour} ${pluralize(diffHour, 'час', 'часа', 'часов')} назад`
  } else if (diffDay < 7) {
    return `${diffDay} ${pluralize(diffDay, 'день', 'дня', 'дней')} назад`
  } else {
    return formatDate(dateString)
  }
}

/**
 * Склонение слов
 */
function pluralize(count, one, few, many) {
  const mod10 = count % 10
  const mod100 = count % 100
  
  if (mod10 === 1 && mod100 !== 11) {
    return one
  } else if (mod10 >= 2 && mod10 <= 4 && (mod100 < 10 || mod100 >= 20)) {
    return few
  } else {
    return many
  }
}

