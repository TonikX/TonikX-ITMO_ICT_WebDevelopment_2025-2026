import React, { useEffect, useState } from 'react'
import {
  Container,
  Paper,
  Typography,
  Box,
} from '@mui/material'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import { stocksAPI } from '../api/stocks.api'
import { HallBookStock } from '../types'
import { Notification } from '../components/Notification'
import { Loading } from '../components/Loading'
import { getErrorMessage } from '../utils/notifications'

export const StocksPage: React.FC = () => {
  const [stocks, setStocks] = useState<HallBookStock[]>([])
  const [loading, setLoading] = useState(true)
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  useEffect(() => {
    loadStocks()
  }, [])

  const loadStocks = async () => {
    try {
      setLoading(true)
      const data = await stocksAPI.getAll()
      setStocks(Array.isArray(data) ? data : [])
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
    { field: 'hall_name', headerName: 'Зал', width: 200 },
    { field: 'book_title', headerName: 'Книга', flex: 1 },
    { field: 'copies_total', headerName: 'Количество экземпляров', width: 200 },
  ]

  if (loading) return <Loading />

  return (
    <Container maxWidth="xl" sx={{ py: 0 }}>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" fontWeight={700}>
          Остатки книг по залам
        </Typography>
      </Box>
      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        <DataGrid
          rows={stocks}
          columns={columns}
          getRowId={(row) => row.id}
          pagination
          paginationModel={{ page: 0, pageSize: 20 }}
          pageSizeOptions={[20]}
          autoHeight
          disableRowSelectionOnClick
          sx={{
            '& .MuiDataGrid-cell:focus': {
              outline: 'none',
            },
            '& .MuiDataGrid-row:hover': {
              bgcolor: 'rgba(99, 102, 241, 0.04)',
            },
          }}
        />
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


