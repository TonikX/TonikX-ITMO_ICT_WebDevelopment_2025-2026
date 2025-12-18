import React, { useEffect, useState, useMemo, useCallback } from 'react' // импортируем react и основные хуки для работы со страницей
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
  Chip,
  Autocomplete,
} from '@mui/material'
import { DataGrid, GridColDef, GridActionsCellItem } from '@mui/x-data-grid'
import EditIcon from '@mui/icons-material/Edit'
import DeleteIcon from '@mui/icons-material/Delete'
import VisibilityIcon from '@mui/icons-material/Visibility'
import AddIcon from '@mui/icons-material/Add'
import { useForm, Controller } from 'react-hook-form' // хук useform и компонент controller для работы с формой книги
import { useNavigate } from 'react-router-dom'
import { booksAPI } from '../api/books.api' // api-клиент для работы с книгами
import { publishersAPI } from '../api/publishers.api'
import { sectionsAPI } from '../api/sections.api'
import { authorsAPI } from '../api/authors.api'
import { Book, Publisher, BookSection, Author, BookCreateUpdate } from '../types'
import { Notification } from '../components/Notification'
import { ConfirmDialog } from '../components/ConfirmDialog'
import { Loading } from '../components/Loading'
import { useNotification, useDeleteConfirm } from '../hooks' // кастомные хуки для уведомлений и подтверждения удаления

// компонент страницы каталога книг
export const BooksPage: React.FC = () => {
  const [books, setBooks] = useState<Book[]>([]) // локальное состояние: список книг
  const [publishers, setPublishers] = useState<Publisher[]>([]) // список издательств
  const [sections, setSections] = useState<BookSection[]>([]) // список разделов
  const [authors, setAuthors] = useState<Author[]>([]) // список авторов
  const [loading, setLoading] = useState(true) // флаг загрузки данных
  const [openDialog, setOpenDialog] = useState(false) // открыто ли модальное окно создания/редактирования книги
  const [editingBook, setEditingBook] = useState<Book | null>(null) // книга, которую редактируем (или null для создания)
  
  const { notification, showSuccess, showError, hideNotification } = useNotification() // хук уведомлений: показ успеха/ошибок
  const { deleteConfirm, openDeleteConfirm, closeDeleteConfirm } = useDeleteConfirm() // хук подтверждения удаления книги

  const navigate = useNavigate() // хук навигации для переходов на другие страницы
  const { control, handleSubmit, reset } = useForm<BookCreateUpdate>({
    // useform управляет полями формы создания/редактирования книги
    defaultValues: {
      title: '',
      cipher: '',
      publisher: null,
      publish_year: null,
      section: null,
      author_ids: [],
    },
  })

  // эффект, который один раз загружает исходные данные при монтировании страницы
  useEffect(() => {
    loadData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // Отслеживание изменений в state для отладки
  useEffect(() => {
    console.log('🔄 Books state changed:', books.length, 'books')
    if (books.length > 0) {
      console.log('📚 First book in state:', books[0])
      console.log('📚 All books IDs:', books.map(b => b.book_id))
    } else {
      console.warn('⚠️ Books array is empty!')
    }
  }, [books])

  // мемоизированная функция загрузки данных книг и связанных сущностей
  const loadData = useCallback(async () => {
    try {
      setLoading(true)
      console.log('🔄 Загрузка данных...')
      
      const booksData = await booksAPI.getAll()
      console.log('📚 Books data received:', booksData)
      console.log('📚 Books data type:', typeof booksData, Array.isArray(booksData))
      console.log('📚 Books data length:', Array.isArray(booksData) ? booksData.length : 'not array')
      
      if (Array.isArray(booksData) && booksData.length > 0) {
        console.log('📚 First book structure:', JSON.stringify(booksData[0], null, 2))
        console.log('📚 First book book_id:', booksData[0].book_id)
      }
      
      const [publishersData, sectionsData, authorsData] = await Promise.all([
        publishersAPI.getAll(),
        sectionsAPI.getAll(),
        authorsAPI.getAll(),
      ])
      
      const booksArray = Array.isArray(booksData) ? booksData : []
      const publishersArray = Array.isArray(publishersData) ? publishersData : []
      const sectionsArray = Array.isArray(sectionsData) ? sectionsData : []
      const authorsArray = Array.isArray(authorsData) ? authorsData : []
      
      console.log('✅ Before setState - booksArray:', booksArray.length, booksArray)
      
      setBooks(booksArray)
      setPublishers(publishersArray)
      setSections(sectionsArray)
      setAuthors(authorsArray)
      
      console.log('✅ State updated. Books in state:', booksArray.length)
      if (booksArray.length > 0) {
        console.log('✅ First book after setState:', booksArray[0])
      }
    } catch (error) {
      console.error('❌ Error loading data:', error)
      if (error instanceof Error) {
        console.error('❌ Error details:', error.message, error.stack)
      }
      showError(error)
    } finally {
      setLoading(false)
    }
  }, [showError])

  // открытие диалога создания/редактирования книги и подготовка значений формы
  const handleOpenDialog = (book?: Book) => {
    if (book) {
      setEditingBook(book)
      reset({
        title: book.title,
        cipher: book.cipher,
        publisher: book.publisher,
        publish_year: book.publish_year,
        section: book.section,
        author_ids: book.authors.map((a) => a.author_id),
      })
    } else {
      setEditingBook(null)
      reset({
        title: '',
        cipher: '',
        publisher: null,
        publish_year: null,
        section: null,
        author_ids: [],
      })
    }
    setOpenDialog(true)
  }

  // закрытие диалога и сброс редактируемой книги
  const handleCloseDialog = () => {
    setOpenDialog(false)
    setEditingBook(null)
  }

  // обработчик сохранения книги (создание или обновление)
  const onSubmit = useCallback(async (data: BookCreateUpdate) => {
    try {
      if (editingBook) {
        await booksAPI.update(editingBook.book_id, data)
        showSuccess('Книга успешно обновлена')
      } else {
        await booksAPI.create(data)
        showSuccess('Книга успешно создана')
      }
      handleCloseDialog()
      loadData()
    } catch (error) {
      showError(error)
    }
  }, [editingBook, loadData, showSuccess, showError])

  // обработчик удаления выбранной книги
  const handleDelete = useCallback(async () => {
    if (deleteConfirm.id === null) return

    try {
      await booksAPI.delete(deleteConfirm.id)
      showSuccess('Книга успешно удалена')
      closeDeleteConfirm()
      loadData()
    } catch (error) {
      showError(error)
    }
  }, [deleteConfirm.id, closeDeleteConfirm, loadData, showSuccess, showError])

  // описание колонок таблицы с книгами, мемоизируем с помощью usememo
  const columns: GridColDef[] = useMemo(() => [
    { field: 'book_id', headerName: 'ID', width: 70 },
    { field: 'title', headerName: 'Название', flex: 1 },
    { field: 'cipher', headerName: 'Шифр', width: 120 },
    { field: 'publisher_name', headerName: 'Издательство', width: 150 },
    { field: 'publish_year', headerName: 'Год', width: 90 },
    { field: 'section_name', headerName: 'Раздел', width: 150 },
    {
      field: 'authors',
      headerName: 'Авторы',
      width: 200,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
          {params.row.authors.map((author: Author) => (
            <Chip key={author.author_id} label={author.full_name} size="small" />
          ))}
        </Box>
      ),
    },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Действия',
      width: 150,
      getActions: (params) => [
        <GridActionsCellItem
          icon={<VisibilityIcon />}
          label="Подробнее"
          onClick={() => navigate(`/books/${params.row.book_id}`)}
        />,
        <GridActionsCellItem
          icon={<EditIcon />}
          label="Редактировать"
          onClick={() => handleOpenDialog(params.row as Book)}
        />,
        <GridActionsCellItem
          icon={<DeleteIcon />}
          label="Удалить"
          onClick={() => openDeleteConfirm(params.row.book_id)}
        />,
      ],
    },
  ], [navigate, openDeleteConfirm])

  // пока данные загружаются, показываем спиннер
  if (loading) return <Loading />

  return (
    <Container maxWidth="xl" sx={{ py: 0 }}>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" fontWeight={700}>Каталог книг</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Добавить книгу
        </Button>
      </Box>
      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        <DataGrid
          rows={books || []}
          columns={columns}
          getRowId={(row) => row.book_id}
          pagination
          initialState={{
            pagination: {
              paginationModel: { pageSize: 20 },
            },
          }}
          pageSizeOptions={[10, 20, 50, 100]}
          autoHeight
          disableRowSelectionOnClick
          loading={loading}
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

      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingBook ? 'Редактировать книгу' : 'Добавить книгу'}
        </DialogTitle>
        <DialogContent>
          <Box component="form" sx={{ mt: 1 }}>
            <Controller
              name="title"
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
              name="cipher"
              control={control}
              rules={{ required: 'Шифр обязателен' }}
              render={({ field, fieldState: { error } }) => (
                <TextField
                  {...field}
                  fullWidth
                  label="Шифр книги"
                  margin="normal"
                  error={!!error}
                  helperText={error?.message}
                />
              )}
            />
            <Controller
              name="publisher"
              control={control}
              render={({ field }) => (
                <FormControl fullWidth margin="normal">
                  <InputLabel>Издательство</InputLabel>
                  <Select 
                    {...field} 
                    label="Издательство"
                    value={field.value ?? ''}
                    onChange={(e) => field.onChange(e.target.value === '' ? null : e.target.value)}
                  >
                    <MenuItem value="">Не выбрано</MenuItem>
                    {publishers.map((p) => (
                      <MenuItem key={p.publisher_id} value={p.publisher_id}>
                        {p.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              )}
            />
            <Controller
              name="publish_year"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  fullWidth
                  label="Год издания"
                  type="number"
                  margin="normal"
                />
              )}
            />
            <Controller
              name="section"
              control={control}
              render={({ field }) => (
                <FormControl fullWidth margin="normal">
                  <InputLabel>Раздел</InputLabel>
                  <Select 
                    {...field} 
                    label="Раздел"
                    value={field.value ?? ''}
                    onChange={(e) => field.onChange(e.target.value === '' ? null : e.target.value)}
                  >
                    <MenuItem value="">Не выбрано</MenuItem>
                    {sections.map((s) => (
                      <MenuItem key={s.section_id} value={s.section_id}>
                        {s.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              )}
            />
            <Controller
              name="author_ids"
              control={control}
              render={({ field }) => (
                <Autocomplete<Author, true>
                  multiple
                  options={authors}
                  getOptionLabel={(option: Author) => option.full_name}
                  value={authors.filter((author: Author) => (field.value || []).includes(author.author_id))}
                  onChange={(_: React.SyntheticEvent, newValue: Author[]) => {
                    field.onChange(newValue.map((author: Author) => author.author_id))
                  }}
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      label="Авторы"
                      margin="normal"
                      placeholder="Выберите авторов или начните вводить имя для поиска"
                    />
                  )}
                  renderTags={(value: Author[], getTagProps) =>
                    value.map((option: Author, index: number) => (
                      <Chip
                        {...getTagProps({ index })}
                        key={option.author_id}
                        label={option.full_name}
                        size="small"
                      />
                    ))
                  }
                  sx={{ mt: 2, mb: 1 }}
                />
              )}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Отмена</Button>
          <Button onClick={handleSubmit(onSubmit)} variant="contained">
            {editingBook ? 'Сохранить' : 'Создать'}
          </Button>
        </DialogActions>
      </Dialog>

      <ConfirmDialog
        open={deleteConfirm.open}
        title="Подтверждение удаления"
        message="Вы уверены, что хотите удалить эту книгу?"
        onConfirm={handleDelete}
        onCancel={closeDeleteConfirm}
      />

      <Notification
        open={notification.open}
        message={notification.message}
        severity={notification.severity}
        onClose={hideNotification}
      />
    </Container>
  )
}


