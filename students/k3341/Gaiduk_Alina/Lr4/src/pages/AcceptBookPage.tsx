import React, { useEffect, useState } from 'react' // используем хуки для работы с локальным состоянием и эффектами
import {
  Container,
  Paper,
  Typography,
  Box,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Divider,
  Autocomplete,
  Chip,
} from '@mui/material'
import { useForm, Controller } from 'react-hook-form' // хук useform и компонент controller для управления формой
import { staffAPI } from '../api/staff.api'
import { booksAPI } from '../api/books.api'
import { hallsAPI } from '../api/halls.api'
import { publishersAPI } from '../api/publishers.api'
import { sectionsAPI } from '../api/sections.api'
import { authorsAPI } from '../api/authors.api'
import { BookAcceptData, Book, Hall, Publisher, BookSection, Author } from '../types'
import { Notification } from '../components/Notification' // компонент уведомлений об успехе/ошибке
import { getErrorMessage } from '../utils/notifications'

// страница приёма книги в фонд библиотеки
export const AcceptBookPage: React.FC = () => {
  const [books, setBooks] = useState<Book[]>([]) // список доступных книг (для выбора существующей)
  const [halls, setHalls] = useState<Hall[]>([]) // список залов библиотеки
  const [publishers, setPublishers] = useState<Publisher[]>([]) // список издательств
  const [sections, setSections] = useState<BookSection[]>([]) // список разделов
  const [authors, setAuthors] = useState<Author[]>([]) // список авторов
  const [isNewBook, setIsNewBook] = useState(false) // флаг: создаём новую книгу или выбираем существующую
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  // useform управляет состоянием формы приёма книги
  const { control, handleSubmit, reset, watch } = useForm<BookAcceptData>({
    defaultValues: {
      book_id: null,
      title: '',
      publisher: null,
      publish_year: null,
      section: null,
      cipher: '',
      author_ids: [],
      hall: null as any,
      inventory_number: '',
    },
  })

  // эффект: при первом рендере загружаем справочники (книги, залы, издательства и т.д.)
  useEffect(() => {
    loadData()
  }, [])

  // функция загрузки всех необходимых данных для формы
  const loadData = async () => {
    try {
      const [booksData, hallsData, publishersData, sectionsData, authorsData] = await Promise.all([
        booksAPI.getAll(),
        hallsAPI.getAll(),
        publishersAPI.getAll(),
        sectionsAPI.getAll(),
        authorsAPI.getAll(),
      ])
      setBooks(Array.isArray(booksData) ? booksData : [])
      setHalls(Array.isArray(hallsData) ? hallsData : [])
      setPublishers(Array.isArray(publishersData) ? publishersData : [])
      setSections(Array.isArray(sectionsData) ? sectionsData : [])
      setAuthors(Array.isArray(authorsData) ? authorsData : [])
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    }
  }

  const bookId = watch('book_id') // отслеживаем выбранный book_id, чтобы понять новая это книга или существующая

  // эффект: обновляем флаг isNewBook при изменении выбранной книги
  useEffect(() => {
    const newIsNewBook = bookId === null || bookId === undefined
    setIsNewBook(newIsNewBook)
  }, [bookId])

  // обработчик отправки формы приёма книги в фонд
  const onSubmit = async (data: BookAcceptData) => {
    try {
      // формируем данные для отправки в зависимости от того, новая книга или существующая
      const submitData: BookAcceptData = {
        hall: data.hall,
        inventory_number: data.inventory_number,
      }
      
      if (isNewBook) {
        // Для новой книги добавляем все поля
        submitData.title = data.title
        submitData.cipher = data.cipher
        submitData.publisher = data.publisher ?? undefined
        submitData.publish_year = data.publish_year ?? undefined
        submitData.section = data.section ?? undefined
        submitData.author_ids = data.author_ids ?? undefined
      } else {
        // Для существующей книги указываем только book_id
        submitData.book_id = data.book_id ?? undefined
      }
      
      await staffAPI.acceptBook(submitData)
      setNotification({
        open: true,
        message: 'Книга успешно принята в фонд',
        severity: 'success',
      })
      reset()
      loadData()
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    }
  }

  return (
    <Container maxWidth="md">
      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Принять книгу в фонд
        </Typography>
        <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ mt: 2 }}>
          <Controller
            name="book_id"
            control={control}
            render={({ field }) => (
              <Autocomplete<Book | null>
                options={[null, ...books]}
                getOptionLabel={(option) => {
                  if (!option) return 'Новая книга'
                  return `${option.title} (${option.cipher})`
                }}
                isOptionEqualToValue={(option, value) => {
                  if (!option && !value) return true
                  if (!option || !value) return false
                  return option.book_id === value.book_id
                }}
                value={books.find((b) => b.book_id === field.value) || null}
                onChange={(_: React.SyntheticEvent, newValue: Book | null) => {
                  field.onChange(newValue?.book_id ?? null)
                }}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    label="Существующая книга (оставьте пустым для новой)"
                    margin="normal"
                    placeholder="Начните вводить название для поиска"
                  />
                )}
                filterOptions={(options, params) => {
                  if (!params.inputValue) return options
                  const filtered = options.filter((option) => {
                    if (!option) return true
                    const searchValue = params.inputValue.toLowerCase()
                    return (
                      option.title.toLowerCase().includes(searchValue) ||
                      option.cipher.toLowerCase().includes(searchValue)
                    )
                  })
                  return filtered
                }}
              />
            )}
          />

          {isNewBook && (
            <>
              <Divider sx={{ my: 2 }}>
                <Typography variant="subtitle2">Данные новой книги</Typography>
              </Divider>
              <Controller
                name="title"
                control={control}
                rules={{ 
                  required: isNewBook ? 'Название обязательно для новой книги' : false 
                }}
                render={({ field, fieldState: { error } }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Название*"
                    margin="normal"
                    error={!!error}
                    helperText={error?.message}
                  />
                )}
              />
              <Controller
                name="cipher"
                control={control}
                rules={{ 
                  required: isNewBook ? 'Шифр обязателен для новой книги' : false 
                }}
                render={({ field, fieldState: { error } }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Шифр*"
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
                      onChange={(e) => field.onChange(e.target.value === '' ? null : Number(e.target.value))}
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
                    value={field.value ?? ''}
                    onChange={(e) => field.onChange(e.target.value === '' ? null : Number(e.target.value))}
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
                      onChange={(e) => field.onChange(e.target.value === '' ? null : Number(e.target.value))}
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
            </>
          )}

          <Divider sx={{ my: 2 }}>
            <Typography variant="subtitle2">Данные экземпляра</Typography>
          </Divider>

          <Controller
            name="hall"
            control={control}
            rules={{ required: 'Зал обязателен', min: { value: 1, message: 'Выберите зал' } }}
            render={({ field, fieldState: { error } }) => (
              <FormControl fullWidth margin="normal" error={!!error}>
                <InputLabel>Зал*</InputLabel>
                <Select 
                  {...field} 
                  value={field.value ?? ''} 
                  label="Зал*"
                  onChange={(e) => field.onChange(e.target.value ? Number(e.target.value) : null)}
                >
                  <MenuItem value="">Выберите зал</MenuItem>
                  {halls.map((h) => (
                    <MenuItem key={h.hall_id} value={h.hall_id}>
                      {h.name}
                    </MenuItem>
                  ))}
                </Select>
                {error && <Typography variant="caption" color="error" sx={{ ml: 2, mt: 0.5, display: 'block' }}>{error.message}</Typography>}
              </FormControl>
            )}
          />
          <Controller
            name="inventory_number"
            control={control}
            rules={{ required: true }}
            render={({ field, fieldState: { error } }) => (
              <TextField
                {...field}
                fullWidth
                label="Инвентарный номер*"
                margin="normal"
                error={!!error}
                helperText={error?.message}
              />
            )}
          />

          <Button type="submit" variant="contained" fullWidth sx={{ mt: 3 }}>
            Принять книгу в фонд
          </Button>
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


