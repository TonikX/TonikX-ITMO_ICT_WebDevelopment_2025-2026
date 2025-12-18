import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm, Controller } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import * as yup from 'yup'
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
} from '@mui/material'
import { staffAPI } from '../api/staff.api'
import { Notification } from '../components/Notification'
import { getErrorMessage } from '../utils/notifications'
import { StaffRegister } from '../types'

const schema = yup.object({
  login: yup.string().required('Логин обязателен'),
  email: yup.string().email('Неверный формат email').required('Email обязателен'),
  password: yup.string().required('Пароль обязателен').min(8, 'Пароль должен содержать минимум 8 символов'),
  registration_key: yup.string().required('Секретный ключ обязателен'),
}).required()

export const RegisterStaffPage: React.FC = () => {
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  const navigate = useNavigate()

  const { control, handleSubmit, formState: { errors } } = useForm<StaffRegister>({
    resolver: yupResolver(schema),
    defaultValues: {
      login: '',
      email: '',
      password: '',
      registration_key: '',
    },
  })

  const onSubmit = async (data: StaffRegister) => {
    try {
      await staffAPI.registerStaff(data)
      setNotification({
        open: true,
        message: 'Новый сотрудник успешно зарегистрирован!',
        severity: 'success',
      })
      setTimeout(() => navigate('/profile'), 2000)
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    }
  }

  return (
    <Container component="main" maxWidth="xs">
      <Paper elevation={3} sx={{ padding: 4, mt: 3 }}>
        <Typography component="h1" variant="h5" align="center" gutterBottom>
          Регистрация нового сотрудника
        </Typography>
        <Typography variant="body2" color="text.secondary" align="center" paragraph>
          Для регистрации нового сотрудника требуется секретный ключ
        </Typography>
          <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate sx={{ mt: 1 }}>
            <Controller
              name="login"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  margin="normal"
                  fullWidth
                  label="Логин"
                  autoFocus
                  error={!!errors.login}
                  helperText={errors.login?.message}
                />
              )}
            />
            <Controller
              name="email"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  margin="normal"
                  fullWidth
                  label="Email"
                  type="email"
                  error={!!errors.email}
                  helperText={errors.email?.message}
                />
              )}
            />
            <Controller
              name="password"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  margin="normal"
                  fullWidth
                  label="Пароль"
                  type="password"
                  error={!!errors.password}
                  helperText={errors.password?.message}
                />
              )}
            />
            <Controller
              name="registration_key"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  margin="normal"
                  fullWidth
                  label="Секретный ключ регистрации"
                  type="password"
                  error={!!errors.registration_key}
                  helperText={errors.registration_key?.message}
                />
              )}
            />
            <Box sx={{ display: 'flex', gap: 2, mt: 3 }}>
              <Button onClick={() => navigate('/profile')}>
                Отмена
              </Button>
              <Button type="submit" variant="contained" fullWidth>
                Зарегистрировать сотрудника
              </Button>
            </Box>
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

