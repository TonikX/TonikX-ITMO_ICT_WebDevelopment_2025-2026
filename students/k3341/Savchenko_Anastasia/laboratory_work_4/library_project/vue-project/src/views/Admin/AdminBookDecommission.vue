<template>
  <div class="admin-book-decommission">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8" lg="6">
          <v-card>
            <!-- Заголовок -->
            <v-card-title class="text-h5 py-3">
              <v-icon left color="primary">mdi-book-remove</v-icon>
              Списание экземпляра
            </v-card-title>

            <v-card-text>
              <!-- Секция "Требуют внимания" (поврежденные экземпляры) -->
              <v-card v-if="damaged.length" class="mb-4" variant="outlined" color="primary">
                <v-card-title class="text-subtitle-2 bg-primary text-white py-1">
                  <v-icon left color="white" size="small">mdi-alert</v-icon>
                  Требуют внимания ({{ damaged.length }})
                </v-card-title>
                <v-list density="compact">
                  <v-list-item v-for="c in damaged" :key="c.id" @click="selectCopy(c)" :active="selectedId === c.id" class="py-0">
                    <template v-slot:prepend>
                      <v-icon :color="getCondColor(c.cond)" size="small">mdi-book</v-icon>
                    </template>
                    <v-list-item-title class="text-body-2">{{ c.title }}</v-list-item-title>
                    <v-list-item-subtitle class="text-caption">
                      №{{ c.id }} | {{ getCondText(c.cond) }} | {{ c.hall }}
                    </v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card>

              <!-- Поиск экземпляра -->
              <v-autocomplete
                v-model="selected"
                :items="items"
                item-title="display"
                item-value="id"
                label="Поиск по книге"
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                density="compact"
                clearable
                return-object
                @update:model-value="onSelect"
                class="mb-3"
              >
                <template v-slot:item="{ props, item }">
                  <v-list-item v-bind="props" density="compact">
                    <v-list-item-title>{{ item.raw.title }} (№{{ item.raw.id }})</v-list-item-title>
                    <v-list-item-subtitle>Сост: {{ getCondText(item.raw.cond) }} | Зал: {{ item.raw.hall }}</v-list-item-subtitle>
                  </v-list-item>
                </template>
              </v-autocomplete>

              <!-- Информация о выбранном экземпляре -->
              <v-card v-if="info" variant="tonal" class="pa-2 mb-3">
                <div class="d-flex align-center">
                  <v-icon :color="getCondColor(info.cond)" size="32" class="mr-2">mdi-book</v-icon>
                  <div>
                    <div class="font-weight-bold">{{ info.title }}</div>
                    <div class="text-caption">
                      №{{ info.id }} |
                      <v-chip :color="info.status === 'available' ? 'success' : 'error'" size="x-small">
                        {{ info.status === 'available' ? 'Доступен' : 'Выдан' }}
                      </v-chip>
                      | {{ getCondText(info.cond) }} | {{ info.hall }}
                    </div>
                  </div>
                </div>
              </v-card>

              <!-- Сообщения -->
              <v-alert v-if="error" type="error" density="compact" class="mb-2">{{ error }}</v-alert>
              <v-alert v-if="success" type="success" density="compact" class="mb-2">
                ✅ Списано: {{ done?.title }} №{{ done?.id }}
              </v-alert>
            </v-card-text>

            <v-card-actions class="pa-3">
              <v-spacer />
              <v-btn color="grey" variant="text" size="small" @click="$router.push('/admin/books')">Отмена</v-btn>
              <v-btn color="primary" :loading="loading" :disabled="!selected" size="small" @click="decommission">
                Списать
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../../api/client'

const router = useRouter()

// Состояние
const copies = ref([])      // все экземпляры
const books = ref([])       // все книги (для получения названий)
const items = ref([])       // форматированные для поиска
const selected = ref(null)  // выбранный экземпляр
const info = ref(null)      // информация о выбранном
const selectedId = ref(null)
const loading = ref(false)
const error = ref('')
const success = ref(false)
const done = ref(null)

// Константы
const condColors = { excellent:'success', good:'info', fair:'warning', poor:'error', damaged:'error' }
const condTexts = { excellent:'Отл', good:'Хор', fair:'Удовл', poor:'Плох', damaged:'Повр' }
const getCondColor = c => condColors[c] || 'grey'
const getCondText = c => condTexts[c] || c

// Получение названия книги
const getBookTitle = (id) => {
  if (!id) return 'Неизвестная книга'
  if (typeof id === 'object' && id?.title) return id.title
  return books.value.find(b => b.book_id === id)?.title || `Книга #${id}`
}

// Поврежденные экземпляры (для секции "Требуют внимания")
const damaged = computed(() => copies.value
  .filter(c => c.availability_status !== 'decommissioned' && ['poor','damaged'].includes(c.copy_condition))
  .map(c => ({
    id: c.copy_book_id,
    title: getBookTitle(c.book_id),
    hall: c.hall_id?.name || c.hall_id || '—',
    cond: c.copy_condition
  }))
)

// Загрузка данных
const loadBooks = async () => {
  try { books.value = (await apiClient.get('books/')).data }
  catch (e) { console.error(e) }
}
const loadCopies = async () => {
  try {
    copies.value = (await apiClient.get('copies/')).data
    items.value = copies.value.map(c => ({
      id: c.copy_book_id,
      title: getBookTitle(c.book_id),
      cond: c.copy_condition,
      hall: c.hall_id?.name || c.hall_id || '—',
      status: c.availability_status,
      display: `${getBookTitle(c.book_id)} (№${c.copy_book_id})`
    }))
  } catch (e) { console.error(e) }
}

// Обработчики выбора
const onSelect = (item) => {
  selected.value = item
  if (item) {
    info.value = {
      id: item.id,
      title: item.title,
      status: item.status,
      hall: item.hall,
      cond: item.cond
    }
    selectedId.value = item.id
  } else {
    info.value = null
    selectedId.value = null
  }
}
const selectCopy = (item) => onSelect(items.value.find(i => i.id === item.id))

// Списание
const decommission = async () => {
  if (!selected.value) return
  loading.value = true; error.value = ''; success.value = false
  try {
    await apiClient.post('books/decommission/', { copy_id: selected.value.id })
    done.value = { id: selected.value.id, title: info.value?.title }
    success.value = true
    setTimeout(() => {
      selected.value = null; info.value = null; selectedId.value = null; success.value = false
      loadCopies()
    }, 2000)
  } catch (err) {
    error.value = err.response?.data?.error || 'Ошибка'
  } finally { loading.value = false }
}

onMounted(() => { loadBooks(); loadCopies() })
</script>

<style scoped>
.admin-book-decommission { padding: 16px; }
.v-card { border-radius: 8px; }
.v-list-item { min-height: 32px; }
.v-chip { font-size: 9px; height: 18px; }
.bg-primary { background-color: #1976D2 !important; }
.text-caption { font-size: 10px; line-height: 1.2; }
.mb-2 { margin-bottom: 6px; } .mb-3 { margin-bottom: 10px; } .mb-4 { margin-bottom: 14px; }
.py-0 { padding: 2px 0; }
</style>