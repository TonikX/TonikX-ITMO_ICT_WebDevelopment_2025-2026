import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  Divider,
  Chip,
} from '@mui/material'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import ArrowBackIcon from '@mui/icons-material/ArrowBack'
import EditIcon from '@mui/icons-material/Edit'
import { readersAPI } from '../api/readers.api'
import { Reader, BookIssue } from '../types'
import { Notification } from '../components/Notification'
import { Loading } from '../components/Loading'
import { getErrorMessage } from '../utils/notifications'

export const ReaderDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [reader, setReader] = useState<Reader | null>(null)
  const [books, setBooks] = useState<BookIssue[]>([])
  const [loading, setLoading] = useState(true)
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  useEffect(() => {
    if (id) {
      loadReaderDetails(parseInt(id))
    }
  }, [id])

  const loadReaderDetails = async (readerId: number) => {
    try {
      setLoading(true)
      const [readerData, booksData] = await Promise.all([
        readersAPI.getById(readerId),
        readersAPI.getBooks(readerId),
      ])
      setReader(readerData)
      setBooks(booksData)
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

  const columns: GridColDef[] = [
    { field: 'issue_id', headerName: 'ID', width: 70 },
    { field: 'book_title', headerName: 'Книга', flex: 1 },
    { field: 'copy_inventory', headerName: 'Инв. №', width: 120 },
    { field: 'hall_name', headerName: 'Зал', width: 150 },
    { field: 'issue_date', headerName: 'Дата выдачи', width: 120 },
  ]

  if (loading) return <Loading />

  if (!reader) {
    return (
      <Container>
        <Typography>Читатель не найден</Typography>
      </Container>
    )
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/readers')}>
          Назад к списку
        </Button>
        <Button
          variant="outlined"
          startIcon={<EditIcon />}
          onClick={() => navigate(`/readers/${id}/edit`)}
        >
          Редактировать
        </Button>
      </Box>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          {reader.full_name}
        </Typography>
        <Chip
          label={reader.is_active ? 'Активен' : 'Неактивен'}
          color={reader.is_active ? 'success' : 'default'}
          sx={{ mb: 2 }}
        />
        <Divider sx={{ my: 2 }} />
        <Box sx={{ display: 'grid', gridTemplateColumns: '200px 1fr', gap: 2 }}>
          <Typography variant="subtitle2">Номер билета:</Typography>
          <Typography>{reader.card_number}</Typography>

          <Typography variant="subtitle2">Паспорт:</Typography>
          <Typography>{reader.passport_number}</Typography>

          <Typography variant="subtitle2">Дата рождения:</Typography>
          <Typography>{reader.birth_date} ({reader.age} лет)</Typography>

          <Typography variant="subtitle2">Адрес:</Typography>
          <Typography>{reader.address || 'Не указан'}</Typography>

          <Typography variant="subtitle2">Телефон:</Typography>
          <Typography>{reader.phone || 'Не указан'}</Typography>

          <Typography variant="subtitle2">Образование:</Typography>
          <Typography>{reader.education_level || 'Не указано'}</Typography>

          <Typography variant="subtitle2">Учёная степень:</Typography>
          <Typography>{reader.has_academic_degree ? 'Есть' : 'Нет'}</Typography>

          <Typography variant="subtitle2">Зал:</Typography>
          <Typography>{reader.hall_name || 'Не закреплён'}</Typography>

          <Typography variant="subtitle2">Дата регистрации:</Typography>
          <Typography>{reader.registration_date}</Typography>

          {reader.last_reregistration_date && (
            <>
              <Typography variant="subtitle2">Последняя перерегистрация:</Typography>
              <Typography>{reader.last_reregistration_date}</Typography>
            </>
          )}
        </Box>
      </Paper>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          Книги на руках
        </Typography>
        <Box sx={{ height: 400, width: '100%', mt: 2 }}>
          <DataGrid
            rows={books}
            columns={columns}
            getRowId={(row) => row.issue_id}
            pageSizeOptions={[5, 10, 25]}
            initialState={{
              pagination: { paginationModel: { pageSize: 5 } },
            }}
          />
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


