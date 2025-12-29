export const formatDate = (dateString, options = {}) => {
    if (!dateString) return ''

    const date = new Date(dateString)
    const defaultOptions = {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
    }

    return date.toLocaleDateString('ru-RU', { ...defaultOptions, ...options })
}

export const checkDiscountOverlap = (newDiscount, existingDiscounts, serviceId = null) => {
    if (!newDiscount.start_date || !newDiscount.end_date) {
        return { hasOverlap: false, message: '' }
    }

    const newStart = new Date(newDiscount.start_date)
    const newEnd = new Date(newDiscount.end_date)

    // Проверяем, что дата начала раньше даты окончания
    if (newStart >= newEnd) {
        return {
            hasOverlap: true,
            message: 'Дата начала должна быть раньше даты окончания'
        }
    }

    // Проверяем, что дата окончания в будущем
    if (newEnd <= new Date()) {
        return {
            hasOverlap: true,
            message: 'Дата окончания должна быть в будущем'
        }
    }

    for (const existing of existingDiscounts) {
        // Если указан serviceId, проверяем только скидки для этой услуги
        if (serviceId && existing.service !== serviceId) continue

        const existingStart = new Date(existing.start_date)
        const existingEnd = new Date(existing.end_date)

        // Проверяем пересечение интервалов
        if (newStart < existingEnd && newEnd > existingStart) {
            return {
                hasOverlap: true,
                message: `Пересечение с существующей скидкой (${formatDate(existing.start_date)} - ${formatDate(existing.end_date)})`
            }
        }
    }

    return { hasOverlap: false, message: '' }
}

export const formatDateTime = (dateString) => {
    if (!dateString) return ''
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}