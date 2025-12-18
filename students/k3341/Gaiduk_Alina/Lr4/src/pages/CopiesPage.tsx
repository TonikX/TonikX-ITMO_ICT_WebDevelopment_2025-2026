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
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Checkbox,
  Chip,
} from '@mui/material'
import { DataGrid, GridColDef, GridActionsCellItem } from '@mui/x-data-grid'
import EditIcon from '@mui/icons-material/Edit'
import DeleteIcon from '@mui/icons-material/Delete'
import AddIcon from '@mui/icons-material/Add'
import { useForm, Controller } from 'react-hook-form'
import { copiesAPI } from '../api/copies.api'
import { booksAPI } from '../api/books.api'
import { hallsAPI } from '../api/halls.api'
import { BookCopy, BookCopyCreate, Book, Hall } from '../types'
import { Notification } from '../components/Notification'
import { ConfirmDialog } from '../components/ConfirmDialog'
import { Loading } from '../components/Loading'
import { getErrorMessage } from '../utils/notifications'

export const CopiesPage: React.FC = () => {
  const [copies, setCopies] = useState<BookCopy[]>([])
  const [books, setBooks] = useState<Book[]>([])
  const [halls, setHalls] = useState<Hall[]>([])
  const [loading, setLoading] = useState(true)
  const [openDialog, setOpenDialog] = useState(false)
  const [editingCopy, setEditingCopy] = useState<BookCopy | null>(null)
  const [deleteConfirm, setDeleteConfirm] = useState<{ open: boolean; id: number | null }>({
    open: false,
    id: null,
  })
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  const { control, handleSubmit, reset, watch, setValue } = useForm<BookCopyCreate>({
    defaultValues: {
      book: 0,
      hall: 0,
      inventory_number: '',
      is_written_off: false,
      writeoff_date: null,
    },
  })

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [copiesData, booksData, hallsData] = await Promise.all([
        copiesAPI.getAll(),
        booksAPI.getAll(),
        hallsAPI.getAll(),
      ])
      setCopies(Array.isArray(copiesData) ? copiesData : [])
      setBooks(Array.isArray(booksData) ? booksData : [])
      setHalls(Array.isArray(hallsData) ? hallsData : [])
    } catch (error) {
      console.error('Error loading data:', error)
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    } finally {
      setLoading(false)
    }
  }

  const handleOpenDialog = (copy?: BookCopy) => {
    if (copy) {
      setEditingCopy(copy)
      reset({
        book: copy.book,
        hall: copy.hall,
        inventory_number: copy.inventory_number,
        is_written_off: copy.is_written_off,
        writeoff_date: copy.is_written_off ? copy.writeoff_date : null,
      })
    } else {
      setEditingCopy(null)
      reset({
        book: 0,
        hall: 0,
        inventory_number: '',
        is_written_off: false,
        writeoff_date: null,
      })
    }
    setOpenDialog(true)
  }

  const handleCloseDialog = () => {
    setOpenDialog(false)
    setEditingCopy(null)
  }

  const onSubmit = async (data: BookCopyCreate) => {
    try {
      // Если книга не списана, дата списания должна быть null
      const submitData: BookCopyCreate = {
        ...data,
        writeoff_date: data.is_written_off ? data.writeoff_date : null,
      }
      
      if (editingCopy) {
        await copiesAPI.update(editingCopy.copy_id, submitData)
        setNotification({
          open: true,
          message: 'Экземпляр успешно обновлен',
          severity: 'success',
        })
      } else {
        await copiesAPI.create(submitData)
        setNotification({
          open: true,
          message: 'Экземпляр успешно создан',
          severity: 'success',
        })
      }
      handleCloseDialog()
      loadData()
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
      await copiesAPI.delete(deleteConfirm.id)
      setNotification({
        open: true,
        message: 'Экземпляр успешно удален',
        severity: 'success',
      })
      setDeleteConfirm({ open: false, id: null })
      loadData()
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    }
  }

  const columns: GridColDef[] = [
    { field: 'copy_id', headerName: 'ID', width: 70 },
    { field: 'book_title', headerName: 'Книга', flex: 1 },
    { field: 'inventory_number', headerName: 'Инвентарный №', width: 180 },
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
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Действия',
      width: 120,
      getActions: (params) => [
        <GridActionsCellItem
          icon={<EditIcon />}
          label="Редактировать"
          onClick={() => handleOpenDialog(params.row as BookCopy)}
        />,
        <GridActionsCellItem
          icon={<DeleteIcon />}
          label="Удалить"
          onClick={() => setDeleteConfirm({ open: true, id: params.row.copy_id })}
        />,
      ],
    },
  ]

  if (loading) return <Loading />

  return (
    <Container maxWidth="xl" sx={{ py: 0 }}>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" fontWeight={700}>Экземпляры книг</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Добавить экземпляр
        </Button>
      </Box>
      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        <DataGrid
          rows={copies}
          columns={columns}
          getRowId={(row) => row.copy_id}
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
          {editingCopy ? 'Редактировать экземпляр' : 'Добавить экземпляр'}
        </DialogTitle>
        <DialogContent>
          <Box component="form" sx={{ mt: 1 }}>
            <Controller
              name="book"
              control={control}
              rules={{ required: 'Книга обязательна' }}
              render={({ field, fieldState: { error } }) => (
                <FormControl fullWidth margin="normal" error={!!error}>
                  <InputLabel>Книга</InputLabel>
                  <Select {...field} label="Книга">
                    {books.map((b) => (
                      <MenuItem key={b.book_id} value={b.book_id}>
                        {b.title}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              )}
            />
            <Controller
              name="hall"
              control={control}
              rules={{ required: 'Зал обязателен' }}
              render={({ field, fieldState: { error } }) => (
                <FormControl fullWidth margin="normal" error={!!error}>
                  <InputLabel>Зал</InputLabel>
                  <Select {...field} label="Зал">
                    {halls.map((h) => (
                      <MenuItem key={h.hall_id} value={h.hall_id}>
                        {h.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              )}
            />
            <Controller
              name="inventory_number"
              control={control}
              rules={{ required: 'Инвентарный номер обязателен' }}
              render={({ field, fieldState: { error } }) => (
                <TextField
                  {...field}
                  fullWidth
                  label="Инвентарный номер"
                  margin="normal"
                  error={!!error}
                  helperText={error?.message}
                />
              )}
            />
            <Controller
              name="is_written_off"
              control={control}
              render={({ field }) => (
                <FormControlLabel
                  control={
                    <Checkbox
                      {...field}
                      checked={field.value}
                      onChange={(e) => {
                        const isChecked = e.target.checked
                        field.onChange(isChecked)
                        // Если галочка снята, устанавливаем дату списания в null
                        if (!isChecked) {
                          setValue('writeoff_date', null)
                        } else {
                          // Если галочка поставлена и даты нет, устанавливаем текущую дату
                          const currentDate = watch('writeoff_date')
                          if (!currentDate) {
                            const today = new Date().toISOString().split('T')[0]
                            setValue('writeoff_date', today)
                          }
                        }
                      }}
                    />
                  }
                  label="Списана"
                />
              )}
            />
            {watch('is_written_off') && (
              <Controller
                name="writeoff_date"
                control={control}
                rules={{ required: 'Дата списания обязательна' }}
                render={({ field, fieldState: { error } }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Дата списания*"
                    type="date"
                    margin="normal"
                    InputLabelProps={{ shrink: true }}
                    value={field.value || ''}
                    onChange={(e) => field.onChange(e.target.value || null)}
                    error={!!error}
                    helperText={error?.message}
                  />
                )}
              />
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Отмена</Button>
          <Button onClick={handleSubmit(onSubmit)} variant="contained">
            {editingCopy ? 'Сохранить' : 'Создать'}
          </Button>
        </DialogActions>
      </Dialog>

      <ConfirmDialog
        open={deleteConfirm.open}
        title="Подтверждение удаления"
        message="Вы уверены, что хотите удалить этот экземпляр?"
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


