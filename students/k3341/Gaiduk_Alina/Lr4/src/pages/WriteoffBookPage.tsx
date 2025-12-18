import React, { useEffect, useState } from 'react'
import {
  Container,
  Paper,
  Typography,
  Box,
  TextField,
  Button,
  Autocomplete,
} from '@mui/material'
import { useForm, Controller } from 'react-hook-form'
import { staffAPI } from '../api/staff.api'
import { copiesAPI } from '../api/copies.api'
import { BookCopy } from '../types'
import { Notification } from '../components/Notification'
import { getErrorMessage } from '../utils/notifications'

export const WriteoffBookPage: React.FC = () => {
  const [copies, setCopies] = useState<BookCopy[]>([])
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  const { control, handleSubmit, reset } = useForm<{ copy_id: number | null }>({
    defaultValues: { copy_id: null },
  })

  useEffect(() => {
    loadCopies()
  }, [])

  const loadCopies = async () => {
    try {
      const data = await copiesAPI.getAll()
      // Фильтруем только активные экземпляры
      setCopies(data.filter((c) => !c.is_written_off))
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    }
  }

  const onSubmit = async (data: { copy_id: number | null }) => {
    if (!data.copy_id) return
    
    try {
      await staffAPI.writeoffBook(data.copy_id)
      setNotification({
        open: true,
        message: 'Книга успешно списана',
        severity: 'success',
      })
      reset()
      loadCopies()
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
          Списать книгу
        </Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          Выберите экземпляр книги для списания. Списывать можно только книги, которые не выданы читателям.
        </Typography>
        <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ mt: 2 }}>
          <Controller
            name="copy_id"
            control={control}
            rules={{ required: 'Выберите экземпляр книги' }}
            render={({ field, fieldState: { error } }) => (
              <Autocomplete<BookCopy>
                options={copies}
                getOptionLabel={(option) => 
                  `${option.book_title || 'Без названия'} - ${option.inventory_number} (${option.hall_name || 'Не указан'})`
                }
                isOptionEqualToValue={(option, value) => option.copy_id === value.copy_id}
                value={copies.find((c) => c.copy_id === field.value) || null}
                onChange={(_: React.SyntheticEvent, newValue: BookCopy | null) => {
                  field.onChange(newValue?.copy_id ?? null)
                }}
                filterOptions={(options, params) => {
                  if (!params.inputValue) return options
                  
                  const searchValue = params.inputValue.toLowerCase()
                  return options.filter((option) => {
                    const bookTitle = (option.book_title || '').toLowerCase()
                    const inventoryNumber = (option.inventory_number || '').toLowerCase()
                    const hallName = (option.hall_name || '').toLowerCase()
                    
                    return (
                      bookTitle.includes(searchValue) ||
                      inventoryNumber.includes(searchValue) ||
                      hallName.includes(searchValue)
                    )
                  })
                }}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    label="Экземпляр книги"
                    margin="normal"
                    placeholder="Начните вводить название книги, инвентарный номер или зал для поиска"
                    error={!!error}
                    helperText={error?.message}
                  />
                )}
              />
            )}
          />
          <Button type="submit" variant="contained" color="error" fullWidth sx={{ mt: 2 }}>
            Списать книгу
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


