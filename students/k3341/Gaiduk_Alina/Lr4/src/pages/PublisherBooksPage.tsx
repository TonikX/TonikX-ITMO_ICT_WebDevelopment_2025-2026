import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Container,
  Paper,
  Typography,
  Button,
  Box,
  Chip,
} from '@mui/material'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import ArrowBackIcon from '@mui/icons-material/ArrowBack'
import { publishersAPI } from '../api/publishers.api'
import { Book, Publisher } from '../types'
import { Notification } from '../components/Notification'
import { Loading } from '../components/Loading'
import { getErrorMessage } from '../utils/notifications'

export const PublisherBooksPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [publisher, setPublisher] = useState<Publisher | null>(null)
  const [books, setBooks] = useState<Book[]>([])
  const [loading, setLoading] = useState(true)
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  useEffect(() => {
    if (id) {
      loadData(parseInt(id))
    }
  }, [id])

  const loadData = async (publisherId: number) => {
    try {
      setLoading(true)
      const [publisherData, booksData] = await Promise.all([
        publishersAPI.getById(publisherId),
        publishersAPI.getBooks(publisherId),
      ])
      setPublisher(publisherData)
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
    { field: 'book_id', headerName: 'ID', width: 70 },
    { field: 'title', headerName: 'Название', flex: 1 },
    { field: 'cipher', headerName: 'Шифр', width: 120 },
    { field: 'publish_year', headerName: 'Год', width: 90 },
    { field: 'section_name', headerName: 'Раздел', width: 150 },
    {
      field: 'authors',
      headerName: 'Авторы',
      width: 200,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
          {params.row.authors.map((author: any) => (
            <Chip key={author.author_id} label={author.full_name} size="small" />
          ))}
        </Box>
      ),
    },
  ]

  if (loading) return <Loading />

  if (!publisher) {
    return (
      <Container>
        <Typography>Издательство не найдено</Typography>
      </Container>
    )
  }

  return (
    <Container maxWidth="lg">
      <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/publishers')} sx={{ mb: 2 }}>
        Назад к списку издательств
      </Button>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Книги издательства: {publisher.name}
        </Typography>
        <Box sx={{ height: 500, width: '100%', mt: 2 }}>
          <DataGrid
            rows={books}
            columns={columns}
            getRowId={(row) => row.book_id}
            pageSizeOptions={[10, 25, 50]}
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


