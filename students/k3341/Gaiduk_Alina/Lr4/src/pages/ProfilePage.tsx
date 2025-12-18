import React, { useEffect, useState } from 'react'
import {
  Container,
  Paper,
  Typography,
  Box,
  TextField,
  Button,
  CircularProgress,
} from '@mui/material'
import { useForm, Controller } from 'react-hook-form'
import { staffAPI } from '../api/staff.api'
import { Staff } from '../types'
import { Notification } from '../components/Notification'
import { getErrorMessage } from '../utils/notifications'

export const ProfilePage: React.FC = () => {
  const [loading, setLoading] = useState(true)
  const [staff, setStaff] = useState<Staff | null>(null)
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  const { control, handleSubmit, reset } = useForm<Partial<Staff>>()

  useEffect(() => {
    loadProfile()
  }, [])

  const loadProfile = async () => {
    try {
      setLoading(true)
      const staffList = await staffAPI.getAll()
      // Берем первого сотрудника (можно улучшить логику)
      if (staffList.length > 0) {
        setStaff(staffList[0])
        reset({
          login: staffList[0].login,
          email: staffList[0].email,
        })
      }
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    } finally {
      setLoading(false)
    }
  }

  const onSubmit = async (data: Partial<Staff>) => {
    if (!staff) return

    try {
      const updated = await staffAPI.update(staff.staff_id, data)
      setStaff(updated)
      setNotification({
        open: true,
        message: 'Профиль успешно обновлен',
        severity: 'success',
      })
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Container maxWidth="md">
      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Профиль сотрудника
        </Typography>
        <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ mt: 2 }}>
          <Controller
            name="login"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                fullWidth
                label="Логин"
                margin="normal"
              />
            )}
          />
          <Controller
            name="email"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                fullWidth
                label="Email"
                type="email"
                margin="normal"
              />
            )}
          />
          <Button type="submit" variant="contained" sx={{ mt: 2 }}>
            Сохранить изменения
          </Button>
        </Box>
      </Paper>
      <Notification
        open={notification.open}
        message={notification.message}
        severity={notification.severity}
        onClose={() => setNotification({ ...notification, open: false })}
      />
    </Container>
  )
}


