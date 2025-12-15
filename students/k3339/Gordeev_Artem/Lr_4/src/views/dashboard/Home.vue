<template>
  <div>
    <h1 class="text-h4 font-weight-bold mb-6">Панель управления</h1>
    
    <!-- Секция приветствия -->
    <v-card class="mb-6" color="primary" variant="tonal">
      <v-card-item>
        <v-card-title class="text-h6">Добро пожаловать, {{ user?.first_name || user?.username }}!</v-card-title>
        <v-card-subtitle>Система управления типографией готова к работе.</v-card-subtitle>
      </v-card-item>
    </v-card>

    <!-- Карточки статистики -->
    <v-row class="mb-6">
      <v-col cols="12" sm="6" md="3">
        <v-card elevation="2" class="h-100">
          <v-card-item>
            <div class="text-overline mb-1">Книги</div>
            <div class="text-h4 mb-2">{{ stats.books }}</div>
            <v-icon color="primary" icon="mdi-book-open-page-variant" size="large" class="position-absolute top-0 right-0 ma-4"></v-icon>
          </v-card-item>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
         <v-card elevation="2" class="h-100">
          <v-card-item>
            <div class="text-overline mb-1">Авторы</div>
             <div class="text-h4 mb-2">{{ stats.authors }}</div>
            <v-icon color="success" icon="mdi-account-group" size="large" class="position-absolute top-0 right-0 ma-4"></v-icon>
          </v-card-item>
        </v-card>
      </v-col>
       <v-col cols="12" sm="6" md="3">
         <v-card elevation="2" class="h-100">
          <v-card-item>
            <div class="text-overline mb-1">Контракты</div>
             <div class="text-h4 mb-2">{{ stats.contracts }}</div>
            <v-icon color="info" icon="mdi-file-document-edit" size="large" class="position-absolute top-0 right-0 ma-4"></v-icon>
          </v-card-item>
        </v-card>
      </v-col>
       <v-col cols="12" sm="6" md="3">
         <v-card elevation="2" class="h-100">
          <v-card-item>
            <div class="text-overline mb-1">Менеджеры</div>
             <div class="text-h4 mb-2">{{ stats.managers }}</div>
            <v-icon color="warning" icon="mdi-check-decagram" size="large" class="position-absolute top-0 right-0 ma-4"></v-icon>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <!-- Последние действия -->
      <v-col cols="12" md="8">
        <v-card class="h-100" elevation="2">
          <v-card-title class="d-flex align-center">
            Последние контракты
            <v-spacer></v-spacer>
            <v-btn variant="text" size="small" color="primary" to="/contracts">Все контракты</v-btn>
          </v-card-title>
          <v-table>
            <thead>
              <tr>
                <th>Номер</th>
                <th>Дата</th>
                <th>Книга</th>
                <th>Менеджер</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="c in recentContracts" :key="c.id">
                <td>{{ c.number }}</td>
                <td>{{ c.date_signed }}</td>
                <td>{{ getBookTitle(c.book) }}</td>
                <td>{{ getManagerName(c.manager) }}</td>
              </tr>
              <tr v-if="recentContracts.length === 0">
                <td colspan="4" class="text-center text-grey">Нет последних контрактов</td>
              </tr>
            </tbody>
          </v-table>
        </v-card>
      </v-col>

      <!-- Быстрые действия -->
      <v-col cols="12" md="4">
        <v-card class="h-100" elevation="2">
          <v-card-title>Быстрые действия</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item to="/contracts" rounded="lg" class="mb-2" color="primary" variant="tonal">
                <template v-slot:prepend><v-icon icon="mdi-plus"></v-icon></template>
                <v-list-item-title>Создать контракт</v-list-item-title>
              </v-list-item>
              <v-list-item to="/books" rounded="lg" class="mb-2" color="primary" variant="tonal">
                <template v-slot:prepend><v-icon icon="mdi-book-plus"></v-icon></template>
                <v-list-item-title>Добавить книгу</v-list-item-title>
              </v-list-item>
              <v-list-item to="/authors" rounded="lg" color="primary" variant="tonal">
                <template v-slot:prepend><v-icon icon="mdi-account-plus"></v-icon></template>
                <v-list-item-title>Добавить автора</v-list-item-title>
              </v-list-item>
               <v-divider class="my-4"></v-divider>
               <v-list-item to="/reports" rounded="lg" color="secondary" variant="flat">
                <template v-slot:prepend><v-icon icon="mdi-chart-bar"></v-icon></template>
                <v-list-item-title>Перейти к отчетам</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import typography from '@/api/typography'
import { useAlertStore } from '@/stores/alert'

const authStore = useAuthStore()
const alertStore = useAlertStore()
const user = computed(() => authStore.user)

const stats = ref({
    books: 0,
    authors: 0,
    contracts: 0,
    managers: 0
})

const recentContracts = ref([])
const booksMap = ref({})
const managersMap = ref({})

const fetchData = async () => {
    try {
        const [booksRes, authorsRes, contractsRes, usersRes] = await Promise.all([
            typography.getBooks(),
            typography.getAuthors(),
            typography.getContracts(),
            typography.getUsers()
        ])

        // Статистика
        stats.value.books = booksRes.data.length
        stats.value.authors = authorsRes.data.length
        stats.value.contracts = contractsRes.data.length
        
        let users = []
        if (Array.isArray(usersRes.data)) users = usersRes.data
        else if (Array.isArray(usersRes.data.results)) users = usersRes.data.results
        stats.value.managers = users.length // Считаем всех пользователей как менеджеров/персонал для упрощения
        
        // Словари для отображения
        booksRes.data.forEach(b => booksMap.value[b.id] = b.title)
        users.forEach(u => managersMap.value[u.id] = u.username)

        // Последние контракты (Последние 5)
        const sorted = [...contractsRes.data].sort((a, b) => new Date(b.date_signed) - new Date(a.date_signed))
        recentContracts.value = sorted.slice(0, 5)

    } catch (e) {
        console.error(e)
        alertStore.showError(e)
    }
}

const getBookTitle = (id) => booksMap.value[id] || id
const getManagerName = (id) => managersMap.value[id] || id

onMounted(() => {
    if (!authStore.user) {
        authStore.fetchUser()
    }
    fetchData()
})
</script>
