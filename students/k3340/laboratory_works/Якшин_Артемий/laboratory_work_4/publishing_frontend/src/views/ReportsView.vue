<template>
  <div class="reports-view">
    <v-row class="mb-4">
      <v-col cols="12">
        <h1 class="page-title">
          <v-icon class="mr-2">mdi-chart-bar</v-icon>
          Отчёты
        </h1>
      </v-col>
    </v-row>

    <v-card>
      <v-tabs v-model="activeTab" color="primary" grow>
        <v-tab value="books-by-author">
          <v-icon left>mdi-book-account</v-icon>
          Книги по авторам
        </v-tab>
        <v-tab value="chief-editors">
          <v-icon left>mdi-account-edit</v-icon>
          Отв. редакторы
        </v-tab>
        <v-tab value="editors-per-book">
          <v-icon left>mdi-book-edit</v-icon>
          Редакторы книг
        </v-tab>
        <v-tab value="contracts-by-month">
          <v-icon left>mdi-calendar-month</v-icon>
          Контракты по месяцам
        </v-tab>
        <v-tab value="top-managers">
          <v-icon left>mdi-trophy</v-icon>
          Топ менеджеры
        </v-tab>
        <v-tab value="quarterly">
          <v-icon left>mdi-calendar-check</v-icon>
          Квартальный отчёт
        </v-tab>
      </v-tabs>

      <v-window v-model="activeTab">
        <!-- Books by Author -->
        <v-window-item value="books-by-author">
          <v-card-text>
            <v-row class="mb-4">
              <v-col cols="12" md="6">
                <v-select
                  v-model="booksByAuthor.authorId"
                  :items="authors"
                  item-title="full_name"
                  item-value="id"
                  label="Выберите автора"
                  clearable
                ></v-select>
              </v-col>
              <v-col cols="12" md="6" class="d-flex align-center">
                <v-btn color="primary" @click="fetchBooksByAuthor" :loading="booksByAuthor.loading"
                       :disabled="!booksByAuthor.authorId">
                  <v-icon left>mdi-magnify</v-icon>
                  Показать
                </v-btn>
              </v-col>
            </v-row>

            <template v-if="booksByAuthor.data">
              <v-alert type="info" variant="tonal" class="mb-4">
                <strong>{{ booksByAuthor.data.author.name }}</strong> — 
                {{ booksByAuthor.data.books_count }} книг
              </v-alert>

              <v-data-table
                :headers="booksByAuthorHeaders"
                :items="booksByAuthor.data.books"
                density="compact"
                class="elevation-0"
              ></v-data-table>
            </template>
          </v-card-text>
        </v-window-item>

        <!-- Chief Editors -->
        <v-window-item value="chief-editors">
          <v-card-text>
            <v-btn color="primary" @click="fetchChiefEditors" :loading="chiefEditors.loading" class="mb-4">
              <v-icon left>mdi-refresh</v-icon>
              Обновить
            </v-btn>

            <template v-if="chiefEditors.data">
              <v-alert type="info" variant="tonal" class="mb-4">
                Всего книг с ответственными редакторами: {{ chiefEditors.data.total_books }}
              </v-alert>

              <v-data-table
                :headers="chiefEditorsHeaders"
                :items="chiefEditors.data.chief_editors"
                density="compact"
                class="elevation-0"
              ></v-data-table>
            </template>
          </v-card-text>
        </v-window-item>

        <!-- Editors per Book -->
        <v-window-item value="editors-per-book">
          <v-card-text>
            <v-btn color="primary" @click="fetchEditorsPerBook" :loading="editorsPerBook.loading" class="mb-4">
              <v-icon left>mdi-refresh</v-icon>
              Обновить
            </v-btn>

            <template v-if="editorsPerBook.data">
              <v-alert type="info" variant="tonal" class="mb-4">
                Всего книг: {{ editorsPerBook.data.total_books }}
              </v-alert>

              <v-data-table
                :headers="editorsPerBookHeaders"
                :items="editorsPerBook.data.books"
                density="compact"
                class="elevation-0"
              >
                <template v-slot:item.chief_editor="{ item }">
                  <v-chip v-if="item.chief_editor" color="secondary" size="small">
                    {{ item.chief_editor }}
                  </v-chip>
                  <span v-else class="text-medium-emphasis">—</span>
                </template>
              </v-data-table>
            </template>
          </v-card-text>
        </v-window-item>

        <!-- Contracts by Month -->
        <v-window-item value="contracts-by-month">
          <v-card-text>
            <v-row class="mb-4">
              <v-col cols="12" md="4">
                <v-text-field
                  v-model.number="contractsByMonth.year"
                  label="Год"
                  type="number"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6" class="d-flex align-center">
                <v-btn color="primary" @click="fetchContractsByMonth" :loading="contractsByMonth.loading">
                  <v-icon left>mdi-magnify</v-icon>
                  Показать
                </v-btn>
              </v-col>
            </v-row>

            <template v-if="contractsByMonth.data">
              <v-alert type="info" variant="tonal" class="mb-4">
                <strong>{{ contractsByMonth.data.year }} год</strong> — 
                всего контрактов: {{ contractsByMonth.data.total_contracts }}
              </v-alert>

              <v-data-table
                :headers="contractsByMonthHeaders"
                :items="contractsByMonth.data.by_month"
                density="compact"
                class="elevation-0"
              >
                <template v-slot:item.month="{ item }">
                  {{ formatMonth(item.month) }}
                </template>
              </v-data-table>
            </template>
          </v-card-text>
        </v-window-item>

        <!-- Top Managers -->
        <v-window-item value="top-managers">
          <v-card-text>
            <v-row class="mb-4">
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="topManagers.startDate"
                  label="Дата начала"
                  type="date"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="topManagers.endDate"
                  label="Дата окончания"
                  type="date"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="4" class="d-flex align-center">
                <v-btn color="primary" @click="fetchTopManagers" :loading="topManagers.loading"
                       :disabled="!topManagers.startDate || !topManagers.endDate">
                  <v-icon left>mdi-magnify</v-icon>
                  Показать
                </v-btn>
              </v-col>
            </v-row>

            <template v-if="topManagers.data">
              <v-alert :type="topManagers.data.top_managers?.length ? 'success' : 'warning'" variant="tonal" class="mb-4">
                <template v-if="topManagers.data.top_managers?.length">
                  Максимум контрактов: {{ topManagers.data.max_contracts_count }}
                </template>
                <template v-else>
                  {{ topManagers.data.message }}
                </template>
              </v-alert>

              <v-data-table
                v-if="topManagers.data.top_managers?.length"
                :headers="topManagersHeaders"
                :items="topManagers.data.top_managers"
                density="compact"
                class="elevation-0"
              ></v-data-table>
            </template>
          </v-card-text>
        </v-window-item>

        <!-- Quarterly Report -->
        <v-window-item value="quarterly">
          <v-card-text>
            <v-row class="mb-4">
              <v-col cols="12" md="4">
                <v-select
                  v-model="quarterly.quarter"
                  :items="quarterOptions"
                  label="Квартал"
                ></v-select>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model.number="quarterly.year"
                  label="Год"
                  type="number"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="4" class="d-flex align-center">
                <v-btn color="primary" @click="fetchQuarterlyReport" :loading="quarterly.loading">
                  <v-icon left>mdi-magnify</v-icon>
                  Сформировать
                </v-btn>
              </v-col>
            </v-row>

            <template v-if="quarterly.data">
              <v-alert type="info" variant="tonal" class="mb-4">
                <strong>{{ quarterly.data.period }}</strong><br>
                Всего контрактов за квартал: {{ quarterly.data.total_contracts }}
              </v-alert>

              <h3 class="mb-2">Итоги по месяцам</h3>
              <v-data-table
                :headers="monthlySummaryHeaders"
                :items="quarterly.data.monthly_summary"
                density="compact"
                class="elevation-0 mb-6"
              ></v-data-table>

              <h3 class="mb-2">Детализация контрактов</h3>
              <v-data-table
                :headers="quarterlyDetailHeaders"
                :items="quarterly.data.contracts"
                density="compact"
                class="elevation-0"
              >
                <template v-slot:item.has_illustrations="{ item }">
                  <v-icon :icon="item.has_illustrations ? 'mdi-check' : 'mdi-close'" 
                          :color="item.has_illustrations ? 'success' : 'grey'" size="small"></v-icon>
                </template>
              </v-data-table>
            </template>
          </v-card-text>
        </v-window-item>
      </v-window>
    </v-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { reportsApi, authorsApi } from '@/services/api'

const route = useRoute()

const activeTab = ref(route.query.tab || 'books-by-author')
const authors = ref([])

// Report states
const booksByAuthor = reactive({
  authorId: null,
  loading: false,
  data: null
})

const chiefEditors = reactive({
  loading: false,
  data: null
})

const editorsPerBook = reactive({
  loading: false,
  data: null
})

const contractsByMonth = reactive({
  year: new Date().getFullYear(),
  loading: false,
  data: null
})

const topManagers = reactive({
  startDate: new Date(new Date().getFullYear(), 0, 1).toISOString().split('T')[0],
  endDate: new Date().toISOString().split('T')[0],
  loading: false,
  data: null
})

const quarterly = reactive({
  quarter: Math.ceil((new Date().getMonth() + 1) / 3),
  year: new Date().getFullYear(),
  loading: false,
  data: null
})

const quarterOptions = [
  { title: '1 квартал (янв-мар)', value: 1 },
  { title: '2 квартал (апр-июн)', value: 2 },
  { title: '3 квартал (июл-сен)', value: 3 },
  { title: '4 квартал (окт-дек)', value: 4 }
]

// Table headers
const booksByAuthorHeaders = [
  { title: 'ID', key: 'id', width: '80px' },
  { title: 'Название', key: 'title' },
  { title: 'ISBN', key: 'isbn' },
  { title: 'Страниц', key: 'pages', width: '100px' },
  { title: 'Дата публикации', key: 'publication_date' },
  { title: 'Контракт', key: 'contract_number' }
]

const chiefEditorsHeaders = [
  { title: 'Книга', key: 'book_title' },
  { title: 'ISBN', key: 'book_isbn' },
  { title: 'Редактор', key: 'editor_name' },
  { title: 'Email', key: 'editor_email' },
  { title: 'Назначен', key: 'assigned_date' }
]

const editorsPerBookHeaders = [
  { title: 'ID', key: 'book_id', width: '80px' },
  { title: 'Книга', key: 'book_title' },
  { title: 'Кол-во редакторов', key: 'editors_count', width: '150px' },
  { title: 'Ответственный', key: 'chief_editor' }
]

const contractsByMonthHeaders = [
  { title: 'Месяц', key: 'month' },
  { title: 'Количество контрактов', key: 'count' }
]

const topManagersHeaders = [
  { title: 'ID', key: 'manager_id', width: '80px' },
  { title: 'Менеджер', key: 'manager_name' },
  { title: 'Email', key: 'manager_email' },
  { title: 'Кол-во контрактов', key: 'contracts_count', width: '150px' }
]

const monthlySummaryHeaders = [
  { title: 'Месяц', key: 'month' },
  { title: 'Кол-во контрактов', key: 'contracts_count' }
]

const quarterlyDetailHeaders = [
  { title: '№ Контракта', key: 'contract_number', width: '130px' },
  { title: 'Книга', key: 'book_title' },
  { title: 'Авторов', key: 'authors_count', width: '90px' },
  { title: 'Редакторов', key: 'editors_count', width: '100px' },
  { title: 'Страниц', key: 'pages', width: '90px' },
  { title: 'Илл.', key: 'has_illustrations', width: '70px' },
  { title: 'Подписан', key: 'signed_date', width: '110px' },
  { title: 'Месяц', key: 'month' }
]

const formatMonth = (dateStr) => {
  if (!dateStr) return '—'
  const date = new Date(dateStr)
  return date.toLocaleDateString('ru-RU', { month: 'long', year: 'numeric' })
}

const fetchAuthors = async () => {
  try {
    const response = await authorsApi.getAll()
    authors.value = response.data.results || response.data
  } catch (error) {
    console.error(error)
  }
}

const fetchBooksByAuthor = async () => {
  if (!booksByAuthor.authorId) return
  booksByAuthor.loading = true
  try {
    const response = await reportsApi.booksByAuthor(booksByAuthor.authorId)
    booksByAuthor.data = response.data
  } catch (error) {
    console.error(error)
  } finally {
    booksByAuthor.loading = false
  }
}

const fetchChiefEditors = async () => {
  chiefEditors.loading = true
  try {
    const response = await reportsApi.chiefEditors()
    chiefEditors.data = response.data
  } catch (error) {
    console.error(error)
  } finally {
    chiefEditors.loading = false
  }
}

const fetchEditorsPerBook = async () => {
  editorsPerBook.loading = true
  try {
    const response = await reportsApi.editorsPerBook()
    editorsPerBook.data = response.data
  } catch (error) {
    console.error(error)
  } finally {
    editorsPerBook.loading = false
  }
}

const fetchContractsByMonth = async () => {
  contractsByMonth.loading = true
  try {
    const response = await reportsApi.contractsByMonth(contractsByMonth.year)
    contractsByMonth.data = response.data
  } catch (error) {
    console.error(error)
  } finally {
    contractsByMonth.loading = false
  }
}

const fetchTopManagers = async () => {
  if (!topManagers.startDate || !topManagers.endDate) return
  topManagers.loading = true
  try {
    const response = await reportsApi.topManagers(topManagers.startDate, topManagers.endDate)
    topManagers.data = response.data
  } catch (error) {
    console.error(error)
  } finally {
    topManagers.loading = false
  }
}

const fetchQuarterlyReport = async () => {
  quarterly.loading = true
  try {
    const response = await reportsApi.quarterlyContracts(quarterly.quarter, quarterly.year)
    quarterly.data = response.data
  } catch (error) {
    console.error(error)
  } finally {
    quarterly.loading = false
  }
}

onMounted(() => {
  fetchAuthors()
})
</script>

<style scoped>
.reports-view {
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

