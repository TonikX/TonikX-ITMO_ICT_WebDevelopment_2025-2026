import React, { useEffect, useState } from 'react'
import {
  Container,
  Paper,
  Typography,
  Box,
  TextField,
  Button,
  Autocomplete,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material'
import { useForm, Controller } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'
import { issuesAPI } from '../api/issues.api'
import { readersAPI } from '../api/readers.api'
import { copiesAPI } from '../api/copies.api'
import { hallsAPI } from '../api/halls.api'
import { BookIssueCreate, Reader, BookCopy, Hall } from '../types'
import { Notification } from '../components/Notification'
import { getErrorMessage } from '../utils/notifications'

export const IssueBookPage: React.FC = () => {
  const [readers, setReaders] = useState<Reader[]>([])
  const [copies, setCopies] = useState<BookCopy[]>([])
  const [halls, setHalls] = useState<Hall[]>([])
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  const navigate = useNavigate()
  const { control, handleSubmit, reset } = useForm<BookIssueCreate>({
    defaultValues: {
      reader: null as any,
      copy: null as any,
      hall: null as any,
    },
  })

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [readersData, copiesData, hallsData] = await Promise.all([
        readersAPI.getAll(),
        copiesAPI.getAll(),
        hallsAPI.getAll(),
      ])
      setReaders(Array.isArray(readersData) ? readersData.filter((r) => r.is_active) : [])
      setCopies(Array.isArray(copiesData) ? copiesData.filter((c) => !c.is_written_off) : [])
      setHalls(Array.isArray(hallsData) ? hallsData : [])
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    }
  }

  const onSubmit = async (data: BookIssueCreate) => {
    try {
      await issuesAPI.create(data)
      setNotification({
        open: true,
        message: 'Книга успешно выдана',
        severity: 'success',
      })
      setTimeout(() => navigate('/issues'), 1500)
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
          Выдать книгу
        </Typography>
        <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ mt: 2 }}>
          <Controller
            name="reader"
            control={control}
            rules={{ required: 'Выберите читателя' }}
            render={({ field, fieldState: { error } }) => (
              <Autocomplete<Reader>
                options={readers}
                getOptionLabel={(option) => `${option.full_name} (${option.card_number})`}
                isOptionEqualToValue={(option, value) => option.reader_id === value.reader_id}
                value={readers.find((r) => r.reader_id === field.value) || null}
                onChange={(_: React.SyntheticEvent, newValue: Reader | null) => {
                  field.onChange(newValue?.reader_id ?? null)
                }}
                filterOptions={(options, params) => {
                  if (!params.inputValue) return options
                  
                  const searchValue = params.inputValue.toLowerCase()
                  return options.filter((option) => {
                    const fullName = (option.full_name || '').toLowerCase()
                    const cardNumber = (option.card_number || '').toLowerCase()
                    
                    return (
                      fullName.includes(searchValue) ||
                      cardNumber.includes(searchValue)
                    )
                  })
                }}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    label="Читатель*"
                    margin="normal"
                    placeholder="Начните вводить ФИО или номер билета для поиска"
                    error={!!error}
                    helperText={error?.message}
                  />
                )}
              />
            )}
          />
          <Controller
            name="copy"
            control={control}
            rules={{ required: 'Выберите экземпляр книги' }}
            render={({ field, fieldState: { error } }) => (
              <Autocomplete<BookCopy>
                options={copies}
                getOptionLabel={(option) => 
                  `${option.book_title || 'Без названия'} - ${option.inventory_number}${option.hall_name ? ` (${option.hall_name})` : ''}`
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
                    label="Экземпляр книги*"
                    margin="normal"
                    placeholder="Начните вводить название книги, инвентарный номер или зал для поиска"
                    error={!!error}
                    helperText={error?.message}
                  />
                )}
              />
            )}
          />
          <Controller
            name="hall"
            control={control}
            rules={{ required: 'Выберите зал', min: { value: 1, message: 'Выберите зал' } }}
            render={({ field, fieldState: { error } }) => (
              <FormControl fullWidth margin="normal" error={!!error}>
                <InputLabel>Зал*</InputLabel>
                <Select 
                  {...field} 
                  value={field.value || ''} 
                  label="Зал*"
                  onChange={(e) => field.onChange(e.target.value ? Number(e.target.value) : null)}
                >
                  <MenuItem value="">Выберите зал</MenuItem>
                  {halls.map((h) => (
                    <MenuItem key={h.hall_id} value={h.hall_id}>
                      {h.name}
                    </MenuItem>
                  ))}
                </Select>
                {error && <Typography variant="caption" color="error" sx={{ ml: 2, mt: 0.5, display: 'block' }}>{error.message}</Typography>}
              </FormControl>
            )}
          />

          <Box sx={{ display: 'flex', gap: 2, mt: 3 }}>
            <Button onClick={() => navigate('/issues')}>
              Отмена
            </Button>
            <Button type="submit" variant="contained">
              Выдать книгу
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


