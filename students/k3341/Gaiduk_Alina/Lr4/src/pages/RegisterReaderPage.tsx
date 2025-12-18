import React, { useEffect, useState } from 'react'
import {
  Container,
  Paper,
  Typography,
  Box,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Checkbox,
} from '@mui/material'
import { useForm, Controller } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'
import { staffAPI } from '../api/staff.api'
import { hallsAPI } from '../api/halls.api'
import { Hall, ReaderCreate } from '../types'
import { Notification } from '../components/Notification'
import { getErrorMessage } from '../utils/notifications'

export const RegisterReaderPage: React.FC = () => {
  const [halls, setHalls] = useState<Hall[]>([])
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  const navigate = useNavigate()
  const { control, handleSubmit, reset } = useForm<ReaderCreate>({
    defaultValues: {
      card_number: '',
      full_name: '',
      passport_number: '',
      birth_date: '',
      address: '',
      phone: '',
      education_level: null,
      has_academic_degree: false,
      hall: null,
    },
  })

  useEffect(() => {
    loadHalls()
  }, [])

  const loadHalls = async () => {
    try {
      const data = await hallsAPI.getAll()
      setHalls(Array.isArray(data) ? data : [])
    } catch (error) {
      console.error('Error loading halls:', error)
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    }
  }

  const onSubmit = async (data: ReaderCreate) => {
    try {
      await staffAPI.registerReader(data)
      setNotification({
        open: true,
        message: 'Читатель успешно зарегистрирован',
        severity: 'success',
      })
      setTimeout(() => navigate('/readers'), 1500)
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    }
  }

  return (
    <Container maxWidth="md">
      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Регистрация читателя
        </Typography>
        <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ mt: 2 }}>
          <Controller
            name="card_number"
            control={control}
            rules={{ required: 'Номер билета обязателен' }}
            render={({ field, fieldState: { error } }) => (
              <TextField
                {...field}
                fullWidth
                label="Номер читательского билета*"
                margin="normal"
                error={!!error}
                helperText={error?.message}
              />
            )}
          />
          <Controller
            name="full_name"
            control={control}
            rules={{ required: 'ФИО обязательно' }}
            render={({ field, fieldState: { error } }) => (
              <TextField
                {...field}
                fullWidth
                label="ФИО*"
                margin="normal"
                error={!!error}
                helperText={error?.message}
              />
            )}
          />
          <Controller
            name="passport_number"
            control={control}
            rules={{ required: 'Номер паспорта обязателен' }}
            render={({ field, fieldState: { error } }) => (
              <TextField
                {...field}
                fullWidth
                label="Номер паспорта*"
                margin="normal"
                error={!!error}
                helperText={error?.message}
              />
            )}
          />
          <Controller
            name="birth_date"
            control={control}
            rules={{ required: 'Дата рождения обязательна' }}
            render={({ field, fieldState: { error } }) => (
              <TextField
                {...field}
                fullWidth
                label="Дата рождения*"
                type="date"
                margin="normal"
                InputLabelProps={{ shrink: true }}
                error={!!error}
                helperText={error?.message}
              />
            )}
          />
          <Controller
            name="address"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                fullWidth
                label="Адрес"
                margin="normal"
              />
            )}
          />
          <Controller
            name="phone"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                fullWidth
                label="Телефон"
                margin="normal"
              />
            )}
          />
          <Controller
            name="education_level"
            control={control}
            render={({ field }) => (
              <FormControl fullWidth margin="normal">
                <InputLabel>Уровень образования</InputLabel>
                <Select {...field} label="Уровень образования">
                  <MenuItem value={null as any}>Не указано</MenuItem>
                  <MenuItem value="начальное">Начальное</MenuItem>
                  <MenuItem value="среднее">Среднее</MenuItem>
                  <MenuItem value="высшее">Высшее</MenuItem>
                </Select>
              </FormControl>
            )}
          />
          <Controller
            name="has_academic_degree"
            control={control}
            render={({ field }) => (
              <FormControlLabel
                control={<Checkbox {...field} checked={field.value} />}
                label="Есть учёная степень"
              />
            )}
          />
          <Controller
            name="hall"
            control={control}
            render={({ field }) => (
              <FormControl fullWidth margin="normal">
                <InputLabel>Зал</InputLabel>
                <Select {...field} label="Зал">
                  <MenuItem value={null as any}>Не выбрано</MenuItem>
                  {halls.map((h) => (
                    <MenuItem key={h.hall_id} value={h.hall_id}>
                      {h.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            )}
          />

          <Box sx={{ display: 'flex', gap: 2, mt: 3 }}>
            <Button onClick={() => navigate('/readers')}>
              Отмена
            </Button>
            <Button type="submit" variant="contained">
              Зарегистрировать
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


