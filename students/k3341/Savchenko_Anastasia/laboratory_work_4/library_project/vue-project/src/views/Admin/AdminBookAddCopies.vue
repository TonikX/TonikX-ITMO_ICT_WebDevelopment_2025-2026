<template>
  <div class="admin-book-add-copies">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8" lg="6">
          <v-card>
            <!-- Заголовок -->
            <v-card-title class="text-h5">
              <v-icon left color="primary">mdi-book-plus-multiple</v-icon>
              Добавление экземпляров
            </v-card-title>

            <v-card-text>
              <v-form ref="formRef" v-model="valid">
                <!-- Поиск книги -->
                <v-autocomplete
                  v-model="book"
                  :items="bookItems"
                  item-title="label"
                  label="Поиск книги"
                  placeholder="Название или инв. номер"
                  prepend-inner-icon="mdi-magnify"
                  variant="outlined"
                  density="compact"
                  clearable
                  return-object
                  @update:model-value="onBookSelect"
                  :rules="[v => !!v]"
                  class="mb-4"
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props">
                      <v-list-item-title>{{ item.raw.title }}</v-list-item-title>
                      <v-list-item-subtitle>Инв. №: {{ item.raw.code }}</v-list-item-subtitle>
                    </v-list-item>
                  </template>
                </v-autocomplete>

                <!-- Инфо о книге -->
                <v-card v-if="book" variant="tonal" class="pa-2 mb-4">
                  <div class="d-flex align-center">
                    <v-icon color="primary" size="36" class="mr-3">mdi-book</v-icon>
                    <div>
                      <div class="font-weight-bold">{{ book.title }}</div>
                      <div class="text-caption">Инв. №: {{ book.code }}</div>
                    </div>
                  </div>
                </v-card>

                <v-divider class="my-3" />

                <!-- Параметры новых экземпляров -->
                <v-row>
                  <v-col cols="12" md="6">
                    <v-text-field v-model="form.count" :rules="[v => v && v > 0]" label="Количество *" type="number" min="1"
                      variant="outlined" density="compact" />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-select v-model="form.hallId" :items="halls" item-title="name" item-value="hall_id" label="Зал *"
                      variant="outlined" density="compact" :rules="[v => !!v]" />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-select v-model="form.condition" :items="conditions" item-title="title" item-value="value" label="Состояние *"
                      variant="outlined" density="compact" />
                  </v-col>
                </v-row>

                <!-- Текущие экземпляры -->
                <v-card v-if="book && existing.length" variant="outlined" class="mt-4">
                  <v-card-title class="text-subtitle-2 bg-grey-lighten-3 py-1">
                    <v-icon left size="18">mdi-book-multiple</v-icon>
                    Текущие экземпляры ({{ existing.length }})
                  </v-card-title>
                  <v-list density="compact">
                    <v-list-item v-for="c in existing" :key="c.id" class="border-bottom py-0">
                      <template v-slot:prepend>
                        <v-icon :color="statusColor(c.status)" size="18">{{ statusIcon(c.status) }}</v-icon>
                      </template>
                      <v-list-item-title class="text-body-2">Экз. №{{ c.id }}</v-list-item-title>
                      <v-list-item-subtitle class="text-caption">
                        <v-chip :color="statusColor(c.status)" size="x-small">{{ statusText(c.status) }}</v-chip>
                        <v-chip :color="condColor(c.cond)" size="x-small" class="ml-1">{{ condText(c.cond) }}</v-chip>
                        <span class="ml-1">Зал: {{ c.hall }}</span>
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-card>

                <!-- Сообщения -->
                <v-alert v-if="error" type="error" class="mt-3" closable @click:close="error = ''">{{ error }}</v-alert>
                <v-alert v-if="success" type="success" class="mt-3">✅ {{ msg }}</v-alert>
              </v-form>
            </v-card-text>

            <v-card-actions class="pa-4">
              <v-spacer />
              <v-btn color="grey" variant="text" @click="$router.push('/admin/books')">Отмена</v-btn>
              <v-btn color="primary" :loading="loading" :disabled="!canAdd" @click="addCopies">
                <v-icon left>mdi-book-plus</v-icon> Добавить
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../../api/client'

const router = useRouter()

// Состояние
const books = ref([])          // все книги
const bookItems = ref([])      // книги для поиска
const halls = ref([])          // все залы
const copies = ref([])         // все экземпляры
const existing = ref([])       // экземпляры выбранной книги
const book = ref(null)         // выбранная книга

const formRef = ref(null)
const valid = ref(false)
const loading = ref(false)
const error = ref('')
const success = ref(false)
const msg = ref('')

// Данные формы
const form = reactive({
  count: 1,
  hallId: null,
  condition: 'good'
})

// Константы для статусов
const statusColors = { available:'success', on_loan:'warning', reserved:'info', decommissioned:'error' }
const statusIcons = { available:'mdi-check-circle', on_loan:'mdi-book-clock', reserved:'mdi-book-lock', decommissioned:'mdi-book-remove' }
const statusTexts = { available:'Доступен', on_loan:'Выдан', reserved:'Зарезервирован', decommissioned:'Списан' }

// Константы для состояний
const condColors = { excellent:'success', good:'info', fair:'warning', poor:'error', damaged:'error' }
const condTexts = { excellent:'Отл', good:'Хор', fair:'Удовл', poor:'Плох', damaged:'Повр' }

const conditions = [
  { title: 'Отличное', value: 'excellent' },
  { title: 'Хорошее', value: 'good' },
  { title: 'Удовлетворительное', value: 'fair' },
  { title: 'Плохое', value: 'poor' },
  { title: 'Поврежден', value: 'damaged' }
]

// Вспомогательные функции
const statusColor = s => statusColors[s] || 'grey'
const statusIcon = s => statusIcons[s] || 'mdi-book'
const statusText = s => statusTexts[s] || s
const condColor = c => condColors[c] || 'grey'
const condText = c => condTexts[c] || c

// Можно ли добавлять
const canAdd = computed(() => book.value && form.count > 0 && form.hallId)

// Загрузка данных
const loadBooks = async () => {
  try {
    const res = await apiClient.get('books/with-copies/')
    books.value = res.data
    bookItems.value = res.data.map(b => ({
      book_id: b.book_id,
      title: b.title,
      code: b.inventory_code,
      label: `${b.title} (${b.inventory_code})`
    }))
  } catch (e) { console.error(e) }
}

const loadHalls = async () => {
  try { halls.value = (await apiClient.get('halls/')).data }
  catch (e) { console.error(e) }
}

const loadCopiesForBook = async (bookId) => {
  try {
    copies.value = (await apiClient.get('copies/')).data
    existing.value = copies.value
      .filter(c => c.book_id === bookId || c.book_id?.book_id === bookId)
      .map(c => ({
        id: c.copy_book_id,
        status: c.availability_status,
        cond: c.copy_condition,
        hall: c.hall_id?.name || c.hall_id || '—'
      }))
  } catch (e) { console.error(e) }
}

// Обработчики
const onBookSelect = (b) => {
  book.value = b
  if (b) loadCopiesForBook(b.book_id)
  else existing.value = []
}

// Добавление экземпляров
const addCopies = async () => {
  if (!book.value || !form.count || !form.hallId) return
  loading.value = true; error.value = ''; success.value = false

  try {
    for (let i = 0; i < form.count; i++) {
      await apiClient.post('copies/create/', {
        book_id: book.value.book_id,
        hall_id: form.hallId,
        availability_status: 'available',
        copy_condition: form.condition
      })
    }

    msg.value = `✅ Добавлено ${form.count} экз. к "${book.value.title}"`
    success.value = true
    await loadCopiesForBook(book.value.book_id)

    setTimeout(() => {
      form.count = 1
      success.value = false
    }, 2000)

  } catch (e) {
    error.value = 'Ошибка при добавлении'
  } finally { loading.value = false }
}

onMounted(() => { loadBooks(); loadHalls() })
</script>

<style scoped>
.admin-book-add-copies { padding: 16px; }
.v-card { border-radius: 8px; }
.v-card-title { background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); border-bottom: 1px solid #90caf9; }
.border-bottom { border-bottom: 1px solid #eee; }
.v-chip { font-size: 9px; height: 18px; }
</style>