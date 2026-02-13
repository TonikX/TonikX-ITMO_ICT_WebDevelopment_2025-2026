<template>
  <div class="admin-book-add">
    <v-container class="book-container">
      <v-row justify="center">
        <v-col cols="12" md="10" lg="8">
          <v-card>
            <v-card-title class="text-h5">
              <v-icon left size="28" color="primary">mdi-book-plus</v-icon>
              Добавление новой книги
            </v-card-title>

            <v-card-text>
              <v-form ref="formRef" v-model="valid">
                <v-row>
                  <v-col cols="12">
                    <h4 class="text-subtitle-1 mb-2">📖 Основная информация</h4>
                  </v-col>

                  <!-- Название книги -->
                  <v-col cols="12">
                    <v-text-field
                      v-model="formData.title"
                      :rules="[v => !!v || 'Название обязательно']"
                      label="Название книги *"
                      placeholder="Собачье сердце"
                      required
                      density="comfortable"
                      variant="outlined"
                    ></v-text-field>
                  </v-col>

                  <!-- Автор (выпадающий список) -->
                  <v-col cols="12" md="8">
                    <v-select
                      v-model="formData.author_id"
                      :items="authors"
                      :rules="[v => !!v || 'Автор обязателен']"
                      item-title="full_name"
                      item-value="author_id"
                      label="Автор *"
                      placeholder="Выберите автора"
                      required
                      density="comfortable"
                      variant="outlined"
                      clearable
                      return-object="false"
                    ></v-select>
                  </v-col>

                  <!-- Кнопка добавления автора -->
                  <v-col cols="12" md="4" class="d-flex align-center">
                    <v-btn
                      color="info"
                      variant="outlined"
                      prepend-icon="mdi-account-plus"
                      @click="openAddAuthorDialog"
                      block
                    >
                      Новый автор
                    </v-btn>
                  </v-col>

                  <!-- Издательство -->
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="formData.publisher"
                      :rules="[v => !!v || 'Издательство обязательно']"
                      label="Издательство *"
                      placeholder="Недра"
                      required
                      density="comfortable"
                      variant="outlined"
                    ></v-text-field>
                  </v-col>

                  <!-- Год издания -->
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="formData.publication_year"
                      :rules="[
                        v => !!v || 'Год издания обязателен',
                        v => /^\d{4}$/.test(v) || 'Введите 4 цифры'
                      ]"
                      label="Год издания *"
                      placeholder="1925"
                      required
                      density="comfortable"
                      variant="outlined"
                      type="number"
                      min="1000"
                      max="2100"
                    ></v-text-field>
                  </v-col>

                  <!-- Раздел -->
                  <v-col cols="12" md="6">
                    <v-select
                      v-model="formData.section"
                      :items="sections"
                      :rules="[v => !!v || 'Раздел обязателен']"
                      label="Раздел *"
                      placeholder="Выберите раздел"
                      required
                      density="comfortable"
                      variant="outlined"
                    ></v-select>
                  </v-col>

                  <!-- Инвентарный номер -->
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="formData.inventory_code"
                      :rules="[v => !!v || 'Инвентарный номер обязателен']"
                      label="Инвентарный номер *"
                      placeholder="RUS-008"
                      required
                      density="comfortable"
                      variant="outlined"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12">
                    <v-divider class="my-4"></v-divider>
                    <h4 class="text-subtitle-1 mb-2">📦 Экземпляры книги</h4>
                  </v-col>

                  <!-- Количество экземпляров -->
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="formData.copy_count"
                      :rules="[
                        v => !!v || 'Количество обязательно',
                        v => parseInt(v) > 0 || 'Минимум 1'
                      ]"
                      label="Количество экземпляров *"
                      placeholder="1"
                      required
                      density="comfortable"
                      variant="outlined"
                      type="number"
                      min="1"
                    ></v-text-field>
                  </v-col>

                  <!-- Зал -->
                  <v-col cols="12" md="6">
                    <v-select
                      v-model="formData.hall_id"
                      :items="halls"
                      :rules="[v => !!v || 'Зал обязателен']"
                      item-title="name"
                      item-value="hall_id"
                      label="Зал *"
                      placeholder="Выберите зал"
                      required
                      density="comfortable"
                      variant="outlined"
                    ></v-select>
                  </v-col>

                  <!-- Состояние -->
                  <v-col cols="12" md="6">
                    <v-select
                      v-model="formData.copy_condition"
                      :items="conditions"
                      item-title="title"
                      item-value="value"
                      label="Состояние"
                      density="comfortable"
                      variant="outlined"
                      default="good"
                    ></v-select>
                  </v-col>
                </v-row>
              </v-form>

              <v-alert
                v-if="error"
                type="error"
                variant="tonal"
                class="mt-4"
                closable
                @click:close="error = ''"
              >
                {{ error }}
              </v-alert>

              <v-alert
                v-if="success"
                type="success"
                variant="tonal"
                class="mt-4"
              >
                ✅ Книга успешно добавлена!
                <div class="mt-2">
                  <strong>Название:</strong> {{ newBook?.title }}<br>
                  <strong>Инв. номер:</strong> {{ newBook?.inventory_code }}
                </div>
              </v-alert>
            </v-card-text>

            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn
                color="grey-darken-1"
                variant="text"
                @click="$router.push('/admin/books')"
              >
                Отмена
              </v-btn>
              <v-btn
                color="primary"
                :loading="loading"
                @click="addBook"
              >
                Добавить книгу
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Диалог добавления нового автора -->
    <v-dialog v-model="authorDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">
          <v-icon left color="primary">mdi-account-plus</v-icon>
          Добавление нового автора
        </v-card-title>
        <v-card-text>
          <v-form ref="authorFormRef" v-model="authorValid">
            <v-text-field
              v-model="newAuthor.full_name"
              :rules="[v => !!v || 'Имя автора обязательно']"
              label="ФИО автора *"
              placeholder="Булгаков Михаил Афанасьевич"
              density="comfortable"
              variant="outlined"
              class="mt-2"
            ></v-text-field>

            <v-text-field
              v-model="newAuthor.birth_date"
              label="Дата рождения"
              placeholder="1891-05-15"
              density="comfortable"
              variant="outlined"
              type="date"
              hint="Формат: ГГГГ-ММ-ДД"
              persistent-hint
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="authorDialog = false">
            Отмена
          </v-btn>
          <v-btn color="primary" @click="addAuthor" :loading="authorLoading">
            Добавить автора
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../../api/client'

const router = useRouter()
const formRef = ref(null)
const authorFormRef = ref(null)
const valid = ref(false)
const authorValid = ref(false)
const loading = ref(false)
const authorLoading = ref(false)
const error = ref('')
const success = ref(false)
const newBook = ref(null)

// Данные для выпадающих списков
const authors = ref([])
const halls = ref([])
const authorDialog = ref(false)

// Данные формы
const formData = reactive({
  title: '',
  author_id: null,
  publisher: '',
  publication_year: '',
  section: '',
  inventory_code: '',
  copy_count: 1,
  hall_id: null,
  copy_condition: 'good'
})

// Новый автор
const newAuthor = reactive({
  full_name: '',
  birth_date: ''
})

// Разделы библиотеки
const sections = [
  'Русская классика',
  'Зарубежная классика',
  'Современная проза',
  'Поэзия',
  'Драматургия',
  'Научная литература',
  'Учебная литература',
  'Детская литература',
  'Фантастика',
  'Детектив',
  'История',
  'Философия',
  'Искусство',
  'Тестирование'
]

// Состояния книг
const conditions = [
  { title: 'Отличное', value: 'excellent' },
  { title: 'Хорошее', value: 'good' },
  { title: 'Удовлетворительное', value: 'fair' },
  { title: 'Плохое', value: 'poor' },
  { title: 'Поврежден', value: 'damaged' }
]

// Загрузка авторов
const loadAuthors = async () => {
  try {
    const response = await apiClient.get('authors/')
    authors.value = response.data
    console.log('Авторы загружены:', authors.value)
  } catch (error) {
    console.error('Ошибка загрузки авторов:', error)
  }
}

// Загрузка залов
const loadHalls = async () => {
  try {
    const response = await apiClient.get('halls/')
    halls.value = response.data
    console.log('Залы загружены:', halls.value)
  } catch (error) {
    console.error('Ошибка загрузки залов:', error)
  }
}

// Открыть диалог добавления автора
const openAddAuthorDialog = () => {
  newAuthor.full_name = ''
  newAuthor.birth_date = ''
  authorDialog.value = true
}

// Добавить нового автора
const addAuthor = async () => {
  if (!authorFormRef.value?.validate()) return

  authorLoading.value = true
  try {
    // Отправляем данные в формате API
    const authorData = {
      full_name: newAuthor.full_name,
      birth_date: newAuthor.birth_date || null
    }

    console.log('Отправка автора:', authorData)
    const response = await apiClient.post('authors/create/', authorData)
    console.log('Автор создан:', response.data)

    // Добавляем нового автора в список
    authors.value.push(response.data)
    // Выбираем созданного автора
    formData.author_id = response.data.author_id

    authorDialog.value = false

  } catch (error) {
    console.error('Ошибка добавления автора:', error.response?.data || error)
    alert('Не удалось добавить автора: ' + (error.response?.data?.error || 'Ошибка сервера'))
  } finally {
    authorLoading.value = false
  }
}

// Добавить книгу
const addBook = async () => {
  if (!formRef.value?.validate()) return

  loading.value = true
  error.value = ''
  success.value = false

  try {
    // 1. Создаем книгу
    const bookData = {
      title: formData.title,
      publisher: formData.publisher,
      publication_year: parseInt(formData.publication_year),
      section: formData.section,
      inventory_code: formData.inventory_code,
      is_in_catalog: true
    }

    console.log('Создание книги:', bookData)
    const bookResponse = await apiClient.post('books/add/', bookData)
    const book = bookResponse.data
    console.log('Книга создана:', book)

    // 2. Привязываем автора
    const bookAuthorData = {
      book_id: book.book_id,
      author_id: formData.author_id,
      author_order: 1
    }

    console.log('Привязка автора:', bookAuthorData)
    await apiClient.post('book-authors/create/', bookAuthorData)
    console.log('Автор привязан')

    // 3. Создаем экземпляры книги
    for (let i = 0; i < parseInt(formData.copy_count); i++) {
      const copyData = {
        book_id: book.book_id,
        hall_id: formData.hall_id,
        availability_status: 'available',
        copy_condition: formData.copy_condition || 'good'
      }

      console.log(`Создание экземпляра ${i + 1}:`, copyData)
      await apiClient.post('copies/create/', copyData)
    }
    console.log('Экземпляры созданы')

    newBook.value = book
    success.value = true

    // Сброс формы
    formData.title = ''
    formData.author_id = null
    formData.publisher = ''
    formData.publication_year = ''
    formData.section = ''
    formData.inventory_code = ''
    formData.copy_count = 1
    formData.hall_id = null
    formData.copy_condition = 'good'

    setTimeout(() => {
      router.push('/admin/books')
    }, 3000)

  } catch (error) {
    console.error('Ошибка добавления книги:', error.response?.data || error)
    error.value = error.response?.data?.error ||
                  error.response?.data?.message ||
                  'Ошибка при добавлении книги'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadAuthors()
  loadHalls()
})
</script>

<style scoped>
.admin-book-add {
  width: 100%;
  min-height: 100%;
}

.book-container {
  max-width: 1200px !important;
  padding: 20px !important;
}

.v-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
}

.v-card-title {
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
  border-bottom: 1px solid #ddd;
}

@media (max-width: 768px) {
  .book-container {
    padding: 10px !important;
  }
}
</style>