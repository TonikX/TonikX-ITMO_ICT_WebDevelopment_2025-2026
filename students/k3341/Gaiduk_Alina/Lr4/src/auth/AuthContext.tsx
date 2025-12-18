import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { authAPI } from '../api/auth.api'
import { LoginCredentials, TokenResponse } from '../types'

// интерфейс для типа контекста аутентификации
interface AuthContextType {
  isAuthenticated: boolean // флаг
  login: (credentials: LoginCredentials) => Promise<void> // функция для входа в систему
  logout: () => void // функция для выхода из системы
  loading: boolean // флаг загрузки (проверка токенов при старте)
}

// создаем контекст для аутентификации с типом или undefined
const AuthContext = createContext<AuthContextType | undefined>(undefined)

// провайдер контекста аутентификации, который оборачивает приложение
export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  // состояние: аутентифицирован ли пользователь (по умолчанию false)
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false)
  // состояние: идет ли проверка токенов (по умолчанию true, пока не проверим)
  const [loading, setLoading] = useState<boolean>(true)

  // эффект, выполняющийся один раз при монтировании компонента
  useEffect(() => {
    // проверяем наличие токенов при загрузке
    // получаем access токен из localStorage
    const accessToken = localStorage.getItem('access_token')
    // Получаем refresh токен из localStorage
    const refreshToken = localStorage.getItem('refresh_token')

    // если оба токена существуют, считаем пользователя аутентифицированным
    if (accessToken && refreshToken) {
      // устанавливаем флаг аутентификации в true
      setIsAuthenticated(true)
    }
    // завершаем процесс загрузки (проверка токенов завершена)
    setLoading(false)
  }, []) // пустой массив зависимостей - выполняется только один раз

  // функция для входа в систему
  const login = async (credentials: LoginCredentials): Promise<void> => {
    try {
      // отправляем запрос на сервер для получения токенов
      const tokens: TokenResponse = await authAPI.login(credentials)
      // сохраняем токены в localStorage
      localStorage.setItem('access_token', tokens.access)
      localStorage.setItem('refresh_token', tokens.refresh)
      // устанавливаем флаг в true
      setIsAuthenticated(true)
    } catch (error) {
      throw error
    }
  }

  // функция для выхода из системы
  const logout = () => {
    // удаляем токены из localStorage
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    // устанавливаем флаг в false
    setIsAuthenticated(false)
  }

  // возвращаем провайдер контекста с передачей всех значений дочерним компонентам
  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

// хук для использования контекста аутентификации в компонентах
export const useAuth = (): AuthContextType => {
  // получаем значение контекста
  const context = useContext(AuthContext)
  // проверяем, что хук используется внутри AuthProvider
  if (context === undefined) {
    // если контекст undefined, значит хук используется вне провайдера - выбрасываем ошибку
    throw new Error('useAuth must be used within an AuthProvider')
  }
  // возвращаем значение контекста
  return context
}


