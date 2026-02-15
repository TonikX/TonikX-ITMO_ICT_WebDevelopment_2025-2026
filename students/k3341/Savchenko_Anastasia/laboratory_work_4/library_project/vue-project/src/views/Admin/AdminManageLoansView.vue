<template>
  <div class="manage-loans-view">
    <h1>Управление выдачами</h1>

    <div v-if="!isAdmin" class="not-admin">
      <p>Доступно только администраторам</p>
    </div>

    <div v-else>
      <div class="controls">
        <v-btn color="primary" @click="loadData" :loading="loading" prepend-icon="mdi-refresh">
          {{ loading ? 'Загрузка...' : 'Обновить' }}
        </v-btn>
      </div>

      <div v-if="loading" class="loading">Загрузка...</div>
      <div v-else-if="error" class="error">{{ error }}</div>

      <div v-else>
        <!-- Статистика -->
        <v-row class="stats">
          <v-col cols="12" md="4">
            <v-card class="stat-card">
              <v-card-text class="text-center">
                <div class="text-h6 text-grey">👥 Читателей</div>
                <div class="text-h2 font-weight-bold text-primary">{{ readers.length }}</div>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" md="4">
            <v-card class="stat-card">
              <v-card-text class="text-center">
                <div class="text-h6 text-grey">📚 Книг</div>
                <div class="text-h2 font-weight-bold text-primary">{{ books.length }}</div>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" md="4">
            <v-card class="stat-card">
              <v-card-text class="text-center">
                <div class="text-h6 text-grey">📦 Доступно экз.</div>
                <div class="text-h2 font-weight-bold text-primary">{{ availableCopies }}</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Информация об API -->
        <v-card class="mt-4">
          <v-card-title class="bg-primary text-white">
            <v-icon left color="white">mdi-api</v-icon>
            API Эндпоинты
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <h4 class="text-subtitle-1 font-weight-bold mt-2 mb-1">📖 Чтение (GET)</h4>
                <v-list density="compact">
                  <v-list-item v-for="ep in getEndpoints" :key="ep.path">
                    <v-list-item-title><code>{{ ep.path }}</code></v-list-item-title>
                    <v-list-item-subtitle>{{ ep.desc }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-col>
              <v-col cols="12" md="6">
                <h4 class="text-subtitle-1 font-weight-bold mt-2 mb-1">✏️ Запись (POST/PATCH)</h4>
                <v-list density="compact">
                  <v-list-item v-for="ep in postEndpoints" :key="ep.path">
                    <v-list-item-title><code>{{ ep.path }}</code></v-list-item-title>
                    <v-list-item-subtitle>{{ ep.desc }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import apiClient from '../../api/client'

const auth = useAuthStore()
const isAdmin = computed(() => auth.isAdmin)

const readers = ref([])
const books = ref([])
const copies = ref([])
const loading = ref(false)
const error = ref(null)

const availableCopies = computed(() =>
  copies.value.filter(c => c.availability_status === 'available').length
)

const loadData = async () => {
  if (!isAdmin.value) return
  loading.value = true; error.value = null
  try {
    const [r, b, c] = await Promise.all([
      apiClient.get('readers/'),
      apiClient.get('books/'),
      apiClient.get('copies/')
    ])
    readers.value = r.data || []
    books.value = b.data || []
    copies.value = c.data || []
  } catch (err) {
    error.value = 'Ошибка загрузки'
  } finally { loading.value = false }
}

const getEndpoints = [
  { path: '/api/books/', desc: 'Список книг' },
  { path: '/api/books/with-copies/', desc: 'Книги + кол-во экз.' },
  { path: '/api/readers/', desc: 'Список читателей (активные)' },
  { path: '/api/admin/readers/', desc: 'Все читатели (админ)' },
  { path: '/api/copies/', desc: 'Все экземпляры' },
  { path: '/api/halls/', desc: 'Читальные залы' },
  { path: '/api/authors/', desc: 'Авторы' },
  { path: '/api/loans/active/', desc: 'Активные выдачи' },
  { path: '/api/loans/overdue/', desc: 'Просроченные (>30 д.)' },
  { path: '/api/reader/{id}/books/', desc: 'Книги читателя' },
  { path: '/api/readers/rare-books/', desc: 'Редкие книги (≤2 экз.)' },
  { path: '/api/readers/young/', desc: 'Читатели <20 лет' },
  { path: '/api/stats/education/', desc: 'Статистика по образованию' },
  { path: '/api/reports/monthly/', desc: 'Отчет за месяц' },
  { path: '/api/user/my-profile/', desc: 'Профиль текущего читателя' }
]

const postEndpoints = [
  { path: '/api/reader/register/', desc: 'Регистрация читателя' },
  { path: '/api/readers/remove-inactive/', desc: 'Исключить неактивных' },
  { path: '/api/books/add/', desc: 'Добавить книгу' },
  { path: '/api/books/decommission/', desc: 'Списать экземпляр' },
  { path: '/api/books/{id}/update-code/', desc: 'Изменить шифр' },
  { path: '/api/copies/create/', desc: 'Создать экземпляр' },
  { path: '/api/copies/transfer-hall/', desc: 'Переместить экземпляр' },
  { path: '/api/loans/create/', desc: 'Выдать книгу' },
  { path: '/api/loans/return/', desc: 'Вернуть книгу' },
  { path: '/api/authors/create/', desc: 'Добавить автора' },
  { path: '/api/book-authors/create/', desc: 'Связать книгу с автором' },
  { path: '/api/user/link-reader/', desc: 'Привязать читателя к user' }
]

onMounted(() => { if (isAdmin.value) loadData() })
</script>

<style scoped>
.manage-loans-view { max-width: 1400px; margin: 0 auto; padding: 20px; }
.not-admin { text-align: center; padding: 40px; background: #f8f9fa; border-radius: 8px; color: #6c757d; }
.controls { margin-bottom: 20px; display: flex; justify-content: flex-end; }
.loading, .error { text-align: center; padding: 40px; }
.stat-card { text-align: center; height: 100%; }
.stat-card .text-h2 { font-size: 3rem !important; line-height: 1.2; }
:deep(.v-list-item) { min-height: 40px; }
code { background: #f5f5f5; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }
</style>