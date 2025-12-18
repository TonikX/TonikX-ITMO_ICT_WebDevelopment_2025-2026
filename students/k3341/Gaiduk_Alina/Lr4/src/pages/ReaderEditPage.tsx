import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
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
import { readersAPI } from '../api/readers.api'
import { hallsAPI } from '../api/halls.api'
import { Hall, Reader, ReaderCreate } from '../types'
import { Notification } from '../components/Notification'
import { Loading } from '../components/Loading'
import { getErrorMessage } from '../utils/notifications'

export const ReaderEditPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [halls, setHalls] = useState<Hall[]>([])
  const [loading, setLoading] = useState(true)
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  const { control, handleSubmit, reset } = useForm<ReaderCreate & { last_reregistration_date?: string | null }>()

  useEffect(() => {
    if (id) {
      loadData(parseInt(id))
    }
  }, [id])

  const loadData = async (readerId: number) => {
    try {
      setLoading(true)
      const [readerData, hallsData] = await Promise.all([
        readersAPI.getById(readerId),
        hallsAPI.getAll(),
      ])
      setHalls(hallsData)
      reset({
        card_number: readerData.card_number,
        full_name: readerData.full_name,
        passport_number: readerData.passport_number,
        birth_date: readerData.birth_date,
        address: readerData.address,
        phone: readerData.phone,
        education_level: readerData.education_level,
        has_academic_degree: readerData.has_academic_degree,
        hall: readerData.hall,
        last_reregistration_date: readerData.last_reregistration_date || '',
      })
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

  const onSubmit = async (data: ReaderCreate & { last_reregistration_date?: string | null }) => {
    if (!id) return

    try {
      await readersAPI.update(parseInt(id), {
        ...data,
        last_reregistration_date: data.last_reregistration_date || null,
      })
      setNotification({
        open: true,
        message: 'Читатель успешно обновлен',
        severity: 'success',
      })
      setTimeout(() => navigate(`/readers/${id}`), 1500)
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    }
  }

  if (loading) return <Loading />

  return (
    <Container maxWidth="md">
      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Редактирование читателя
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
                value={field.value || ''}
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
                value={field.value || ''}
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
                <Select {...field} value={field.value || ''} label="Уровень образования">
                  <MenuItem value="">Не указано</MenuItem>
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
                control={<Checkbox {...field} checked={field.value || false} />}
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
                <Select {...field} value={field.value || ''} label="Зал">
                  <MenuItem value="">Не выбрано</MenuItem>
                  {halls.map((h) => (
                    <MenuItem key={h.hall_id} value={h.hall_id}>
                      {h.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            )}
          />
          <Controller
            name="last_reregistration_date"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                fullWidth
                label="Дата последней перерегистрации"
                type="date"
                margin="normal"
                InputLabelProps={{ shrink: true }}
                value={field.value || ''}
                onChange={(e) => field.onChange(e.target.value || null)}
              />
            )}
          />

          <Box sx={{ display: 'flex', gap: 2, mt: 3 }}>
            <Button onClick={() => navigate(`/readers/${id}`)}>
              Отмена
            </Button>
            <Button type="submit" variant="contained">
              Сохранить изменения
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


