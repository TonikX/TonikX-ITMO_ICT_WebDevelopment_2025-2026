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
import VisibilityIcon from '@mui/icons-material/Visibility'
import { useForm, Controller } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'
import { publishersAPI } from '../api/publishers.api'
import { Publisher } from '../types'
import { Notification } from '../components/Notification'
import { ConfirmDialog } from '../components/ConfirmDialog'
import { Loading } from '../components/Loading'
import { getErrorMessage } from '../utils/notifications'

export const PublishersPage: React.FC = () => {
  const [publishers, setPublishers] = useState<Publisher[]>([])
  const [loading, setLoading] = useState(true)
  const [openDialog, setOpenDialog] = useState(false)
  const [editingPublisher, setEditingPublisher] = useState<Publisher | null>(null)
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
  const { control, handleSubmit, reset } = useForm<{ name: string }>({
    defaultValues: { name: '' },
  })

  useEffect(() => {
    loadPublishers()
  }, [])

  const loadPublishers = async () => {
    try {
      setLoading(true)
      const data = await publishersAPI.getAll()
      setPublishers(Array.isArray(data) ? data : [])
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

  const handleOpenDialog = (publisher?: Publisher) => {
    if (publisher) {
      setEditingPublisher(publisher)
      reset({ name: publisher.name })
    } else {
      setEditingPublisher(null)
      reset({ name: '' })
    }
    setOpenDialog(true)
  }

  const handleCloseDialog = () => {
    setOpenDialog(false)
    setEditingPublisher(null)
    reset({ name: '' })
  }

  const onSubmit = async (data: { name: string }) => {
    try {
      if (editingPublisher) {
        await publishersAPI.update(editingPublisher.publisher_id, data)
        setNotification({
          open: true,
          message: 'Издательство успешно обновлено',
          severity: 'success',
        })
      } else {
        await publishersAPI.create(data)
        setNotification({
          open: true,
          message: 'Издательство успешно создано',
          severity: 'success',
        })
      }
      handleCloseDialog()
      loadPublishers()
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
      await publishersAPI.delete(deleteConfirm.id)
      setNotification({
        open: true,
        message: 'Издательство успешно удалено',
        severity: 'success',
      })
      setDeleteConfirm({ open: false, id: null })
      loadPublishers()
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    }
  }

  const columns: GridColDef[] = [
    { field: 'publisher_id', headerName: 'ID', width: 90 },
    { field: 'name', headerName: 'Название', flex: 1 },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Действия',
      width: 150,
      getActions: (params) => [
        <GridActionsCellItem
          icon={<VisibilityIcon />}
          label="Книги"
          onClick={() => navigate(`/publishers/${params.row.publisher_id}/books`)}
        />,
        <GridActionsCellItem
          icon={<EditIcon />}
          label="Редактировать"
          onClick={() => handleOpenDialog(params.row as Publisher)}
        />,
        <GridActionsCellItem
          icon={<DeleteIcon />}
          label="Удалить"
          onClick={() => setDeleteConfirm({ open: true, id: params.row.publisher_id })}
        />,
      ],
    },
  ]

  if (loading) return <Loading />

  return (
    <Container maxWidth="xl" sx={{ py: 0 }}>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" fontWeight={700}>Издательства</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Добавить издательство
        </Button>
      </Box>
      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        <DataGrid
          rows={publishers}
          columns={columns}
          getRowId={(row) => row.publisher_id}
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
          {editingPublisher ? 'Редактировать издательство' : 'Добавить издательство'}
        </DialogTitle>
        <DialogContent>
          <Box component="form" sx={{ mt: 1 }}>
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
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Отмена</Button>
          <Button onClick={handleSubmit(onSubmit)} variant="contained">
            {editingPublisher ? 'Сохранить' : 'Создать'}
          </Button>
        </DialogActions>
      </Dialog>

      <ConfirmDialog
        open={deleteConfirm.open}
        title="Подтверждение удаления"
        message="Вы уверены, что хотите удалить это издательство?"
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


