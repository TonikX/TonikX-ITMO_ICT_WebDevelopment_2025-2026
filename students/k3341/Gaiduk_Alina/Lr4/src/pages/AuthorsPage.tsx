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
import { useForm, Controller } from 'react-hook-form'
import { authorsAPI } from '../api/authors.api'
import { Author } from '../types'
import { Notification } from '../components/Notification'
import { ConfirmDialog } from '../components/ConfirmDialog'
import { Loading } from '../components/Loading'
import { getErrorMessage } from '../utils/notifications'

export const AuthorsPage: React.FC = () => {
  const [authors, setAuthors] = useState<Author[]>([])
  const [loading, setLoading] = useState(true)
  const [openDialog, setOpenDialog] = useState(false)
  const [editingAuthor, setEditingAuthor] = useState<Author | null>(null)
  const [deleteConfirm, setDeleteConfirm] = useState<{ open: boolean; id: number | null }>({
    open: false,
    id: null,
  })
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  const { control, handleSubmit, reset } = useForm<{ full_name: string }>({
    defaultValues: { full_name: '' },
  })

  useEffect(() => {
    loadAuthors()
  }, [])

  const loadAuthors = async () => {
    try {
      setLoading(true)
      const data = await authorsAPI.getAll()
      setAuthors(Array.isArray(data) ? data : [])
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

  const handleOpenDialog = (author?: Author) => {
    if (author) {
      setEditingAuthor(author)
      reset({ full_name: author.full_name })
    } else {
      setEditingAuthor(null)
      reset({ full_name: '' })
    }
    setOpenDialog(true)
  }

  const handleCloseDialog = () => {
    setOpenDialog(false)
    setEditingAuthor(null)
    reset({ full_name: '' })
  }

  const onSubmit = async (data: { full_name: string }) => {
    try {
      if (editingAuthor) {
        await authorsAPI.update(editingAuthor.author_id, data)
        setNotification({
          open: true,
          message: 'Автор успешно обновлен',
          severity: 'success',
        })
      } else {
        await authorsAPI.create(data)
        setNotification({
          open: true,
          message: 'Автор успешно создан',
          severity: 'success',
        })
      }
      handleCloseDialog()
      loadAuthors()
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
      await authorsAPI.delete(deleteConfirm.id)
      setNotification({
        open: true,
        message: 'Автор успешно удален',
        severity: 'success',
      })
      setDeleteConfirm({ open: false, id: null })
      loadAuthors()
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    }
  }

  const columns: GridColDef[] = [
    { field: 'author_id', headerName: 'ID', width: 90 },
    { field: 'full_name', headerName: 'Полное имя', flex: 1 },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Действия',
      width: 120,
      getActions: (params) => [
        <GridActionsCellItem
          icon={<EditIcon />}
          label="Редактировать"
          onClick={() => handleOpenDialog(params.row as Author)}
        />,
        <GridActionsCellItem
          icon={<DeleteIcon />}
          label="Удалить"
          onClick={() => setDeleteConfirm({ open: true, id: params.row.author_id })}
        />,
      ],
    },
  ]

  if (loading) return <Loading />

  return (
    <Container maxWidth="xl" sx={{ py: 0 }}>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" fontWeight={700}>Авторы</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Добавить автора
        </Button>
      </Box>
      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        <DataGrid
          rows={authors}
          columns={columns}
          getRowId={(row) => row.author_id}
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
        <DialogTitle>{editingAuthor ? 'Редактировать автора' : 'Добавить автора'}</DialogTitle>
        <DialogContent>
          <Box component="form" sx={{ mt: 1 }}>
            <Controller
              name="full_name"
              control={control}
              rules={{ required: 'Полное имя обязательно' }}
              render={({ field, fieldState: { error } }) => (
                <TextField
                  {...field}
                  fullWidth
                  label="Полное имя"
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
            {editingAuthor ? 'Сохранить' : 'Создать'}
          </Button>
        </DialogActions>
      </Dialog>

      <ConfirmDialog
        open={deleteConfirm.open}
        title="Подтверждение удаления"
        message="Вы уверены, что хотите удалить этого автора?"
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


