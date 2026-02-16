<template>
  <div class="admin-copy-transfer">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8" lg="6">
          <v-card>
            <!-- Заголовок с кнопкой назад -->
            <v-card-title class="d-flex align-center pa-4">
              <v-btn icon="mdi-arrow-left" variant="text" @click="$router.push('/admin/books')" class="mr-2" />
              <span class="text-h5">🔄 Перемещение экземпляра</span>
            </v-card-title>

            <v-card-text>
              <!-- Поиск экземпляра -->
              <v-autocomplete
                v-model="selectedCopy"
                :items="copies"
                item-title="label"
                item-value="copy_book_id"
                label="Поиск экземпляра"
                placeholder="Начните вводить название книги"
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                density="compact"
                clearable
                return-object
                @update:model-value="onCopySelected"
                class="mb-4"
              >
                <template v-slot:item="{ props, item }">
                  <v-list-item v-bind="props" density="compact">
                    <v-list-item-title>{{ item.raw.bookTitle }}</v-list-item-title>
                    <v-list-item-subtitle>
                      Экз.№{{ item.raw.copyId }} | {{ item.raw.status }} | {{ item.raw.currentHall }}
                    </v-list-item-subtitle>
                  </v-list-item>
                </template>
              </v-autocomplete>

              <!-- Информация о выбранном экземпляре -->
              <v-card v-if="selectedCopy" variant="tonal" class="pa-3 mb-4">
                <div class="d-flex align-center">
                  <v-icon size="36" color="primary" class="mr-3">mdi-book</v-icon>
                  <div>
                    <div class="font-weight-bold">{{ selectedCopy.bookTitle }}</div>
                    <div class="text-caption">
                      Экз.№{{ selectedCopy.copyId }} | Текущий зал: {{ selectedCopy.currentHall }}
                    </div>
                  </div>
                </div>
              </v-card>

              <!-- Выбор нового зала -->
              <v-select
                v-model="newHallId"
                :items="halls"
                item-title="name"
                item-value="hall_id"
                label="Новый зал *"
                variant="outlined"
                density="compact"
                :disabled="!selectedCopy"
                class="mb-4"
              />

              <!-- Предупреждение для выданных экземпляров -->
              <v-alert
                v-if="selectedCopy?.status === 'Выдан'"
                type="warning"
                density="compact"
                class="mb-3"
              >
                ⚠️ Экземпляр выдан читателю, перемещение невозможно
              </v-alert>

              <!-- Сообщения об ошибке/успехе -->
              <v-alert v-if="error" type="error" density="compact" class="mb-3">{{ error }}</v-alert>
              <v-alert v-if="success" type="success" density="compact" class="mb-3">
                ✅ Перемещено: {{ successMsg }}
              </v-alert>

              <!-- Кнопка перемещения -->
              <v-btn
                color="primary"
                block
                :loading="loading"
                :disabled="!canTransfer"
                @click="transferCopy"
              >
                <v-icon left>mdi-swap-horizontal</v-icon>
                Переместить
              </v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../../api/client'

const router = useRouter()

// Состояние
const copies = ref([])
const halls = ref([])
const books = ref([]) // Добавляем для хранения книг
const selectedCopy = ref(null)
const newHallId = ref(null)
const loading = ref(false)
const error = ref('')
const success = ref(false)
const successMsg = ref('')

// Статусы экземпляров
const statusMap = {
  'available': 'Доступен',
  'on_loan': 'Выдан',
  'decommissioned': 'Списан'
}

// Получение названия книги по ID
const getBookTitle = (bookId) => {
  if (!bookId) return 'Неизвестная книга'
  if (typeof bookId === 'object' && bookId?.title) return bookId.title
  const book = books.value.find(b => b.book_id === bookId)
  return book?.title || `Книга #${bookId}`
}

// Получение названия зала по ID
const getHallName = (hallId) => {
  if (!hallId) return 'Не указан'
  if (typeof hallId === 'object' && hallId?.name) return hallId.name
  const hall = halls.value.find(h => h.hall_id === hallId)
  return hall?.name || `Зал #${hallId}`
}

// Загрузка данных
const loadData = async () => {
  try {
    // Загружаем книги отдельно для получения названий
    const booksRes = await apiClient.get('books/')
    books.value = booksRes.data

    const [copiesRes, hallsRes] = await Promise.all([
      apiClient.get('copies/'),
      apiClient.get('halls/')
    ])

    halls.value = hallsRes.data

    // Форматируем экземпляры для поиска
    copies.value = copiesRes.data.map(c => {
      const bookTitle = getBookTitle(c.book_id)
      const hallName = getHallName(c.hall_id)

      return {
        copy_book_id: c.copy_book_id,
        copyId: c.copy_book_id,
        bookTitle,
        currentHall: hallName,
        status: statusMap[c.availability_status] || c.availability_status,
        label: `${bookTitle} (№${c.copy_book_id})`
      }
    })

  } catch (e) {
    error.value = 'Ошибка загрузки данных'
    console.error(e)
  }
}

// Выбор экземпляра
const onCopySelected = (copy) => {
  selectedCopy.value = copy
  newHallId.value = null
  error.value = ''
  success.value = false
}

// Можно ли перемещать
const canTransfer = computed(() =>
  selectedCopy.value &&
  newHallId.value &&
  selectedCopy.value.status !== 'Выдан'
)

// Перемещение
const transferCopy = async () => {
  if (!selectedCopy.value || !newHallId.value) return

  loading.value = true
  error.value = ''
  success.value = false

  try {
    const res = await apiClient.post('copies/transfer-hall/', {
      copy_id: selectedCopy.value.copy_book_id,
      hall_id: newHallId.value
    })

    // Находим название нового зала
    const newHall = halls.value.find(h => h.hall_id === newHallId.value)
    successMsg.value = `${selectedCopy.value.bookTitle} → ${newHall?.name || 'новый зал'}`
    success.value = true

    // Обновляем данные через 2 сек
    setTimeout(() => {
      selectedCopy.value = null
      newHallId.value = null
      success.value = false
      loadData()
    }, 2000)

  } catch (err) {
    error.value = err.response?.data?.error || 'Ошибка перемещения'
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

<style scoped>
.admin-copy-transfer { padding: 16px; }
.v-card { border-radius: 8px; }
</style>