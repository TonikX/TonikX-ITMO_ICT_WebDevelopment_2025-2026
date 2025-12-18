// функция для извлечения текста сообщения об ошибке из различных форматов
export const getErrorMessage = (error: unknown): string => {
  // если ошибка - это строка, возвращаем её напрямую
  if (typeof error === 'string') {
    return error
  }

  // если ошибка это объект с полем response (например, AxiosError)
  if (error && typeof error === 'object' && 'response' in error) {
    // получаем объект response из ошибки
    const response = (error as any).response
    if (response?.data) {
      if (typeof response.data === 'string') {
        return response.data
      }
      // если есть поле detail (DRF)
      if (response.data.detail) {
        return response.data.detail
      }

      if (response.data.error) {
        return response.data.error
      }

      if (response.data.message) {
        return response.data.message
      }
      // обработка ошибок валидации (DRF)
      // получаем первый ключ из объекта данных
      const firstKey = Object.keys(response.data)[0]
      // если первый ключ существует и его значение - массив
      if (firstKey && Array.isArray(response.data[firstKey])) {
        // возвращаем формат: "поле: первое сообщение об ошибке"
        return `${firstKey}: ${response.data[firstKey][0]}`
      }
    }
    // если нет данных, но есть statusText (например, "Not Found", "Unauthorized")
    if (response?.statusText) {
      return response.statusText
    }
  }

  // если ошибка - это объект Error с полем message
  if (error && typeof error === 'object' && 'message' in error) {
    // возвращаем стандартное сообщение об ошибке
    return (error as Error).message
  }

  // если не удалось извлечь сообщение
  return 'Произошла неизвестная ошибка'
}


