import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios'

// базовый URL API из переменных окружения
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'


// создаем настроенный экземпляр axios клиента
export const httpClient = axios.create({
  // добавляем /api к базовому URL для запросов
  baseURL: `${baseURL}/api`,
  // заголовки по умолчанию для всех запросов
  headers: {
    'Content-Type': 'application/json', // отправляем JSON данные
  },
})

// добавляет токен к каждому запросу
// перехватчик запросов: выполняется перед отправкой каждого HTTP запроса
httpClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // получаем access токен из localStorage
    const token = localStorage.getItem('access_token')
    // если токен существует и заголовки доступны, добавляем его к запросу
    if (token && config.headers) {
      // устанавливаем заголовок Authorization с Bearer токеном
      config.headers.Authorization = `Bearer ${token}`
    }
    // возвращаем конфигурацию запроса
    return config
  },
  // обработчик ошибок при настройке запроса
  (error) => {
    // пробрасываем ошибку дальше
    return Promise.reject(error)
  }
)


// флаг, указывающий, выполняется ли сейчас обновление токена
let isRefreshing = false
// очередь запросов, которые были отправлены во время обновления токена
let failedQueue: Array<{
  resolve: (value?: unknown) => void // функция для успешного разрешения промиса
  reject: (reason?: unknown) => void // функция для отклонения промиса
}> = []

// функция для обработки очереди запросов после обновления токена
const processQueue = (error: Error | null, token: string | null = null) => {
  // проходим по всем ожидающим запросам в очереди
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })

  // очищаем очередь после обработки
  failedQueue = []
}

// обрабатывает ошибки и обновляет токен
// перехватчик ответов: выполняется после получения каждого HTTP ответа
httpClient.interceptors.response.use(
  (response) => {
    return response
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean }

    // Обрабатываем ошибку 401 (Unauthorized) - токен истек или недействителен
    // Проверяем, что это ошибка авторизации и запрос еще не был повторен
    if (error.response?.status === 401 && !originalRequest._retry) {
      // Если уже идет процесс обновления токена
      if (isRefreshing) {
        // Возвращаем новый промис, который добавим в очередь ожидания
        return new Promise((resolve, reject) => {
          // Добавляем промис в очередь для выполнения после обновления токена
          failedQueue.push({ resolve, reject })
        })
          .then((token) => {
            // Когда токен обновлен, добавляем его к оригинальному запросу
            if (originalRequest.headers) {
              originalRequest.headers.Authorization = `Bearer ${token}`
            }
            // Повторяем оригинальный запрос с новым токеном
            return httpClient(originalRequest)
          })
          .catch((err) => {
            // Если обновление токена провалилось, отклоняем промис
            return Promise.reject(err)
          })
      }

      // Помечаем, что этот запрос уже пытались повторить
      originalRequest._retry = true
      // Устанавливаем флаг, что идет обновление токена
      isRefreshing = true

      // Получаем refresh токен из localStorage
      const refreshToken = localStorage.getItem('refresh_token')

      if (!refreshToken) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(error)
      }

      try {
        const response = await axios.post(`${baseURL}/api/token/refresh/`, {
          refresh: refreshToken,
        })

        const { access } = response.data
        localStorage.setItem('access_token', access)

        // Добавляем новый токен к оригинальному запросу
        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${access}`
        }

        // Обрабатываем очередь ожидающих запросов с новым токеном
        processQueue(null, access)
        // Сбрасываем флаг обновления токена
        isRefreshing = false

        // Повторяем оригинальный запрос с новым токеном
        return httpClient(originalRequest)
      } catch (refreshError) {
        processQueue(refreshError as Error, null)
        // удаляем все токены из localStorage
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        // перенаправляем пользователя на страницу входа
        window.location.href = '/login'
        // сбрасываем флаг обновления токена
        isRefreshing = false
        // отклоняем промис с ошибкой обновления токена
        return Promise.reject(refreshError)
      }
    }

    // для всех других ошибок просто пробрасываем их дальше
    return Promise.reject(error)
  }
)

// вспомогательная функция для загрузки всех страниц пагинированных данных
// используется для получения всех данных из API, которые разбиты на страницы
export const fetchAllPages = async <T>(endpoint: string): Promise<T[]> => {
  try {
    // массив для накопления всех данных со всех страниц
    const allData: T[] = []
    // URL следующей страницы для загрузки (начинаем с переданного эндпоинта)
    let nextUrl: string | null = endpoint
    // счетчик страниц для защиты от бесконечного цикла
    let pageCount = 0

      // увеличиваем счетчик страниц
    while (nextUrl && pageCount < 100) {
      pageCount++
      // отправляем GET запрос для получения текущей страницы данных
      const response: { data: any } = await httpClient.get<any>(nextUrl)

      // если ответ - это массив напрямую (пагинация отключена)
      if (Array.isArray(response.data)) {
        return response.data
      }

      // если ответ - это объект с results (пагинация включена)
      if (response.data?.results && Array.isArray(response.data.results)) {
        // добавляем все элементы текущей страницы в общий массив
        allData.push(...response.data.results)
        // если есть следующая страница
        if (response.data.next) {
          // получаем URL следующей страницы
          const next: string = response.data.next
          
          // если URL начинается с http
          if (next.startsWith('http')) {
            // Полный URL - извлекаем путь и query параметры
            try {
              // парсим URL
              const url = new URL(next)
              // извлекаем путь и query параметры
              let path = url.pathname + url.search
              // если путь начинается с /api/
              if (path.startsWith('/api/')) {
                // убираем /api/ из пути
                path = path.substring(4)
              }
              // устанавливаем URL следующей страницы
              nextUrl = path
            } catch (e) {
              // если не удалось парсить URL, используем исходный URL
              let path = next
              // если путь включает /api/
              if (path.includes('/api/')) {
                // убираем /api/ из пути
                path = '/' + path.split('/api/')[1]
              }
              // убеждаемся что путь начинается с /
              nextUrl = path.startsWith('/') ? path : '/' + path
            }
          } else {
            // убеждаемся что путь начинается с /
            nextUrl = next.startsWith('/') ? next : '/' + next
          }
        } else {
          // если нет следующей страницы, устанавливаем URL на null
          nextUrl = null
        }
      } else if (response.data?.results && response.data.results.length === 0) {
        // если нет результатов, устанавливаем URL на null
        nextUrl = null
      } else {
        // если это первая страница и нет результатов, возвращаем пустой массив
        if (pageCount === 1) {
          return []
        }
        break
      }
    }

    return allData
  } catch (error) {
    throw error
  }
}

export default httpClient
