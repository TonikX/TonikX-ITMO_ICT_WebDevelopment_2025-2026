<template>
  <div class="book-detail-view">
    <v-btn class="mb-4" variant="text" :to="{ name: 'books' }">
      <v-icon left>mdi-arrow-left</v-icon>
      Назад к списку
    </v-btn>

    <v-skeleton-loader v-if="loading" type="article, actions"></v-skeleton-loader>

    <template v-else-if="book">
      <v-row>
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title class="d-flex align-center">
              <v-icon class="mr-2">mdi-book-open-page-variant</v-icon>
              {{ book.title }}
            </v-card-title>
            <v-card-subtitle>ISBN: {{ book.isbn }}</v-card-subtitle>

            <v-card-text>
              <v-row>
                <v-col cols="6" md="3">
                  <div class="text-caption text-medium-emphasis">Страниц</div>
                  <div class="text-h6">{{ book.pages }}</div>
                </v-col>
                <v-col cols="6" md="3">
                  <div class="text-caption text-medium-emphasis">Цена</div>
                  <div class="text-h6">{{ formatPrice(book.cover_price) }}</div>
                </v-col>
                <v-col cols="6" md="3">
                  <div class="text-caption text-medium-emphasis">Жанр</div>
                  <div class="text-h6">{{ book.genre || '—' }}</div>
                </v-col>
                <v-col cols="6" md="3">
                  <div class="text-caption text-medium-emphasis">Язык</div>
                  <div class="text-h6">{{ book.language }}</div>
                </v-col>
              </v-row>

              <v-divider class="my-4"></v-divider>

              <div class="mb-4">
                <div class="text-caption text-medium-emphasis mb-1">Дата публикации</div>
                <div>{{ book.publication_date || 'Не указана' }}</div>
              </div>

              <div class="mb-4">
                <div class="text-caption text-medium-emphasis mb-1">Иллюстрации</div>
                <v-chip :color="book.has_illustrations ? 'success' : 'grey'" size="small">
                  {{ book.has_illustrations ? 'Есть' : 'Нет' }}
                </v-chip>
              </div>

              <div v-if="book.description">
                <div class="text-caption text-medium-emphasis mb-1">Описание</div>
                <p>{{ book.description }}</p>
              </div>
            </v-card-text>
          </v-card>

          <!-- Contract Info -->
          <v-card v-if="book.contract" class="mt-4">
            <v-card-title class="d-flex align-center">
              <v-icon class="mr-2">mdi-file-document-edit</v-icon>
              Контракт
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="6" md="4">
                  <div class="text-caption text-medium-emphasis">Номер</div>
                  <div class="font-weight-medium">{{ book.contract.contract_number }}</div>
                </v-col>
                <v-col cols="6" md="4">
                  <div class="text-caption text-medium-emphasis">Статус</div>
                  <v-chip :color="getStatusColor(book.contract.status)" size="small">
                    {{ getStatusLabel(book.contract.status) }}
                  </v-chip>
                </v-col>
                <v-col cols="12" md="4">
                  <div class="text-caption text-medium-emphasis">Дата подписания</div>
                  <div>{{ book.contract.signed_date }}</div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="4">
          <!-- Authors -->
          <v-card class="mb-4">
            <v-card-title class="d-flex align-center justify-space-between">
              <span>
                <v-icon class="mr-2">mdi-feather</v-icon>
                Авторы
              </span>
              <v-btn size="small" color="primary" variant="tonal" @click="openAuthorDialog">
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </v-card-title>
            <v-card-text>
              <v-list v-if="book.authors?.length" density="compact">
                <v-list-item v-for="author in book.authors" :key="author.id">
                  <template v-slot:prepend>
                    <v-avatar color="primary" size="32">
                      <span class="text-body-2">{{ author.author_order }}</span>
                    </v-avatar>
                  </template>
                  <v-list-item-title>{{ author.author_name }}</v-list-item-title>
                  <v-list-item-subtitle>Гонорар: {{ author.royalty_percentage }}%</v-list-item-subtitle>
                  <template v-slot:append>
                    <v-btn icon="mdi-delete" size="x-small" variant="text" color="error" 
                           @click="deleteBookAuthor(author.id)"></v-btn>
                  </template>
                </v-list-item>
              </v-list>
              <p v-else class="text-medium-emphasis text-center">Авторы не назначены</p>
            </v-card-text>
          </v-card>

          <!-- Editors -->
          <v-card>
            <v-card-title class="d-flex align-center justify-space-between">
              <span>
                <v-icon class="mr-2">mdi-account-edit</v-icon>
                Редакторы
              </span>
              <v-btn size="small" color="primary" variant="tonal" @click="openEditorDialog">
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </v-card-title>
            <v-card-text>
              <v-list v-if="book.editors?.length" density="compact">
                <v-list-item v-for="editor in book.editors" :key="editor.id">
                  <template v-slot:prepend>
                    <v-avatar :color="editor.is_chief_editor ? 'secondary' : 'grey'" size="32">
                      <v-icon size="16">{{ editor.is_chief_editor ? 'mdi-star' : 'mdi-account' }}</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title>{{ editor.editor_name }}</v-list-item-title>
                  <v-list-item-subtitle v-if="editor.is_chief_editor">Ответственный редактор</v-list-item-subtitle>
                  <template v-slot:append>
                    <v-btn icon="mdi-delete" size="x-small" variant="text" color="error" 
                           @click="deleteBookEditor(editor.id)"></v-btn>
                  </template>
                </v-list-item>
              </v-list>
              <p v-else class="text-medium-emphasis text-center">Редакторы не назначены</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>

    <!-- Add Author Dialog -->
    <v-dialog v-model="authorDialog" max-width="500">
      <v-card>
        <v-card-title>Добавить автора</v-card-title>
        <v-card-text>
          <v-form ref="authorForm" v-model="authorFormValid">
            <v-select
              v-model="authorFormData.author"
              :items="availableAuthors"
              item-title="full_name"
              item-value="id"
              label="Автор"
              :rules="[rules.required]"
            ></v-select>
            <v-text-field
              v-model.number="authorFormData.author_order"
              label="Порядок на обложке"
              type="number"
              :rules="[rules.required, rules.positive]"
            ></v-text-field>
            <v-text-field
              v-model.number="authorFormData.royalty_percentage"
              label="Процент гонорара"
              type="number"
              step="0.01"
              suffix="%"
              :rules="[rules.required, rules.percentage]"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="authorDialog = false">Отмена</v-btn>
          <v-btn color="primary" :loading="saving" :disabled="!authorFormValid" @click="addAuthor">
            Добавить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Add Editor Dialog -->
    <v-dialog v-model="editorDialog" max-width="500">
      <v-card>
        <v-card-title>Добавить редактора</v-card-title>
        <v-card-text>
          <v-form ref="editorForm" v-model="editorFormValid">
            <v-select
              v-model="editorFormData.editor"
              :items="availableEditors"
              item-title="full_name"
              item-value="id"
              label="Редактор"
              :rules="[rules.required]"
            ></v-select>
            <v-checkbox
              v-model="editorFormData.is_chief_editor"
              label="Ответственный редактор"
            ></v-checkbox>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="editorDialog = false">Отмена</v-btn>
          <v-btn color="primary" :loading="saving" :disabled="!editorFormValid" @click="addEditor">
            Добавить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, inject } from 'vue'
import { useRoute } from 'vue-router'
import { booksApi, authorsApi, employeesApi, bookAuthorsApi, bookEditorsApi } from '@/services/api'

const route = useRoute()
const showSnackbar = inject('showSnackbar')

const loading = ref(false)
const saving = ref(false)
const book = ref(null)
const allAuthors = ref([])
const allEditors = ref([])

const authorDialog = ref(false)
const editorDialog = ref(false)
const authorForm = ref(null)
const editorForm = ref(null)
const authorFormValid = ref(false)
const editorFormValid = ref(false)

const authorFormData = reactive({
  author: null,
  author_order: 1,
  royalty_percentage: 50
})

const editorFormData = reactive({
  editor: null,
  is_chief_editor: false
})

const rules = {
  required: (v) => !!v || v === 0 || 'Обязательное поле',
  positive: (v) => v > 0 || 'Должно быть больше 0',
  percentage: (v) => (v >= 0 && v <= 100) || 'От 0 до 100'
}

const availableAuthors = ref([])
const availableEditors = ref([])

const getStatusColor = (status) => {
  const colors = { DRAFT: 'grey', ACTIVE: 'success', COMPLETED: 'info', TERMINATED: 'error' }
  return colors[status] || 'grey'
}

const getStatusLabel = (status) => {
  const labels = { DRAFT: 'Черновик', ACTIVE: 'Активный', COMPLETED: 'Завершён', TERMINATED: 'Расторгнут' }
  return labels[status] || status
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(price)
}

const fetchBook = async () => {
  loading.value = true
  try {
    const response = await booksApi.getOne(route.params.id)
    book.value = response.data
  } catch (error) {
    showSnackbar('Ошибка загрузки книги', 'error')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const fetchAuthors = async () => {
  try {
    const response = await authorsApi.getAll()
    allAuthors.value = response.data.results || response.data
  } catch (error) {
    console.error(error)
  }
}

const fetchEditors = async () => {
  try {
    const response = await employeesApi.getAll({ role: 'EDITOR' })
    allEditors.value = response.data.results || response.data
  } catch (error) {
    console.error(error)
  }
}

const openAuthorDialog = () => {
  const existingAuthorIds = book.value.authors?.map(a => a.author) || []
  availableAuthors.value = allAuthors.value.filter(a => !existingAuthorIds.includes(a.id))
  authorFormData.author = null
  authorFormData.author_order = (book.value.authors?.length || 0) + 1
  authorFormData.royalty_percentage = 50
  authorDialog.value = true
}

const openEditorDialog = () => {
  const existingEditorIds = book.value.editors?.map(e => e.editor) || []
  availableEditors.value = allEditors.value.filter(e => !existingEditorIds.includes(e.id))
  editorFormData.editor = null
  editorFormData.is_chief_editor = false
  editorDialog.value = true
}

const addAuthor = async () => {
  const { valid } = await authorForm.value.validate()
  if (!valid) return

  saving.value = true
  try {
    await bookAuthorsApi.create({
      book: book.value.id,
      author: authorFormData.author,
      author_order: authorFormData.author_order,
      royalty_percentage: authorFormData.royalty_percentage
    })
    showSnackbar('Автор добавлен', 'success')
    authorDialog.value = false
    fetchBook()
  } catch (error) {
    const errorMsg = error.response?.data?.detail || 
                     Object.values(error.response?.data || {}).flat().join('. ') ||
                     'Ошибка добавления'
    showSnackbar(errorMsg, 'error')
  } finally {
    saving.value = false
  }
}

const addEditor = async () => {
  const { valid } = await editorForm.value.validate()
  if (!valid) return

  saving.value = true
  try {
    await bookEditorsApi.create({
      book: book.value.id,
      editor: editorFormData.editor,
      is_chief_editor: editorFormData.is_chief_editor
    })
    showSnackbar('Редактор добавлен', 'success')
    editorDialog.value = false
    fetchBook()
  } catch (error) {
    const errorMsg = error.response?.data?.detail || 
                     Object.values(error.response?.data || {}).flat().join('. ') ||
                     'Ошибка добавления'
    showSnackbar(errorMsg, 'error')
  } finally {
    saving.value = false
  }
}

const deleteBookAuthor = async (id) => {
  try {
    await bookAuthorsApi.delete(id)
    showSnackbar('Автор удалён', 'success')
    fetchBook()
  } catch (error) {
    showSnackbar('Ошибка удаления', 'error')
  }
}

const deleteBookEditor = async (id) => {
  try {
    await bookEditorsApi.delete(id)
    showSnackbar('Редактор удалён', 'success')
    fetchBook()
  } catch (error) {
    showSnackbar('Ошибка удаления', 'error')
  }
}

onMounted(() => {
  fetchBook()
  fetchAuthors()
  fetchEditors()
})
</script>

<style scoped>
.book-detail-view {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

