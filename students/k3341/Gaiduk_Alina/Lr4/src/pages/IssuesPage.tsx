import React, { useEffect, useState } from 'react' // используем хуки для состояния и эффекта загрузки
import {
  Container,
  Paper,
  Typography,
  Button,
  Box,
  Chip,
} from '@mui/material'
import { DataGrid, GridColDef, GridActionsCellItem } from '@mui/x-data-grid'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import AddIcon from '@mui/icons-material/Add'
import { useNavigate } from 'react-router-dom'
import { issuesAPI } from '../api/issues.api' // api-клиент для работы с выдачами книг
import { BookIssue } from '../types'
import { Notification } from '../components/Notification'
import { ConfirmDialog } from '../components/ConfirmDialog'
import { Loading } from '../components/Loading'
import { getErrorMessage } from '../utils/notifications'

// компонент страницы со списком текущих и завершённых выдач
export const IssuesPage: React.FC = () => {
  const [issues, setIssues] = useState<BookIssue[]>([]) // состояние: список выдач
  const [loading, setLoading] = useState(true) // состояние: идёт ли загрузка
  const [returnConfirm, setReturnConfirm] = useState<{ open: boolean; id: number | null }>({
    open: false,
    id: null,
  })
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  const navigate = useNavigate() // хук навигации: переход на страницу "выдать книгу"

  // эффект: загружаем список выдач при монтировании страницы
  useEffect(() => {
    loadIssues()
  }, [])

  // функция загрузки всех выдач с сервера
  const loadIssues = async () => {
    try {
      setLoading(true)
      const data = await issuesAPI.getAll()
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

  // обработчик подтверждения возврата книги
  const handleReturn = async () => {
    if (returnConfirm.id === null) return

    try {
      const today = new Date().toISOString().split('T')[0]
      await issuesAPI.returnBook(returnConfirm.id, today)
      setNotification({
        open: true,
        message: 'Книга успешно возвращена',
        severity: 'success',
      })
      setReturnConfirm({ open: false, id: null })
      loadIssues()
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    }
  }

  // описание колонок таблицы выдач
  const columns: GridColDef[] = [
    { field: 'issue_id', headerName: 'ID', width: 70 },
    { field: 'reader_name', headerName: 'Читатель', flex: 1 },
    { field: 'reader_card', headerName: 'Билет №', width: 120 },
    { field: 'book_title', headerName: 'Книга', flex: 1 },
    { field: 'copy_inventory', headerName: 'Инв. №', width: 120 },
    { field: 'hall_name', headerName: 'Зал', width: 120 },
    { field: 'issue_date', headerName: 'Дата выдачи', width: 120 },
    { field: 'return_date', headerName: 'Дата возврата', width: 120 },
    {
      field: 'is_returned',
      headerName: 'Статус',
      width: 120,
      renderCell: (params) => (
        <Chip
          label={params.row.is_returned ? 'Возвращена' : 'На руках'}
          color={params.row.is_returned ? 'success' : 'warning'}
          size="small"
        />
      ),
    },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Действия',
      width: 100,
      getActions: (params) => {
        if (params.row.is_returned) return []
        return [
          <GridActionsCellItem
            icon={<CheckCircleIcon />}
            label="Вернуть"
            onClick={() => setReturnConfirm({ open: true, id: params.row.issue_id })}
          />,
        ]
      },
    },
  ]

  // если данные ещё грузятся, показываем индикатор загрузки
  if (loading) return <Loading />

  return (
    <Container maxWidth="xl" sx={{ py: 0 }}>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" fontWeight={700}>Выдачи книг</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => navigate('/issue-book')}
        >
          Выдать книгу
        </Button>
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

      <ConfirmDialog
        open={returnConfirm.open}
        title="Подтверждение возврата"
        message="Вы уверены, что хотите отметить эту книгу как возвращённую?"
        onConfirm={handleReturn}
        onCancel={() => setReturnConfirm({ open: false, id: null })}
      />

      <Notification
        open={notification.open}
        message={notification.message}
        severity={notification.severity}
        onClose={() => setNotification({ ...notification, open: false })}
      />
    </Container>
  )
}


