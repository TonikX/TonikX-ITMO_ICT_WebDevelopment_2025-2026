/**
 * общие типы для всего приложения
 */

// интерфейс для состояния уведомления
export interface NotificationState {
  open: boolean // флаг видимости уведомления
  message: string
  severity: 'success' | 'error' | 'info' | 'warning' // тип уведомления (успех, ошибка, информация, предупреждение)
}

// интерфейс для состояния диалога подтверждения удаления
export interface DeleteConfirmState {
  open: boolean
  id: number | null // ID элемента для удаления (null, если диалог закрыт)
}

// значение по умолчанию для состояния уведомления
export const DEFAULT_NOTIFICATION: NotificationState = {
  open: false,
  message: '',
  severity: 'info', // тип: информационное
}

// значение по умолчанию для состояния диалога подтверждения удаления
export const DEFAULT_DELETE_CONFIRM: DeleteConfirmState = {
  open: false,
  id: null,
}

