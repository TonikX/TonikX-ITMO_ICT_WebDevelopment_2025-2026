import React, { useEffect, useState } from 'react'
import {
  Container,
  Paper,
  Typography,
  Button,
  Box,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material'
import { DataGrid, GridColDef, GridActionsCellItem } from '@mui/x-data-grid'
import EditIcon from '@mui/icons-material/Edit'
import DeleteIcon from '@mui/icons-material/Delete'
import AddIcon from '@mui/icons-material/Add'
import PeopleIcon from '@mui/icons-material/People'
import { useForm, Controller } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'
import { hallsAPI } from '../api/halls.api'
import { Hall } from '../types'
import { Notification } from '../components/Notification'
import { ConfirmDialog } from '../components/ConfirmDialog'
import { Loading } from '../components/Loading'
import { getErrorMessage } from '../utils/notifications'

type HallFormData = {
  hall_number: number
  name: string
  capacity: number
}

export const HallsPage: React.FC = () => {
  const [halls, setHalls] = useState<Hall[]>([])
  const [loading, setLoading] = useState(true)
  const [openDialog, setOpenDialog] = useState(false)
  const [editingHall, setEditingHall] = useState<Hall | null>(null)
  const [deleteConfirm, setDeleteConfirm] = useState<{ open: boolean; id: number | null }>({
    open: false,
    id: null,
  })
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  const navigate = useNavigate()
  const { control, handleSubmit, reset } = useForm<HallFormData>({
    defaultValues: { hall_number: 0, name: '', capacity: 0 },
  })

  useEffect(() => {
    loadHalls()
  }, [])

  const loadHalls = async () => {
    try {
      setLoading(true)
      const data = await hallsAPI.getAll()
      setHalls(Array.isArray(data) ? data : [])
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

  const handleOpenDialog = (hall?: Hall) => {
    if (hall) {
      setEditingHall(hall)
      reset({
        hall_number: hall.hall_number,
        name: hall.name,
        capacity: hall.capacity,
      })
    } else {
      setEditingHall(null)
      reset({ hall_number: 0, name: '', capacity: 0 })
    }
    setOpenDialog(true)
  }

  const handleCloseDialog = () => {
    setOpenDialog(false)
    setEditingHall(null)
    reset({ hall_number: 0, name: '', capacity: 0 })
  }

  const onSubmit = async (data: HallFormData) => {
    try {
      if (editingHall) {
        await hallsAPI.update(editingHall.hall_id, data)
        setNotification({
          open: true,
          message: 'Зал успешно обновлен',
          severity: 'success',
        })
      } else {
        await hallsAPI.create(data)
        setNotification({
          open: true,
          message: 'Зал успешно создан',
          severity: 'success',
        })
      }
      handleCloseDialog()
      loadHalls()
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    }
  }

  const handleDelete = async () => {
    if (deleteConfirm.id === null) return

    try {
      await hallsAPI.delete(deleteConfirm.id)
      setNotification({
        open: true,
        message: 'Зал успешно удален',
        severity: 'success',
      })
      setDeleteConfirm({ open: false, id: null })
      loadHalls()
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    }
  }

  const columns: GridColDef[] = [
    { field: 'hall_id', headerName: 'ID', width: 90 },
    { field: 'hall_number', headerName: 'Номер зала', width: 120 },
    { field: 'name', headerName: 'Название', flex: 1 },
    { field: 'capacity', headerName: 'Вместимость', width: 150 },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Действия',
      width: 150,
      getActions: (params) => [
        <GridActionsCellItem
          icon={<PeopleIcon />}
          label="Читатели"
          onClick={() => navigate(`/halls/${params.row.hall_id}/readers`)}
        />,
        <GridActionsCellItem
          icon={<EditIcon />}
          label="Редактировать"
          onClick={() => handleOpenDialog(params.row as Hall)}
        />,
        <GridActionsCellItem
          icon={<DeleteIcon />}
          label="Удалить"
          onClick={() => setDeleteConfirm({ open: true, id: params.row.hall_id })}
        />,
      ],
    },
  ]

  if (loading) return <Loading />

  return (
    <Container maxWidth="xl" sx={{ py: 0 }}>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" fontWeight={700}>Читальные залы</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Добавить зал
        </Button>
      </Box>
      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        <DataGrid
          rows={halls}
          columns={columns}
          getRowId={(row) => row.hall_id}
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

      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingHall ? 'Редактировать зал' : 'Добавить зал'}
        </DialogTitle>
        <DialogContent>
          <Box component="form" sx={{ mt: 1 }}>
            <Controller
              name="hall_number"
              control={control}
              rules={{ required: 'Номер зала обязателен', min: { value: 1, message: 'Минимум 1' } }}
              render={({ field, fieldState: { error } }) => (
                <TextField
                  {...field}
                  fullWidth
                  label="Номер зала"
                  type="number"
                  margin="normal"
                  error={!!error}
                  helperText={error?.message}
                />
              )}
            />
            <Controller
              name="name"
              control={control}
              rules={{ required: 'Название обязательно' }}
              render={({ field, fieldState: { error } }) => (
                <TextField
                  {...field}
                  fullWidth
                  label="Название"
                  margin="normal"
                  error={!!error}
                  helperText={error?.message}
                />
              )}
            />
            <Controller
              name="capacity"
              control={control}
              rules={{ required: 'Вместимость обязательна', min: { value: 1, message: 'Минимум 1' } }}
              render={({ field, fieldState: { error } }) => (
                <TextField
                  {...field}
                  fullWidth
                  label="Вместимость"
                  type="number"
                  margin="normal"
                  error={!!error}
                  helperText={error?.message}
                />
              )}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Отмена</Button>
          <Button onClick={handleSubmit(onSubmit)} variant="contained">
            {editingHall ? 'Сохранить' : 'Создать'}
          </Button>
        </DialogActions>
      </Dialog>

      <ConfirmDialog
        open={deleteConfirm.open}
        title="Подтверждение удаления"
        message="Вы уверены, что хотите удалить этот зал?"
        onConfirm={handleDelete}
        onCancel={() => setDeleteConfirm({ open: false, id: null })}
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


