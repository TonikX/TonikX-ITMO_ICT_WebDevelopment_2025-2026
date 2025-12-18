import React, { useState } from 'react'
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
} from '@mui/material'
import { staffAPI } from '../api/staff.api'
import { Notification } from '../components/Notification'
import { ConfirmDialog } from '../components/ConfirmDialog'
import { getErrorMessage } from '../utils/notifications'

export const DeactivateReadersPage: React.FC = () => {
  const [confirmOpen, setConfirmOpen] = useState(false)
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  const handleDeactivate = async () => {
    try {
      const result = await staffAPI.deactivateOldReaders()
      setNotification({
        open: true,
        message: result.message,
        severity: 'success',
      })
      setConfirmOpen(false)
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    }
  }

  return (
    <Container maxWidth="sm">
      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Деактивация старых читателей
        </Typography>
        <Typography variant="body1" paragraph>
          Эта операция деактивирует всех читателей, которые зарегистрировались более года назад 
          и не проходили перерегистрацию.
        </Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          Деактивированные читатели не смогут брать новые книги, но информация о них сохранится в системе.
        </Typography>
        <Box sx={{ mt: 3 }}>
          <Button
            variant="contained"
            color="warning"
            onClick={() => setConfirmOpen(true)}
            fullWidth
          >
            Деактивировать старых читателей
          </Button>
        </Box>
      </Paper>

      <ConfirmDialog
        open={confirmOpen}
        title="Подтверждение деактивации"
        message="Вы уверены, что хотите деактивировать всех читателей, зарегистрированных более года назад без перерегистрации?"
        onConfirm={handleDeactivate}
        onCancel={() => setConfirmOpen(false)}
      />

      <Notification
        open={notification.open}
        message={notification.message}
        severity={notification.severity}
        onClose={() => setNotification({ ...notification, open: false })}
      />
    </Container>
  )
}


