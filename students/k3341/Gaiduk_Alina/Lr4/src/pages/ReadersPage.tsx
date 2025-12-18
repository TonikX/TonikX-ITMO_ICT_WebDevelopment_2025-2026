import React, { useEffect, useState, useCallback, useMemo } from 'react' // используем хуки для работы с состоянием и мемоизацией
import {
  Container,
  Paper,
  Typography,
  Button,
  Box,
  Chip,
} from '@mui/material'
import { DataGrid, GridColDef, GridActionsCellItem } from '@mui/x-data-grid'
import VisibilityIcon from '@mui/icons-material/Visibility'
import EditIcon from '@mui/icons-material/Edit'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import { useNavigate } from 'react-router-dom'
import { readersAPI } from '../api/readers.api' // api-клиент для работы с читателями
import { Reader } from '../types'
import { Notification } from '../components/Notification'
import { Loading } from '../components/Loading'
import { getErrorMessage } from '../utils/notifications'

// вспомогательная функция для форматирования даты регистрации/перерегистрации
const formatDate = (dateString: string | null | undefined): string => {
  if (!dateString) return '—'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    })
  } catch {
    return dateString
  }
}

// компонент страницы списка читателей
export const ReadersPage: React.FC = () => {
  const [readers, setReaders] = useState<Reader[]>([]) // состояние: список читателей
  const [loading, setLoading] = useState(true) // состояние: идёт ли загрузка данных
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  const navigate = useNavigate() // хук навигации для переходов на страницы деталей и редактирования

  // мемоизированная функция загрузки списка читателей с сервера
  const loadReaders = useCallback(async () => {
    try {
      setLoading(true)
      const data = await readersAPI.getAll()
      setReaders(Array.isArray(data) ? data : [])
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    } finally {
      setLoading(false)
    }
  }, [])

  // эффект: загружаем читателей при первом рендере
  useEffect(() => {
    loadReaders()
  }, [loadReaders])

  // обработчик активации выбранного читателя
  const handleActivateReader = useCallback(async (readerId: number) => {
    try {
      await readersAPI.update(readerId, { is_active: true })
      setNotification({
        open: true,
        message: 'Читатель успешно активирован',
        severity: 'success',
      })
      // Перезагружаем данные для обновления всех полей
      await loadReaders()
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    }
  }, [loadReaders])

  // конфигурация колонок таблицы с читателями, мемоизируем чтобы не пересоздавать на каждый рендер
  const columns: GridColDef[] = useMemo(
    () => [
      { field: 'reader_id', headerName: 'ID', width: 70 },
      { field: 'card_number', headerName: 'Билет №', width: 130 },
      { field: 'full_name', headerName: 'ФИО', flex: 1 },
      { field: 'age', headerName: 'Возраст', width: 90 },
      { field: 'phone', headerName: 'Телефон', width: 150 },
      { field: 'hall_name', headerName: 'Зал', width: 150 },
      {
        field: 'registration_date',
        headerName: 'Дата регистрации',
        width: 150,
        renderCell: (params) => formatDate(params.row.registration_date),
      },
      {
        field: 'last_reregistration_date',
        headerName: 'Дата последней перерегистрации',
        width: 220,
        renderCell: (params) => formatDate(params.row.last_reregistration_date),
      },
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
      {
        field: 'actions',
        type: 'actions',
        headerName: 'Действия',
        width: 180,
        getActions: (params) => {
          const actions = [
            <GridActionsCellItem
              key="view"
              icon={<VisibilityIcon />}
              label="Подробнее"
              onClick={() => navigate(`/readers/${params.row.reader_id}`)}
            />,
            <GridActionsCellItem
              key="edit"
              icon={<EditIcon />}
              label="Редактировать"
              onClick={() => navigate(`/readers/${params.row.reader_id}/edit`)}
            />,
          ]

          // Добавляем кнопку активации только для неактивных читателей
          if (!params.row.is_active) {
            actions.push(
              <GridActionsCellItem
                key="activate"
                icon={<CheckCircleIcon />}
                label="Активировать"
                onClick={() => handleActivateReader(params.row.reader_id)}
                sx={{ color: 'success.main' }}
              />
            )
          }

          return actions
        },
      },
    ],
    [navigate, handleActivateReader]
  )

  // показываем индикатор загрузки, пока данные ещё приходят
  if (loading) return <Loading />

  return (
    <Container maxWidth="xl" sx={{ py: 0 }}>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" fontWeight={700}>Читатели</Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            onClick={() => navigate('/deactivate-readers')}
          >
            Деактивировать старых
          </Button>
          <Button
            variant="contained"
            onClick={() => navigate('/register-reader')}
          >
            Зарегистрировать читателя
          </Button>
        </Box>
      </Box>
      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        <DataGrid
          rows={readers}
          columns={columns}
          getRowId={(row) => row.reader_id}
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


