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
  InputAdornment,
  IconButton,
  Stack,
  Avatar,
  Fade,
} from '@mui/material'
import {
  Visibility,
  VisibilityOff,
  Login as LoginIcon,
  MenuBook,
} from '@mui/icons-material'
import { useAuth } from '../auth/AuthContext'
import { Notification } from '../components/Notification'
import { getErrorMessage } from '../utils/notifications'
import { LoginCredentials } from '../types'

// схема валидации полей формы входа с помощью библиотеки yup
const schema = yup.object({
  login: yup.string().required('Логин обязателен'),
  password: yup.string().required('Пароль обязателен').min(8, 'Пароль должен содержать минимум 8 символов'),
}).required()

// компонент страницы входа в систему
export const LoginPage: React.FC = () => {
  const [showPassword, setShowPassword] = useState(false) // хук usestate: управляет отображением/скрытием пароля
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  const { login } = useAuth() // кастомный хук авторизации: получаем функцию логина
  const navigate = useNavigate() // хук react-router: позволяет программно переходить между страницами

  // хук useform из react-hook-form: управляет состоянием и валидацией формы входа
  const { control, handleSubmit, formState: { errors, isSubmitting } } = useForm<LoginCredentials>({
    resolver: yupResolver(schema),
    defaultValues: {
      login: '',
      password: '',
    },
  })

  // основная функция-обработчик отправки формы входа
  const onSubmit = async (data: LoginCredentials) => {
    try {
      await login(data)
      setNotification({
        open: true,
        message: 'Успешный вход',
        severity: 'success',
      })
      setTimeout(() => navigate('/books'), 500)
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    }
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        position: 'relative',
        overflow: 'hidden',
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%)',
        },
        '&::after': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%)',
        },
      }}
    >
      <Container component="main" maxWidth="xs" sx={{ position: 'relative', zIndex: 1 }}>
        <Fade in timeout={600}>
          <Paper
            elevation={24}
            sx={{
              p: 4,
              borderRadius: 4,
              background: 'rgba(255, 255, 255, 0.95)',
              backdropFilter: 'blur(20px)',
              boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
            }}
          >
            <Stack spacing={3} alignItems="center">
              <Avatar
                sx={{
                  width: 80,
                  height: 80,
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  boxShadow: '0 8px 16px rgba(102, 126, 234, 0.4)',
                }}
              >
                <MenuBook sx={{ fontSize: 40 }} />
              </Avatar>

              <Box textAlign="center">
                <Typography
                  component="h1"
                  variant="h4"
                  fontWeight={700}
                  sx={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    backgroundClip: 'text',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    mb: 1,
                  }}
                >
                  Добро пожаловать
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Войдите в систему управления библиотекой
                </Typography>
              </Box>

              <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ width: '100%' }}>
                <Stack spacing={2.5}>
                  <Controller
                    name="login"
                    control={control}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        fullWidth
                        label="Логин"
                        autoComplete="username"
                        autoFocus
                        error={!!errors.login}
                        helperText={errors.login?.message}
                        sx={{
                          '& .MuiOutlinedInput-root': {
                            '&:hover fieldset': {
                              borderColor: '#667eea',
                            },
                          },
                        }}
                      />
                    )}
                  />

                  <Controller
                    name="password"
                    control={control}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        fullWidth
                        label="Пароль"
                        type={showPassword ? 'text' : 'password'}
                        autoComplete="current-password"
                        error={!!errors.password}
                        helperText={errors.password?.message}
                        InputProps={{
                          endAdornment: (
                            <InputAdornment position="end">
                              <IconButton
                                aria-label="toggle password visibility"
                                onClick={() => setShowPassword(!showPassword)}
                                edge="end"
                              >
                                {showPassword ? <VisibilityOff /> : <Visibility />}
                              </IconButton>
                            </InputAdornment>
                          ),
                        }}
                        sx={{
                          '& .MuiOutlinedInput-root': {
                            '&:hover fieldset': {
                              borderColor: '#667eea',
                            },
                          },
                        }}
                      />
                    )}
                  />

                  <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    size="large"
                    disabled={isSubmitting}
                    startIcon={<LoginIcon />}
                    sx={{
                      mt: 2,
                      py: 1.5,
                      fontSize: '1rem',
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      '&:hover': {
                        background: 'linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%)',
                        boxShadow: '0 8px 16px rgba(102, 126, 234, 0.4)',
                      },
                      '&.Mui-disabled': {
                        background: 'rgba(0, 0, 0, 0.12)',
                      },
                    }}
                  >
                    {isSubmitting ? 'Вход...' : 'Войти'}
                  </Button>
                </Stack>
              </Box>

              <Box textAlign="center" sx={{ pt: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Нет аккаунта? Обратитесь к существующему сотруднику для регистрации.
                </Typography>
              </Box>
            </Stack>
          </Paper>
        </Fade>
      </Container>

      <Notification
        open={notification.open}
        message={notification.message}
        severity={notification.severity}
        onClose={() => setNotification({ ...notification, open: false })}
      />
    </Box>
  )
}
