<template>
  <div class="admin-issue-book">
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <h1 class="text-h4 mb-4">📘 Выдача книги</h1>
        </v-col>
      </v-row>

      <!-- Только для админов -->
      <v-row v-if="!isAdmin">
        <v-col cols="12">
          <v-alert type="warning" variant="tonal">
            Эта страница доступна только администраторам.
          </v-alert>
        </v-col>
      </v-row>

      <template v-else>
        <v-row>
          <!-- ===== КОЛОНКА 1: ПОИСК ЧИТАТЕЛЯ ===== -->
          <v-col cols="12" md="6">
            <v-card class="pa-4">
              <v-card-title class="text-h5 pa-0 mb-4">
                <v-icon color="primary" size="28" class="mr-2">mdi-account</v-icon>
                Читатель
              </v-card-title>

              <!-- Поле поиска -->
              <v-text-field
                v-model="searchReaderQuery"
                label="Поиск читателя"
                placeholder="Введите ФИО или номер билета"
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                density="comfortable"
                clearable
                @input="searchReaderDebounced"
                @keyup.enter="searchReader"
                :loading="searchingReader"
              ></v-text-field>

              <!-- Результаты поиска -->
              <v-card v-if="foundReaders.length > 0" variant="outlined" class="mt-2">
                <v-list>
                  <v-list-subheader>Найденные читатели ({{ foundReaders.length }})</v-list-subheader>
                  <v-list-item
                    v-for="reader in foundReaders"
                    :key="reader.reader_id"
                    @click="selectReader(reader)"
                    :active="selectedReader?.reader_id === reader.reader_id"
                  >
                    <template v-slot:prepend>
                      <v-avatar :color="getAvatarColor(reader.full_name)" size="40">
                        <span class="text-white">{{ reader.full_name.charAt(0) }}</span>
                      </v-avatar>
                    </template>
                    <v-list-item-title>{{ reader.full_name }}</v-list-item-title>
                    <v-list-item-subtitle>
                      Билет: {{ reader.library_card_id }}
                    </v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card>

              <!-- Сообщение если ничего не найдено -->
              <v-card v-else-if="searchReaderQuery && !searchingReader" variant="outlined" class="mt-2">
                <v-card-text class="text-center text-grey">
                  <v-icon size="48" color="grey-lighten-1">mdi-account-off</v-icon>
                  <p class="mt-2">Читатели не найдены</p>
                </v-card-text>
              </v-card>

              <!-- Выбранный читатель -->
              <v-card v-if="selectedReader" color="primary" variant="tonal" class="mt-4">
                <v-card-text class="d-flex align-center">
                  <v-avatar :color="getAvatarColor(selectedReader.full_name)" size="48" class="mr-3">
                    <span class="text-white">{{ selectedReader.full_name.charAt(0) }}</span>
                  </v-avatar>
                  <div>
                    <div class="text-h6">{{ selectedReader.full_name }}</div>
                    <div class="text-caption">Билет: {{ selectedReader.library_card_id }}</div>
                  </div>
                  <v-spacer></v-spacer>
                  <v-btn icon="mdi-close" variant="text" @click="deselectReader"></v-btn>
                </v-card-text>
              </v-card>
            </v-card>
          </v-col>

          <!-- ===== КОЛОНКА 2: ПОИСК КНИГИ ===== -->
          <v-col cols="12" md="6">
            <v-card class="pa-4">
              <v-card-title class="text-h5 pa-0 mb-4">
                <v-icon color="primary" size="28" class="mr-2">mdi-book</v-icon>
                Книга
              </v-card-title>

              <v-text-field
                v-model="searchBookQuery"
                label="Поиск книги"
                placeholder="Введите название или инв. номер"
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                density="comfortable"
                clearable
                @input="searchBookDebounced"
                @keyup.enter="searchBook"
                :loading="searchingBook"
              ></v-text-field>

              <!-- Результаты поиска книги -->
              <v-card v-if="foundBooks.length > 0" variant="outlined" class="mt-2">
                <v-list>
                  <v-list-subheader>Найденные книги ({{ foundBooks.length }})</v-list-subheader>
                  <v-list-item
                    v-for="book in foundBooks"
                    :key="book.book_id"
                    @click="selectBook(book)"
                    :active="selectedBook?.book_id === book.book_id"
                  >
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-book</v-icon>
                    </template>
                    <v-list-item-title>{{ book.title }}</v-list-item-title>
                    <v-list-item-subtitle>
                      Инв. №: {{ book.inventory_code }} | Доступно: {{ book.available_copies }} экз.
                    </v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card>

              <!-- Сообщение если ничего не найдено -->
              <v-card v-else-if="searchBookQuery && !searchingBook" variant="outlined" class="mt-2">
                <v-card-text class="text-center text-grey">
                  <v-icon size="48" color="grey-lighten-1">mdi-book-off</v-icon>
                  <p class="mt-2">Книги не найдены</p>
                </v-card-text>
              </v-card>

              <!-- Выбранная книга -->
              <v-card v-if="selectedBook" color="primary" variant="tonal" class="mt-4">
                <v-card-text class="d-flex align-center">
                  <v-icon color="primary" size="48" class="mr-3">mdi-book</v-icon>
                  <div>
                    <div class="text-h6">{{ selectedBook.title }}</div>
                    <div class="text-caption">Инв. №: {{ selectedBook.inventory_code }}</div>
                  </div>
                  <v-spacer></v-spacer>
                  <v-btn icon="mdi-close" variant="text" @click="deselectBook"></v-btn>
                </v-card-text>
              </v-card>
            </v-card>
          </v-col>

          <!-- ===== КОЛОНКА 3: ПАРАМЕТРЫ ВЫДАЧИ ===== -->
          <v-col cols="12">
            <v-card class="pa-4" :disabled="!canIssue">
              <v-card-title class="text-h5 pa-0 mb-4">
                <v-icon color="primary" size="28" class="mr-2">mdi-book-plus</v-icon>
                Параметры выдачи
              </v-card-title>

              <v-row>
                <v-col cols="12" md="6">
                  <v-select
                    v-model="selectedCopyId"
                    :items="availableCopies"
                    item-title="label"
                    item-value="copy_book_id"
                    label="Экземпляр книги *"
                    variant="outlined"
                    density="comfortable"
                    :disabled="!selectedBook"
                  ></v-select>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="dueDate"
                    label="Срок возврата *"
                    type="date"
                    variant="outlined"
                    density="comfortable"
                    :min="tomorrow"
                  ></v-text-field>
                </v-col>
              </v-row>

              <v-alert
                v-if="issueError"
                type="error"
                variant="tonal"
                class="mt-4"
                closable
                @click:close="issueError = ''"
              >
                <strong>❌ {{ issueError }}</strong>
              </v-alert>

              <v-alert
                v-if="issueSuccess"
                type="success"
                variant="tonal"
                class="mt-4"
              >
                ✅ Книга успешно выдана!
              </v-alert>

              <v-card-actions class="pa-0 mt-4">
                <v-spacer></v-spacer>
                <v-btn
                  color="success"
                  size="large"
                  :loading="issuing"
                  :disabled="!canIssue || !selectedCopyId || !dueDate"
                  @click="issueBook"
                >
                  <v-icon left>mdi-book-check</v-icon>
                  Выдать книгу
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </template>
    </v-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import apiClient from '../../api/client'

const auth = useAuthStore()
const isAdmin = computed(() => auth.isAdmin)

// Состояние
const searchReaderQuery = ref('')
const searchBookQuery = ref('')
const searchingReader = ref(false)
const searchingBook = ref(false)
const foundReaders = ref([])
const foundBooks = ref([])
const selectedReader = ref(null)
const selectedBook = ref(null)
const availableCopies = ref([])
const selectedCopyId = ref(null)
const dueDate = ref('')
const issuing = ref(false)
const issueError = ref('')
const issueSuccess = ref(false)

// Debounce таймеры
let readerSearchTimeout = null
let bookSearchTimeout = null

// Вычисляемые свойства
const tomorrow = computed(() => {
  const date = new Date()
  date.setDate(date.getDate() + 1)
  return date.toISOString().split('T')[0]
})

const canIssue = computed(() => selectedReader.value && selectedBook.value)

// Цвета для аватарок
const getAvatarColor = (name) => {
  const colors = ['primary', 'success', 'info', 'warning', 'error', 'purple', 'pink']
  const index = name.charCodeAt(0) % colors.length
  return colors[index]
}

// ===== ПОИСК ЧИТАТЕЛЯ =====
const searchReader = async () => {
  const query = searchReaderQuery.value?.trim() || ''

  if (!query) {
    foundReaders.value = []
    return
  }

  searchingReader.value = true
  try {
    const response = await apiClient.get('readers/')
    const allReaders = response.data
    const lowerQuery = query.toLowerCase()

    foundReaders.value = allReaders.filter(reader =>
      reader.full_name.toLowerCase().includes(lowerQuery) ||
      reader.library_card_id.toLowerCase().includes(lowerQuery)
    )
  } catch (error) {
    console.error('Ошибка поиска читателей:', error)
  } finally {
    searchingReader.value = false
  }
}

const searchReaderDebounced = () => {
  clearTimeout(readerSearchTimeout)
  readerSearchTimeout = setTimeout(() => {
    searchReader()
  }, 300)
}

const selectReader = (reader) => {
  selectedReader.value = reader
  foundReaders.value = []
  searchReaderQuery.value = ''
}

const deselectReader = () => {
  selectedReader.value = null
}

// ===== ПОИСК КНИГИ =====
const searchBook = async () => {
  const query = searchBookQuery.value?.trim() || ''

  if (!query) {
    foundBooks.value = []
    return
  }

  searchingBook.value = true
  try {
    const response = await apiClient.get('books/with-copies/')
    const allBooks = response.data
    const lowerQuery = query.toLowerCase()

    foundBooks.value = allBooks.filter(book =>
      book.title.toLowerCase().includes(lowerQuery) ||
      book.inventory_code.toLowerCase().includes(lowerQuery)
    )
  } catch (error) {
    console.error('Ошибка поиска книг:', error)
  } finally {
    searchingBook.value = false
  }
}

const searchBookDebounced = () => {
  clearTimeout(bookSearchTimeout)
  bookSearchTimeout = setTimeout(() => {
    searchBook()
  }, 300)
}

const selectBook = async (book) => {
  selectedBook.value = book
  foundBooks.value = []
  searchBookQuery.value = ''
  selectedCopyId.value = null
  await loadAvailableCopies(book.book_id)
}

const deselectBook = () => {
  selectedBook.value = null
  availableCopies.value = []
  selectedCopyId.value = null
}

// ===== ЗАГРУЗКА ЭКЗЕМПЛЯРОВ =====
const loadAvailableCopies = async (bookId) => {
  try {
    const response = await apiClient.get('copies/')
    const copies = response.data.filter(copy =>
      copy.book_id === bookId && copy.availability_status === 'available'
    )

    availableCopies.value = copies.map(copy => ({
      copy_book_id: copy.copy_book_id,
      label: `Экз. №${copy.copy_book_id} — ${copy.copy_condition || 'хорошее'}`
    }))
  } catch (error) {
    console.error('Ошибка загрузки экземпляров:', error)
  }
}

// ===== ВЫДАЧА КНИГИ =====
const issueBook = async () => {
  if (!selectedCopyId.value || !dueDate.value) return

  issuing.value = true
  issueError.value = ''
  issueSuccess.value = false

  try {
    await apiClient.post('loans/create/', {
      copy_book_id: selectedCopyId.value,
      reader_id: selectedReader.value.reader_id,
      issued_at: new Date().toISOString().split('T')[0],
      due_date: dueDate.value,
      returned_at: null
    })

    issueSuccess.value = true

    setTimeout(() => {
      selectedReader.value = null
      selectedBook.value = null
      selectedCopyId.value = null
      availableCopies.value = []
      foundReaders.value = []
      foundBooks.value = []
      searchReaderQuery.value = ''
      searchBookQuery.value = ''
      issueSuccess.value = false
    }, 2000)

  } catch (error) {
    console.error('Ошибка выдачи:', error)
    issueError.value = error.response?.data?.error || 'Не удалось выдать книгу'
  } finally {
    issuing.value = false
  }
}

// Инициализация
onMounted(() => {
  const date = new Date()
  date.setDate(date.getDate() + 14)
  dueDate.value = date.toISOString().split('T')[0]
})
</script>