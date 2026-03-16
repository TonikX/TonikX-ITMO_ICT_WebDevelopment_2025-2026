<template>
  <div class="page">
    <v-card class="panel-card" rounded="xl" elevation="8">
      <v-card-title class="py-3 d-flex align-center justify-space-between flex-wrap ga-2">
        <div>
          <div class="text-h5 font-weight-medium">Альпинисты</div>
          <div class="panel-subtitle">Справочник</div>
        </div>

        <div class="d-flex align-center ga-2 flex-wrap">
          <v-text-field
            v-model.trim="search"
            label="Поиск"
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
                <th style="width: 80px">ID</th>
                <th>ФИО</th>
                <th>Адрес</th>
                <th>Клубы</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="a in alpinists" :key="a.id">
                <td class="text-grey-darken-1">{{ a.id }}</td>
                <td class="font-weight-medium">{{ a.name }}</td>
                <td class="text-truncate" style="max-width: 400px">{{ a.address }}</td>
                <td>
                  <template v-if="a.club_names && a.club_names.length">
                    <v-chip
                      v-for="club in a.club_names"
                      :key="club"
                      size="small"
                      label
                      class="mr-1"
                    >{{ club }}</v-chip>
                  </template>
                  <span v-else class="text-grey-darken-1">—</span>
                </td>
              </tr>

              <tr v-if="!loading && alpinists.length === 0">
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
            @update:model-value="fetchAlpinists"
          />
        </div>
      </v-card-text>
    </v-card>

    <v-dialog v-model="createDialog" max-width="560">
      <v-card class="dialog-card" rounded="xl" elevation="10">
        <v-card-title class="py-3 d-flex align-center justify-space-between">
          <div class="text-h6 font-weight-medium">Добавить альпиниста</div>
          <v-btn icon="mdi-close" variant="text" @click="createDialog = false" />
        </v-card-title>

        <v-card-text class="pt-2">
          <v-alert v-if="createError" type="error" variant="tonal" class="mb-4" :text="createError" />

          <v-form @submit.prevent="submitCreate">
            <v-text-field
              v-model.trim="form.name"
              label="ФИО"
              variant="outlined"
              density="comfortable"
              :disabled="createLoading"
              class="mb-3"
            />

            <v-text-field
              v-model.trim="form.address"
              label="Адрес"
              variant="outlined"
              density="comfortable"
              :disabled="createLoading"
              class="mb-3"
            />

            <v-select
              v-model="form.clubs"
              :items="clubsList"
              item-title="name"
              item-value="id"
              label="Клубы (необязательно)"
              variant="outlined"
              density="comfortable"
              :loading="loadingClubs"
              :disabled="createLoading"
              multiple
              chips
              closable-chips
              no-data-text="Нет клубов"
              class="mb-3"
            />

            <div class="d-flex ga-3 mt-2">
              <v-btn
                type="submit"
                color="black"
                class="text-none flex-grow-1"
                size="large"
                :loading="createLoading"
                :disabled="!form.name || !form.address"
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
const alpinists = ref([])
const totalCount = ref(0)
const page = ref(1)
const PAGE_SIZE = 10

const totalPages = computed(() => Math.ceil(totalCount.value / PAGE_SIZE))

const search = ref('')

let searchTimer = null
watch(search, () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    page.value = 1
    fetchAlpinists()
  }, 350)
})

async function fetchAlpinists() {
  loading.value = true
  try {
    const params = new URLSearchParams({ page: page.value })
    if (search.value) params.set('search', search.value)
    const res = await api.get(`api/alpinists/?${params}`)
    const data = res.data
    alpinists.value = Array.isArray(data) ? data : (data.results ?? [])
    totalCount.value = Array.isArray(data) ? data.length : (data.count ?? 0)
  } catch (e) {
    console.error('Ошибка загрузки альпинистов', e)
  } finally {
    loading.value = false
  }
}

const clubsList = ref([])
const loadingClubs = ref(false)

async function fetchClubs() {
  loadingClubs.value = true
  try {
    const res = await api.get('api/clubs/?page_size=all')
    const data = res.data
    clubsList.value = Array.isArray(data) ? data : (data.results ?? [])
  } catch (e) {
    console.error('Ошибка загрузки клубов', e)
  } finally {
    loadingClubs.value = false
  }
}

const createDialog = ref(false)
const createLoading = ref(false)
const createError = ref('')

const form = ref({ name: '', address: '', clubs: [] })

function openCreateDialog() {
  form.value = { name: '', address: '', clubs: [] }
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
    await api.post('api/alpinists/', {
      name: form.value.name,
      address: form.value.address,
      clubs: form.value.clubs, 
    })
    createDialog.value = false
    showSnackbar('Альпинист добавлен', 'success')
    page.value = 1
    await fetchAlpinists()
  } catch (e) {
    createError.value = formatErr(e)
  } finally {
    createLoading.value = false
  }
}

const snackbar = ref({ show: false, text: '', color: 'success' })

function showSnackbar(text, color = 'success') {
  snackbar.value = { show: true, text, color }
}

onMounted(() => {
  fetchAlpinists()
  fetchClubs()
})
</script>
