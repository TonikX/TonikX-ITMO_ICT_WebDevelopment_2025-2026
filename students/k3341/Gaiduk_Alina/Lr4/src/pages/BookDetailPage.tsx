import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  Chip,
  Divider,
} from '@mui/material'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import ArrowBackIcon from '@mui/icons-material/ArrowBack'
import { booksAPI } from '../api/books.api'
import { Book, BookCopy } from '../types'
import { Notification } from '../components/Notification'
import { Loading } from '../components/Loading'
import { getErrorMessage } from '../utils/notifications'

export const BookDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [book, setBook] = useState<Book | null>(null)
  const [copies, setCopies] = useState<BookCopy[]>([])
  const [loading, setLoading] = useState(true)
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  useEffect(() => {
    if (id) {
      loadBookDetails(parseInt(id))
    }
  }, [id])

  const loadBookDetails = async (bookId: number) => {
    try {
      setLoading(true)
      const [bookData, copiesData] = await Promise.all([
        booksAPI.getById(bookId),
        booksAPI.getCopies(bookId),
      ])
      setBook(bookData)
      setCopies(copiesData)
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
    { field: 'copy_id', headerName: 'ID', width: 90 },
    { field: 'inventory_number', headerName: 'Инвентарный номер', width: 200 },
    { field: 'hall_name', headerName: 'Зал', width: 150 },
    { field: 'registration_date', headerName: 'Дата регистрации', width: 150 },
    {
      field: 'is_written_off',
      headerName: 'Статус',
      width: 120,
      renderCell: (params) => (
        <Chip
          label={params.row.is_written_off ? 'Списана' : 'Активна'}
          color={params.row.is_written_off ? 'error' : 'success'}
          size="small"
        />
      ),
    },
  ]

  if (loading) return <Loading />

  if (!book) {
    return (
      <Container>
        <Typography>Книга не найдена</Typography>
      </Container>
    )
  }

  return (
    <Container maxWidth="lg">
      <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/books')} sx={{ mb: 2 }}>
        Назад к списку
      </Button>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          {book.title}
        </Typography>
        <Divider sx={{ my: 2 }} />
        <Box sx={{ display: 'grid', gridTemplateColumns: '200px 1fr', gap: 2 }}>
          <Typography variant="subtitle2">Шифр:</Typography>
          <Typography>{book.cipher}</Typography>

          <Typography variant="subtitle2">Издательство:</Typography>
          <Typography>{book.publisher_name || 'Не указано'}</Typography>

          <Typography variant="subtitle2">Год издания:</Typography>
          <Typography>{book.publish_year || 'Не указан'}</Typography>

          <Typography variant="subtitle2">Раздел:</Typography>
          <Typography>{book.section_name || 'Не указан'}</Typography>

          <Typography variant="subtitle2">Авторы:</Typography>
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {book.authors.map((author) => (
              <Chip key={author.author_id} label={author.full_name} />
            ))}
          </Box>
        </Box>
      </Paper>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          Экземпляры книги
        </Typography>
        <Box sx={{ height: 400, width: '100%', mt: 2 }}>
          <DataGrid
            rows={copies}
            columns={columns}
            getRowId={(row) => row.copy_id}
            pageSizeOptions={[5, 10, 25]}
            initialState={{
              pagination: { paginationModel: { pageSize: 10 } },
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


