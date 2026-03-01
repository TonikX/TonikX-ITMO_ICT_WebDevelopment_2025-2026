<template>
  <div class="page">
    <v-card class="panel-card" rounded="xl" elevation="8">
      <v-card-title class="py-3 d-flex align-center justify-space-between flex-wrap ga-2">
        <div>
          <div class="text-h5 font-weight-medium">Маршруты</div>
          <div class="panel-subtitle">Справочник</div>
        </div>

        <div class="d-flex align-center ga-2 flex-wrap">
          <v-text-field
            v-model.trim="search"
            label="Поиск по горе / описанию"
            variant="outlined"
            density="comfortable"
            hide-details
            clearable
            class="search-field"
          />
          <v-btn color="black" class="text-none" size="large" @click="openCreateDialog">
            Добавить
          </v-btn>
        </div>
      </v-card-title>

      <v-card-text class="pt-2">
        <v-progress-linear v-if="loading" indeterminate color="black" class="mb-4" />

        <div class="table-wrap">
          <v-table hover>
            <thead>
              <tr>
                <th style="width:60px">ID</th>
                <th style="width:200px">Гора</th>
                <th>Описание</th>
                <th style="width:180px">Длительность (план)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="r in routes" :key="r.id">
                <td class="text-grey-darken-1">{{ r.id }}</td>
                <td class="font-weight-medium">{{ r.mountain_name }}</td>
                <td>{{ r.description }}</td>
                <td>{{ fmtDuration(r.expected_duration) }}</td>
              </tr>
              <tr v-if="!loading && routes.length === 0">
                <td colspan="4" class="text-center py-8 text-grey-darken-1">Пусто</td>
              </tr>
            </tbody>
          </v-table>
        </div>

        <div class="d-flex flex-wrap align-center justify-space-between mt-4 ga-2">
          <div class="text-body-2 text-grey-darken-1">
            Всего: <b>{{ totalCount }}</b>
            <span v-if="totalPages > 1"> • Страница {{ page }} из {{ totalPages }}</span>
          </div>
          <v-pagination
            v-if="totalPages > 1"
            v-model="page"
            :length="totalPages"
            :total-visible="7"
            density="comfortable"
            @update:model-value="fetchRoutes"
          />
        </div>
      </v-card-text>
    </v-card>

    <v-dialog v-model="createDialog" max-width="560">
      <v-card class="dialog-card" rounded="xl" elevation="10">
        <v-card-title class="py-3 d-flex align-center justify-space-between">
          <div class="text-h6 font-weight-medium">Добавить маршрут</div>
          <v-btn icon="mdi-close" variant="text" @click="createDialog = false" />
        </v-card-title>

        <v-card-text class="pt-2">
          <v-alert v-if="createError" type="error" variant="tonal" class="mb-4" :text="createError" />

          <v-form @submit.prevent="submitCreate">
            <v-autocomplete
              v-model="form.mountain"
              :items="mountains"
              item-title="name"
              item-value="id"
              label="Гора"
              variant="outlined"
              density="comfortable"
              :loading="loadingMountains"
              :disabled="createLoading"
              no-data-text="Нет вершин"
              clearable
              auto-select-first
              class="mb-3"
            />

            <v-textarea
              v-model.trim="form.description"
              label="Описание маршрута"
              variant="outlined"
              density="comfortable"
              :disabled="createLoading"
              rows="3"
              class="mb-3"
            />

            <v-text-field
              v-model.trim="form.expected_duration"
              label="Длительность — формат ЧЧ:ММ:СС"
              variant="outlined"
              density="comfortable"
              :disabled="createLoading"
              class="mb-3"
              persistent-hint
            />

            <div class="d-flex ga-3 mt-4">
              <v-btn
                type="submit"
                color="black"
                class="text-none flex-grow-1"
                size="large"
                :loading="createLoading"
                :disabled="!form.mountain || !form.description || !form.expected_duration"
              >
                Сохранить
              </v-btn>
              <v-btn
                variant="outlined"
                class="text-none"
                size="large"
                :disabled="createLoading"
                @click="createDialog = false"
              >
                Отмена
              </v-btn>
            </div>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
      {{ snackbar.text }}
      <template #actions>
        <v-btn variant="text" @click="snackbar.show = false">Ок</v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import api from '../api'

const loading = ref(false)
const routes = ref([])
const totalCount = ref(0)
const page = ref(1)
const PAGE_SIZE = 10
const totalPages = computed(() => Math.ceil(totalCount.value / PAGE_SIZE))

const search = ref('')

let searchTimer = null
watch(search, () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => { page.value = 1; fetchRoutes() }, 350)
})

async function fetchRoutes() {
  loading.value = true
  try {
    const params = new URLSearchParams({ page: page.value })
    if (search.value) params.set('search', search.value)
    const res = await api.get(`api/routes/?${params}`)
    const data = res.data
    routes.value = Array.isArray(data) ? data : (data.results ?? [])
    totalCount.value = Array.isArray(data) ? data.length : (data.count ?? 0)
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const mountains = ref([])
const loadingMountains = ref(false)

async function fetchMountains() {
  loadingMountains.value = true
  try {
    const res = await api.get('api/mountains/?page_size=all')
    const data = res.data
    mountains.value = Array.isArray(data) ? data : (data.results ?? [])
  } catch (e) {
    console.error(e)
  } finally {
    loadingMountains.value = false
  }
}

const createDialog = ref(false)
const createLoading = ref(false)
const createError = ref('')

const form = ref({ mountain: null, description: '', expected_duration: '' })

function openCreateDialog() {
  form.value = { mountain: null, description: '', expected_duration: '' }
  createError.value = ''
  createDialog.value = true
}

function formatErr(e) {
  const d = e?.response?.data
  if (!d) return 'Ошибка запроса'
  if (typeof d === 'string') return d
  if (typeof d === 'object') {
    return Object.entries(d)
      .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : String(v)}`)
      .join(' | ')
  }
  return 'Ошибка'
}

async function submitCreate() {
  createError.value = ''
  createLoading.value = true
  try {
    await api.post('api/routes/', {
      mountain: form.value.mountain,
      description: form.value.description,
      expected_duration: form.value.expected_duration,
    })
    createDialog.value = false
    showSnackbar('Маршрут добавлен', 'success')
    page.value = 1
    await fetchRoutes()
  } catch (e) {
    createError.value = formatErr(e)
  } finally {
    createLoading.value = false
  }
}

function fmtDuration(d) {
  // Django возвращает длительность как строку
  if (!d) return '—'
  const str = String(d)
  const dayMatch = str.match(/(\d+)\s+day[s]?,\s+(\d+):(\d+)/)
  if (dayMatch) {
    const days = parseInt(dayMatch[1])
    const hours = parseInt(dayMatch[2])
    const totalHours = days * 24 + hours
    return `${totalHours} ч ${dayMatch[3]} мин`
  }
  const parts = str.split(':')
  if (parts.length >= 2) {
    const h = parseInt(parts[0])
    const m = parseInt(parts[1])
    if (m === 0) return `${h} ч`
    return `${h} ч ${m} мин`
  }
  return str
}

const snackbar = ref({ show: false, text: '', color: 'success' })
function showSnackbar(text, color = 'success') {
  snackbar.value = { show: true, text, color }
}

onMounted(() => {
  fetchRoutes()
  fetchMountains()
})
</script>