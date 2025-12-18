/**
 * Custom hook для управления уведомлениями
 * Упрощает работу с notification state и предоставляет удобные методы
 */

import { useState, useCallback } from 'react'
import { NotificationState, DEFAULT_NOTIFICATION } from '../types/common'
import { getErrorMessage } from '../utils/notifications'

// интерфейс возвращаемого значения хука useNotification
interface UseNotificationReturn {
  notification: NotificationState
  showSuccess: (message: string) => void
  showError: (error: unknown) => void
  showInfo: (message: string) => void
  showWarning: (message: string) => void
  hideNotification: () => void
}

// хук для управления состоянием уведомлений в компонентах
export const useNotification = (): UseNotificationReturn => {
  const [notification, setNotification] = useState<NotificationState>(DEFAULT_NOTIFICATION)

  const showSuccess = useCallback((message: string) => {
    setNotification({
      open: true,
      message,
      severity: 'success',
    })
  }, []) // пустой массив зависимостей - функция создается один раз

  const showError = useCallback((error: unknown) => {
    setNotification({
      open: true,
      message: getErrorMessage(error),
      severity: 'error',
    })
  }, [])


  const showInfo = useCallback((message: string) => {
    setNotification({
      open: true,
      message,
      severity: 'info',
    })
  }, [])


  const showWarning = useCallback((message: string) => {
    setNotification({
      open: true,
      message,
      severity: 'warning',
    })
  }, [])

  // функция для скрытия уведомления
  const hideNotification = useCallback(() => {
    // обновляем состояние, сохраняя все поля, но устанавливая open в false
    setNotification((prev) => ({ ...prev, open: false }))
  }, [])


  return {
    notification,
    showSuccess,
    showError,
    showInfo,
    showWarning,
    hideNotification,
  }
}

