<template>
  <div class="books-view">
    <v-row class="mb-4">
      <v-col cols="12" class="d-flex justify-space-between align-center flex-wrap">
        <h1 class="page-title">
          <v-icon class="mr-2">mdi-book-open-page-variant</v-icon>
          Книги
        </h1>
        <v-btn color="primary" @click="openDialog()">
          <v-icon left>mdi-plus</v-icon>
          Добавить книгу
        </v-btn>
      </v-col>
    </v-row>

    <v-card>
      <v-card-title class="d-flex flex-wrap gap-4">
        <v-text-field
          v-model="search"
          prepend-inner-icon="mdi-magnify"
          label="Поиск"
          single-line
          hide-details
          density="compact"
          style="max-width: 300px"
        ></v-text-field>

        <v-select
          v-model="genreFilter"
          :items="genreOptions"
          label="Жанр"
          clearable
          hide-details
          density="compact"
          style="max-width: 200px"
        ></v-select>

        <v-checkbox
          v-model="illustrationsFilter"
          label="С иллюстрациями"
          hide-details
          density="compact"
        ></v-checkbox>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="filteredBooks"
        :search="search"
        :loading="loading"
        :items-per-page="10"
        class="elevation-0"
      >
        <template v-slot:item.has_illustrations="{ item }">
          <v-icon :icon="item.has_illustrations ? 'mdi-check-circle' : 'mdi-close-circle'" 
                  :color="item.has_illustrations ? 'success' : 'grey'"></v-icon>
        </template>

        <template v-slot:item.cover_price="{ item }">
          {{ formatPrice(item.cover_price) }}
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn icon="mdi-eye" size="small" variant="text" :to="{ name: 'book-detail', params: { id: item.id } }"></v-btn>
          <v-btn icon="mdi-pencil" size="small" variant="text" @click="openDialog(item)"></v-btn>
          <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="confirmDelete(item)"></v-btn>
        </template>

        <template v-slot:no-data>
          <div class="text-center pa-4">
            <v-icon size="48" color="grey">mdi-book-off</v-icon>
            <p class="mt-2 text-medium-emphasis">Книги не найдены</p>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- Create/Edit Dialog -->
    <v-dialog v-model="dialog" max-width="800" persistent>
      <v-card>
        <v-card-title class="d-flex align-center">
          <v-icon class="mr-2">{{ editingItem ? 'mdi-pencil' : 'mdi-plus' }}</v-icon>
          {{ editingItem ? 'Редактировать книгу' : 'Новая книга' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="formValid">
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="formData.title"
                  label="Название"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.isbn"
                  label="ISBN"
                  :rules="[rules.required, rules.isbn]"
                  counter="13"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model.number="formData.pages"
                  label="Количество страниц"
                  type="number"
                  :rules="[rules.required, rules.positive]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model.number="formData.cover_price"
                  label="Цена"
                  type="number"
                  step="0.01"
                  prefix="₽"
                  :rules="[rules.required, rules.positive]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.genre"
                  label="Жанр"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.publication_date"
                  label="Дата публикации"
                  type="date"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.language"
                  :items="languageOptions"
                  label="Язык"
                ></v-select>
              </v-col>
              <v-col cols="12" md="6">
                <v-checkbox
                  v-model="formData.has_illustrations"
                  label="Наличие иллюстраций"
                ></v-checkbox>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="formData.description"
                  label="Описание"
                  rows="3"
                ></v-textarea>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" :loading="saving" :disabled="!formValid" @click="saveItem">
            {{ editingItem ? 'Сохранить' : 'Создать' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить книгу 
          <strong>{{ itemToDelete?.title }}</strong>?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="deleteDialog = false">Отмена</v-btn>
          <v-btn color="error" :loading="deleting" @click="deleteItem">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, inject } from 'vue'
import { booksApi } from '@/services/api'

const showSnackbar = inject('showSnackbar')

const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)
const books = ref([])
const search = ref('')
const genreFilter = ref(null)
const illustrationsFilter = ref(false)

const dialog = ref(false)
const deleteDialog = ref(false)
const form = ref(null)
const formValid = ref(false)
const editingItem = ref(null)
const itemToDelete = ref(null)

const headers = [
  { title: 'ID', key: 'id', width: '80px' },
  { title: 'Название', key: 'title' },
  { title: 'ISBN', key: 'isbn', width: '150px' },
  { title: 'Авторы', key: 'authors_display' },
  { title: 'Страниц', key: 'pages', width: '100px' },
  { title: 'Цена', key: 'cover_price', width: '100px' },
  { title: 'Илл.', key: 'has_illustrations', width: '80px' },
  { title: 'Действия', key: 'actions', sortable: false, width: '140px' }
]

const genreOptions = ['Роман', 'Детектив', 'Фантастика', 'Научная литература', 'Биография', 'Учебник', 'Поэзия']
const languageOptions = [
  { title: 'Русский', value: 'RU' },
  { title: 'Английский', value: 'EN' },
  { title: 'Немецкий', value: 'DE' },
  { title: 'Французский', value: 'FR' }
]

const formData = reactive({
  title: '',
  isbn: '',
  pages: null,
  has_illustrations: false,
  publication_date: '',
  cover_price: null,
  description: '',
  genre: '',
  language: 'RU'
})

const rules = {
  required: (v) => !!v || v === 0 || 'Обязательное поле',
  positive: (v) => v > 0 || 'Должно быть больше 0',
  isbn: (v) => /^\d{13}$/.test(v) || 'ISBN должен содержать 13 цифр'
}

const filteredBooks = computed(() => {
  let result = books.value
  if (genreFilter.value) {
    result = result.filter(b => b.genre === genreFilter.value)
  }
  if (illustrationsFilter.value) {
    result = result.filter(b => b.has_illustrations)
  }
  return result
})

const formatPrice = (price) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(price)
}

const fetchBooks = async () => {
  loading.value = true
  try {
    const response = await booksApi.getAll()
    books.value = response.data.results || response.data
  } catch (error) {
    showSnackbar('Ошибка загрузки данных', 'error')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const openDialog = (item = null) => {
  editingItem.value = item
  if (item) {
    Object.assign(formData, {
      title: item.title,
      isbn: item.isbn,
      pages: item.pages,
      has_illustrations: item.has_illustrations,
      publication_date: item.publication_date || '',
      cover_price: item.cover_price,
      description: item.description || '',
      genre: item.genre || '',
      language: item.language || 'RU'
    })
  } else {
    Object.assign(formData, {
      title: '',
      isbn: '',
      pages: null,
      has_illustrations: false,
      publication_date: '',
      cover_price: null,
      description: '',
      genre: '',
      language: 'RU'
    })
  }
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
  editingItem.value = null
  form.value?.reset()
}

const saveItem = async () => {
  const { valid } = await form.value.validate()
  if (!valid) return

  saving.value = true
  try {
    const data = { ...formData }
    if (!data.publication_date) delete data.publication_date

    if (editingItem.value) {
      await booksApi.update(editingItem.value.id, data)
      showSnackbar('Книга обновлена', 'success')
    } else {
      await booksApi.create(data)
      showSnackbar('Книга создана', 'success')
    }
    closeDialog()
    fetchBooks()
  } catch (error) {
    const errorMsg = error.response?.data?.detail || 
                     Object.values(error.response?.data || {}).flat().join('. ') ||
                     'Ошибка сохранения'
    showSnackbar(errorMsg, 'error')
  } finally {
    saving.value = false
  }
}

const confirmDelete = (item) => {
  itemToDelete.value = item
  deleteDialog.value = true
}

const deleteItem = async () => {
  deleting.value = true
  try {
    await booksApi.delete(itemToDelete.value.id)
    showSnackbar('Книга удалена', 'success')
    deleteDialog.value = false
    fetchBooks()
  } catch (error) {
    showSnackbar('Ошибка удаления', 'error')
  } finally {
    deleting.value = false
  }
}

onMounted(fetchBooks)
</script>

<style scoped>
.books-view {
  max-width: 1400px;
  margin: 0 auto;
}

.page-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
  font-weight: 600;
  color: rgb(var(--v-theme-on-background));
}
</style>

