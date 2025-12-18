import React, { useEffect, useState } from 'react'
import {
  Container,
  Paper,
  Typography,
  Box,
} from '@mui/material'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import { issuesAPI } from '../api/issues.api'
import { BookIssue } from '../types'
import { Notification } from '../components/Notification'
import { Loading } from '../components/Loading'
import { getErrorMessage } from '../utils/notifications'

export const RareBooksPage: React.FC = () => {
  const [issues, setIssues] = useState<BookIssue[]>([])
  const [loading, setLoading] = useState(true)
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  useEffect(() => {
    loadRareBooks()
  }, [])

  const loadRareBooks = async () => {
    try {
      setLoading(true)
      const data = await issuesAPI.getRareBooks()
      setIssues(Array.isArray(data) ? data : [])
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
    { field: 'reader_name', headerName: 'Читатель', flex: 1 },
    { field: 'book_title', headerName: 'Редкая книга', flex: 1 },
    { field: 'copy_inventory', headerName: 'Инв. №', width: 120 },
    { field: 'issue_date', headerName: 'Дата выдачи', width: 120 },
    { field: 'hall_name', headerName: 'Зал', width: 150 },
  ]

  if (loading) return <Loading />

  return (
    <Container maxWidth="xl" sx={{ py: 0 }}>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" fontWeight={700}>
          Читатели с редкими книгами (≤ 2 экземпляра)
        </Typography>
      </Box>
      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        <DataGrid
          rows={issues}
          columns={columns}
          getRowId={(row) => row.issue_id}
          pagination
          initialState={{
            pagination: {
              paginationModel: { pageSize: 20 },
            },
          }}
          pageSizeOptions={[10, 20, 50, 100]}
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


