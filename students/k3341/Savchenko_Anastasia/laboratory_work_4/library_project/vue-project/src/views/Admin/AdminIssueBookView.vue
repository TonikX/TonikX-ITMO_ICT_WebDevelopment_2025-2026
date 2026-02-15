<template>
  <div class="admin-issue-book">
    <v-container fluid>
      <v-row><v-col cols="12"><h1 class="text-h4 mb-4">📘 Выдача книги</h1></v-col></v-row>

      <v-row v-if="!isAdmin"><v-col cols="12"><v-alert type="warning">Только для администраторов</v-alert></v-col></v-row>

      <template v-else>
        <v-row>
          <!-- Поиск читателя -->
          <v-col cols="12" md="6">
            <v-card class="pa-4">
              <v-card-title class="text-h5 pa-0 mb-4"><v-icon color="primary" class="mr-2">mdi-account</v-icon>Читатель</v-card-title>
              <v-text-field v-model="qReader" label="Поиск читателя" placeholder="ФИО или билет" prepend-inner-icon="mdi-magnify"
                variant="outlined" density="compact" clearable @input="searchReaderDebounced" :loading="loadingReader" />

              <!-- Результаты -->
              <v-card v-if="foundReaders.length" variant="outlined" class="mt-2">
                <v-list density="compact">
                  <v-list-subheader>Найдено: {{ foundReaders.length }}</v-list-subheader>
                  <v-list-item v-for="r in foundReaders" :key="r.reader_id" @click="selectReader(r)" :active="selectedReader?.reader_id === r.reader_id">
                    <template v-slot:prepend><v-avatar :color="getColor(r.full_name)" size="32"><span class="text-white">{{ r.full_name.charAt(0) }}</span></v-avatar></template>
                    <v-list-item-title>{{ r.full_name }}</v-list-item-title>
                    <v-list-item-subtitle>{{ r.library_card_id }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card>

              <!-- Выбранный читатель -->
              <v-card v-if="selectedReader" color="primary" variant="tonal" class="mt-4">
                <v-card-text class="d-flex align-center py-2">
                  <v-avatar :color="getColor(selectedReader.full_name)" size="40" class="mr-2"><span class="text-white">{{ selectedReader.full_name.charAt(0) }}</span></v-avatar>
                  <div><div class="font-weight-bold">{{ selectedReader.full_name }}</div><div class="text-caption">{{ selectedReader.library_card_id }}</div></div>
                  <v-spacer /><v-btn icon="mdi-close" size="small" variant="text" @click="selectedReader = null" />
                </v-card-text>
              </v-card>
            </v-card>
          </v-col>

          <!-- Поиск книги -->
          <v-col cols="12" md="6">
            <v-card class="pa-4">
              <v-card-title class="text-h5 pa-0 mb-4"><v-icon color="primary" class="mr-2">mdi-book</v-icon>Книга</v-card-title>
              <v-text-field v-model="qBook" label="Поиск книги" placeholder="Название или инв. номер" prepend-inner-icon="mdi-magnify"
                variant="outlined" density="compact" clearable @input="searchBookDebounced" :loading="loadingBook" />

              <v-card v-if="foundBooks.length" variant="outlined" class="mt-2">
                <v-list density="compact">
                  <v-list-subheader>Найдено: {{ foundBooks.length }}</v-list-subheader>
                  <v-list-item v-for="b in foundBooks" :key="b.book_id" @click="selectBook(b)" :active="selectedBook?.book_id === b.book_id">
                    <template v-slot:prepend><v-icon color="primary">mdi-book</v-icon></template>
                    <v-list-item-title>{{ b.title }}</v-list-item-title>
                    <v-list-item-subtitle>{{ b.inventory_code }} | {{ b.available_copies }} экз.</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card>

              <v-card v-if="selectedBook" color="primary" variant="tonal" class="mt-4">
                <v-card-text class="d-flex align-center py-2">
                  <v-icon color="primary" size="40" class="mr-2">mdi-book</v-icon>
                  <div><div class="font-weight-bold">{{ selectedBook.title }}</div><div class="text-caption">{{ selectedBook.inventory_code }}</div></div>
                  <v-spacer /><v-btn icon="mdi-close" size="small" variant="text" @click="selectedBook = null" />
                </v-card-text>
              </v-card>
            </v-card>
          </v-col>

          <!-- Параметры выдачи -->
          <v-col cols="12">
            <v-card class="pa-4" :disabled="!canIssue">
              <v-card-title class="text-h5 pa-0 mb-4"><v-icon color="primary" class="mr-2">mdi-book-plus</v-icon>Параметры</v-card-title>
              <v-row>
                <v-col cols="12" md="6">
                  <v-select v-model="copyId" :items="copies" item-title="label" item-value="copy_book_id" label="Экземпляр"
                    variant="outlined" density="compact" :disabled="!selectedBook" />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field v-model="dueDate" label="Срок возврата" type="date" variant="outlined" density="compact" :min="tomorrow" />
                </v-col>
              </v-row>
              <v-alert v-if="error" type="error" class="mt-2" closable @click:close="error = ''">{{ error }}</v-alert>
              <v-alert v-if="success" type="success" class="mt-2">✅ Книга выдана</v-alert>
              <v-card-actions class="pa-0 mt-2">
                <v-spacer /><v-btn color="success" :loading="issuing" :disabled="!canIssue || !copyId || !dueDate" @click="issue">
                  <v-icon left>mdi-book-check</v-icon> Выдать
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

// Поиск
const qReader = ref('')
const qBook = ref('')
const loadingReader = ref(false)
const loadingBook = ref(false)
const foundReaders = ref([])
const foundBooks = ref([])

// Выбранное
const selectedReader = ref(null)
const selectedBook = ref(null)
const copies = ref([])
const copyId = ref(null)
const dueDate = ref('')

// Состояние
const issuing = ref(false)
const error = ref('')
const success = ref(false)

let timerReader, timerBook

const tomorrow = computed(() => {
  const d = new Date(); d.setDate(d.getDate() + 1); return d.toISOString().split('T')[0]
})
const canIssue = computed(() => selectedReader.value && selectedBook.value)

const getColor = (name) => {
  const colors = ['primary', 'success', 'info', 'warning', 'error']
  return colors[name.charCodeAt(0) % colors.length]
}

// Поиск читателя
const searchReader = async () => {
  if (!qReader.value.trim()) { foundReaders.value = []; return }
  loadingReader.value = true
  try {
    const all = (await apiClient.get('readers/')).data
    const q = qReader.value.toLowerCase()
    foundReaders.value = all.filter(r => r.full_name.toLowerCase().includes(q) || r.library_card_id.toLowerCase().includes(q))
  } finally { loadingReader.value = false }
}
const searchReaderDebounced = () => { clearTimeout(timerReader); timerReader = setTimeout(searchReader, 300) }

const selectReader = (r) => { selectedReader.value = r; foundReaders.value = []; qReader.value = '' }

// Поиск книги
const searchBook = async () => {
  if (!qBook.value.trim()) { foundBooks.value = []; return }
  loadingBook.value = true
  try {
    const all = (await apiClient.get('books/with-copies/')).data
    const q = qBook.value.toLowerCase()
    foundBooks.value = all.filter(b => b.title.toLowerCase().includes(q) || b.inventory_code.toLowerCase().includes(q))
  } finally { loadingBook.value = false }
}
const searchBookDebounced = () => { clearTimeout(timerBook); timerBook = setTimeout(searchBook, 300) }

const selectBook = async (b) => {
  selectedBook.value = b; foundBooks.value = []; qBook.value = ''; copyId.value = null
  try {
    const all = (await apiClient.get('copies/')).data
    copies.value = all.filter(c => c.book_id === b.book_id && c.availability_status === 'available')
      .map(c => ({ copy_book_id: c.copy_book_id, label: `№${c.copy_book_id} — ${c.copy_condition || 'хор'}` }))
  } catch (e) { console.error(e) }
}

// Выдача
const issue = async () => {
  if (!copyId.value || !dueDate.value) return
  issuing.value = true; error.value = ''; success.value = false
  try {
    await apiClient.post('loans/create/', {
      copy_book_id: copyId.value,
      reader_id: selectedReader.value.reader_id,
      issued_at: new Date().toISOString().split('T')[0],
      due_date: dueDate.value
    })
    success.value = true
    setTimeout(() => {
      selectedReader.value = selectedBook.value = null
      copyId.value = null; copies.value = []
      qReader.value = qBook.value = ''
      success.value = false
    }, 2000)
  } catch (e) {
    error.value = e.response?.data?.error || 'Ошибка'
  } finally { issuing.value = false }
}

onMounted(() => {
  const d = new Date(); d.setDate(d.getDate() + 14); dueDate.value = d.toISOString().split('T')[0]
})
</script>