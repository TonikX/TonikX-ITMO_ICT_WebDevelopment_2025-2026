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
import { hallsAPI } from '../api/halls.api'
import { Reader, Hall } from '../types'
import { Notification } from '../components/Notification'
import { Loading } from '../components/Loading'
import { getErrorMessage } from '../utils/notifications'

export const HallReadersPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [hall, setHall] = useState<Hall | null>(null)
  const [readers, setReaders] = useState<Reader[]>([])
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

  const loadData = async (hallId: number) => {
    try {
      setLoading(true)
      const [hallData, readersData] = await Promise.all([
        hallsAPI.getById(hallId),
        hallsAPI.getReaders(hallId),
      ])
      setHall(hallData)
      setReaders(readersData)
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
    { field: 'reader_id', headerName: 'ID', width: 70 },
    { field: 'card_number', headerName: 'Билет №', width: 130 },
    { field: 'full_name', headerName: 'ФИО', flex: 1 },
    { field: 'age', headerName: 'Возраст', width: 90 },
    { field: 'phone', headerName: 'Телефон', width: 150 },
    { field: 'education_level', headerName: 'Образование', width: 150 },
    {
      field: 'is_active',
      headerName: 'Статус',
      width: 120,
      renderCell: (params) => (
        <Chip
          label={params.row.is_active ? 'Активен' : 'Неактивен'}
          color={params.row.is_active ? 'success' : 'default'}
          size="small"
        />
      ),
    },
  ]

  if (loading) return <Loading />

  if (!hall) {
    return (
      <Container>
        <Typography>Зал не найден</Typography>
      </Container>
    )
  }

  return (
    <Container maxWidth="lg">
      <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/halls')} sx={{ mb: 2 }}>
        Назад к списку залов
      </Button>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Читатели зала: {hall.name}
        </Typography>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          Номер зала: {hall.hall_number} | Вместимость: {hall.capacity}
        </Typography>
        <Box sx={{ height: 500, width: '100%', mt: 2 }}>
          <DataGrid
            rows={readers}
            columns={columns}
            getRowId={(row) => row.reader_id}
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


