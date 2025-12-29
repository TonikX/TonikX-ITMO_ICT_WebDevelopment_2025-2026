<template>
  <div>
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card class="pa-6">
          <v-card-title class="text-h4 mb-2">
            Охранные компании
          </v-card-title>
          <v-card-subtitle class="text-body-1">
            Найдите подходящую охранную компанию для ваших нужд
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>

    <!-- Поиск и фильтры -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="8">
                <v-text-field
                    v-model="search"
                    label="Поиск компаний"
                    placeholder="Введите название или описание..."
                    prepend-inner-icon="mdi-magnify"
                    clearable
                    @input="debouncedSearch"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-select
                    v-model="sortBy"
                    :items="sortOptions"
                    label="Сортировать по"
                    @update:model-value="fetchCompanies"
                ></v-select>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Состояние загрузки -->
    <v-row v-if="companiesStore.isLoading">
      <v-col cols="12" class="text-center">
        <v-progress-circular
            indeterminate
            color="primary"
            size="64"
        ></v-progress-circular>
        <p class="mt-4">Загрузка компаний...</p>
      </v-col>
    </v-row>

    <!-- Ошибка -->
    <v-row v-else-if="companiesStore.error">
      <v-col cols="12">
        <v-alert type="error" @close="companiesStore.error = null" closable>
          {{ companiesStore.error }}
        </v-alert>
      </v-col>
    </v-row>

    <!-- Список компаний -->
    <v-row v-else>
      <v-col
          v-for="company in companiesStore.companies"
          :key="company.id"
          cols="12"
          md="6"
          lg="4"
      >
        <v-card height="100%" @click="goToCompany(company.id)">
          <!-- Логотип компании или заглушка -->
          <div class="company-image-container">
            <v-img
                v-if="company.logo && isValidLogo(company.logo)"
                :src="company.logo"
                height="200"
                cover
                class="company-logo"
            >
              <template v-slot:placeholder>
                <div class="logo-placeholder">
                  <v-icon size="64" color="grey-lighten-1">mdi-office-building</v-icon>
                </div>
              </template>
            </v-img>
            <div v-else class="no-logo-placeholder">
              <v-icon size="64" color="grey-lighten-1">mdi-office-building</v-icon>
              <div class="text-caption mt-2">Нет логотипа</div>
            </div>
          </div>

          <v-card-title class="text-h6">
            {{ company.name }}
          </v-card-title>

          <v-card-subtitle>
            <v-chip
                v-if="company.avg_rating"
                color="amber"
                text-color="white"
                size="small"
                class="mr-2"
            >
              <v-icon start icon="mdi-star"></v-icon>
              {{ company.avg_rating.toFixed(1) }}
            </v-chip>
            <v-chip
                color="primary"
                variant="outlined"
                size="small"
            >
              <v-icon start icon="mdi-tools"></v-icon>
              {{ company.services_count || 0 }} услуг
            </v-chip>
          </v-card-subtitle>

          <v-card-text>
            <p class="text-body-2 line-clamp-3">
              {{ company.description || 'Нет описания' }}
            </p>

            <div v-if="company.website" class="mt-2">
              <v-icon icon="mdi-web" size="small"></v-icon>
              <a :href="company.website" target="_blank" class="ml-1" @click.stop>
                {{ formatWebsite(company.website) }}
              </a>
            </div>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" variant="text" @click.stop="goToCompany(company.id)">
              Подробнее
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <!-- Сообщение если компаний нет -->
      <v-col v-if="companiesStore.companies.length === 0" cols="12">
        <v-alert type="info">
          Компании не найдены. Попробуйте изменить параметры поиска.
        </v-alert>
      </v-col>
    </v-row>

    <!-- Пагинация -->
    <v-row v-if="companiesStore.totalPages > 1">
      <v-col cols="12" class="text-center">
        <v-pagination
            v-model="companiesStore.currentPage"
            :length="companiesStore.totalPages"
            @update:model-value="changePage"
        ></v-pagination>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCompaniesStore } from '@/stores/companies'
import { useRouter } from 'vue-router'

const companiesStore = useCompaniesStore()
const router = useRouter()

const search = ref('')
const sortBy = ref('-created_at')
const searchTimeout = ref(null)

const sortOptions = [
  { title: 'По дате (новые)', value: '-created_at' },
  { title: 'По дате (старые)', value: 'created_at' },
  { title: 'По названию (А-Я)', value: 'name' },
  { title: 'По названию (Я-А)', value: '-name' },
  { title: 'По рейтингу (высокий)', value: '-avg_rating' },
  { title: 'По рейтингу (низкий)', value: 'avg_rating' }
]

const isValidLogo = (logoUrl) => {
  if (!logoUrl) return false

  const invalidPatterns = [
    'via.placeholder.com',
    'example.com',
    'string',
    'test',
    'localhost'
  ]

  return !invalidPatterns.some(pattern =>
      logoUrl.toLowerCase().includes(pattern)
  )
}

// Форматирование URL сайта
const formatWebsite = (website) => {
  if (!website) return ''

  // Убираем протокол для отображения
  return website.replace(/^https?:\/\//, '')
}

const fetchCompanies = () => {
  const params = {
    search: search.value,
    ordering: sortBy.value
  }
  companiesStore.fetchCompanies(params)
}

const debouncedSearch = () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }
  searchTimeout.value = setTimeout(fetchCompanies, 500)
}

const changePage = (page) => {
  fetchCompanies()
}

const goToCompany = (companyId) => {
  router.push(`/companies/${companyId}`)
}

onMounted(() => {
  fetchCompanies()
})
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.v-card {
  cursor: pointer;
  transition: transform 0.2s;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.v-card:hover {
  transform: translateY(-4px);
}

.company-image-container {
  height: 200px;
  width: 100%;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.company-logo {
  width: 100%;
  height: 100%;
}

.no-logo-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
  color: #9e9e9e;
}

.logo-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
  background-color: #f5f5f5;
}

.v-card-content {
  flex-grow: 1;
}

a {
  text-decoration: none;
  color: inherit;
}

a:hover {
  text-decoration: underline;
  color: #1976D2;
}
</style>