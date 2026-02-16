<template>
  <div class="admin-book-add">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="10" lg="8">
          <v-card>
            <!-- Заголовок -->
            <v-card-title class="text-h5">
              <v-icon left color="primary">mdi-book-plus</v-icon>
              Добавление книги
            </v-card-title>

            <v-card-text>
              <v-form ref="formRef" v-model="valid">
                <!-- Основная информация -->
                <v-row>
                  <v-col cols="12"><h4 class="text-subtitle-2 mb-2">📖 Основное</h4></v-col>
                  <v-col cols="12">
                    <v-text-field v-model="form.title" :rules="[v => !!v]" label="Название *" placeholder="Война и мир"
                      variant="outlined" density="compact" />
                  </v-col>

                  <!-- Автор -->
                  <v-col cols="12" md="8">
                    <v-select v-model="form.authorId" :items="authors" :rules="[v => !!v]" item-title="full_name"
                      item-value="author_id" label="Автор *" variant="outlined" density="compact" clearable />
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-btn color="info" variant="outlined" prepend-icon="mdi-account-plus" @click="showAuthorDialog = true" block>
                      Новый автор
                    </v-btn>
                  </v-col>

                  <!-- Издательство и год -->
                  <v-col cols="12" md="6">
                    <v-text-field v-model="form.publisher" :rules="[v => !!v]" label="Издательство *" variant="outlined" density="compact" />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field v-model="form.year" :rules="[v => !!v && /^\d{4}$/.test(v)]" label="Год *" type="number"
                      variant="outlined" density="compact" />
                  </v-col>

                  <!-- Раздел и инв. номер -->
                  <v-col cols="12" md="6">
                    <v-select v-model="form.section" :items="sections" :rules="[v => !!v]" label="Раздел *" variant="outlined" density="compact" />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field v-model="form.code" :rules="[v => !!v]" label="Инв. номер *" variant="outlined" density="compact" />
                  </v-col>
                </v-row>

                <v-divider class="my-3" />

                <!-- Экземпляры -->
                <v-row>
                  <v-col cols="12"><h4 class="text-subtitle-2 mb-2">📦 Экземпляры</h4></v-col>
                  <v-col cols="12" md="6">
                    <v-text-field v-model="form.copyCount" :rules="[v => v && v > 0]" label="Количество *" type="number" min="1"
                      variant="outlined" density="compact" />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-select v-model="form.hallId" :items="halls" :rules="[v => !!v]" item-title="name" item-value="hall_id"
                      label="Зал *" variant="outlined" density="compact" />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-select v-model="form.condition" :items="conditions" item-title="title" item-value="value"
                      label="Состояние *" variant="outlined" density="compact" />
                  </v-col>
                </v-row>

                <!-- Сообщения -->
                <v-alert v-if="error" type="error" class="mt-3" closable @click:close="error = ''">{{ error }}</v-alert>
                <v-alert v-if="success" type="success" class="mt-3">
                  ✅ Книга добавлена<br>
                  <small>Инв. №: {{ newBook?.inventory_code }} | {{ form.copyCount }} экз.</small>
                </v-alert>
              </v-form>
            </v-card-text>

            <v-card-actions class="pa-4">
              <v-spacer />
              <v-btn color="grey" variant="text" @click="$router.push('/admin/books')">Отмена</v-btn>
              <v-btn color="primary" :loading="loading" @click="addBook">Добавить</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Диалог добавления автора -->
    <v-dialog v-model="showAuthorDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">
          <v-icon left color="primary">mdi-account-plus</v-icon>
          Новый автор
        </v-card-title>
        <v-card-text>
          <v-form ref="authorFormRef" v-model="authorValid">
            <v-text-field v-model="newAuthor.name" :rules="[v => !!v]" label="ФИО *" variant="outlined" density="compact" class="mt-2" />
            <v-text-field v-model="newAuthor.birth" label="Дата рождения" type="date" variant="outlined" density="compact" />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="grey" variant="text" @click="showAuthorDialog = false">Отмена</v-btn>
          <v-btn color="primary" :loading="authorLoading" @click="addAuthor">Добавить</v-btn>
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

// Состояние формы
const formRef = ref(null)
const valid = ref(false)
const loading = ref(false)
const error = ref('')
const success = ref(false)
const newBook = ref(null)

// Данные для списков
const authors = ref([])
const halls = ref([])
const showAuthorDialog = ref(false)

// Данные формы
const form = reactive({
  title: '',
  authorId: null,
  publisher: '',
  year: '',
  section: '',
  code: '',
  copyCount: 1,
  hallId: null,
  condition: 'good'
})

// Новый автор
const authorFormRef = ref(null)
const authorValid = ref(false)
const authorLoading = ref(false)
const newAuthor = reactive({ name: '', birth: '' })

// Разделы и состояния
const sections = [
  'Русская классика', 'Зарубежная классика', 'Современная проза',
  'Поэзия', 'Драматургия', 'Научная литература', 'Учебная литература',
  'Детская литература', 'Фантастика', 'Детектив', 'История', 'Философия', 'Искусство'
]

const conditions = [
  { title: 'Отличное', value: 'excellent' },
  { title: 'Хорошее', value: 'good' },
  { title: 'Удовлетворительное', value: 'fair' },
  { title: 'Плохое', value: 'poor' },
  { title: 'Поврежден', value: 'damaged' }
]

// Загрузка данных
const loadAuthors = async () => {
  try { authors.value = (await apiClient.get('authors/')).data }
  catch (e) { console.error(e) }
}
const loadHalls = async () => {
  try { halls.value = (await apiClient.get('halls/')).data }
  catch (e) { console.error(e) }
}

// Добавление автора
const addAuthor = async () => {
  if (!authorFormRef.value?.validate()) return
  authorLoading.value = true
  try {
    const res = await apiClient.post('authors/create/', {
      full_name: newAuthor.name,
      birth_date: newAuthor.birth || null
    })
    authors.value.push(res.data)
    form.authorId = res.data.author_id
    showAuthorDialog.value = false
    newAuthor.name = ''; newAuthor.birth = ''
  } catch (e) {
    alert('Ошибка при добавлении автора')
  } finally { authorLoading.value = false }
}

// Добавление книги
const addBook = async () => {
  if (!formRef.value?.validate()) return
  loading.value = true; error.value = ''; success.value = false

  try {
    // Создание книги
    const bookRes = await apiClient.post('books/add/', {
      title: form.title,
      publisher: form.publisher,
      publication_year: parseInt(form.year),
      section: form.section,
      inventory_code: form.code,
      is_in_catalog: true
    })
    const book = bookRes.data

    // Привязка автора
    if (form.authorId) {
      await apiClient.post('book-authors/create/', {
        book_id: book.book_id,
        author_id: form.authorId,
        author_order: 1
      })
    }

    // Создание экземпляров
    for (let i = 0; i < form.copyCount; i++) {
      await apiClient.post('copies/create/', {
        book_id: book.book_id,
        hall_id: form.hallId,
        availability_status: 'available',
        copy_condition: form.condition
      })
    }

    newBook.value = book
    success.value = true

    setTimeout(() => {
      Object.assign(form, {
        title: '', authorId: null, publisher: '', year: '',
        section: '', code: '', copyCount: 1, hallId: null, condition: 'good'
      })
      router.push('/admin/books')
    }, 2000)

  } catch (e) {
    error.value = e.response?.data?.error || 'Ошибка'
  } finally { loading.value = false }
}

onMounted(() => { loadAuthors(); loadHalls() })
</script>

<style scoped>
.admin-book-add { padding: 16px; }
.v-card { border-radius: 8px; }
.v-card-title { background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%); border-bottom: 1px solid #ddd; }
</style>