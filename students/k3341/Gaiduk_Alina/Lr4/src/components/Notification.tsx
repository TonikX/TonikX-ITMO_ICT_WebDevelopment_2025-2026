import React from 'react'
import { Snackbar, Alert, AlertColor } from '@mui/material'

// интерфейс для пропсов компонента Notification
interface NotificationProps {
  open: boolean
  message: string
  severity?: AlertColor // тип уведомления (success, error, warning, info)
  onClose: () => void // функция для закрытия уведомления
}

// компонент для отображения уведомлений
export const Notification: React.FC<NotificationProps> = ({
  open,
  message,
  severity = 'info',
  onClose,
}) => {
  return (
    // компонент MUI для показа уведомлений внизу экрана
    <Snackbar
      open={open}
      autoHideDuration={6000} // автоматически скрывается через 6 секунд
      onClose={onClose}
      anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
    >
      {/* компонент для отображения сообщения с иконкой и цветом */}
      <Alert onClose={onClose} severity={severity} sx={{ width: '100%' }}>
        {message}
      </Alert>
    </Snackbar>
  )
}


