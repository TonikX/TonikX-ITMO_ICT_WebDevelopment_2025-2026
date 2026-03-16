<template>
  <div class="page">
    <v-card class="panel-card" rounded="xl" elevation="8">
      <v-card-title class="py-3 d-flex align-center justify-space-between flex-wrap ga-2">
        <div>
          <div class="text-h5 font-weight-medium">Альпклубы</div>
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
        <v-alert
          v-if="loadError"
          type="error"
          variant="tonal"
          class="mb-4"
          :text="loadError"
        />

        <v-progress-linear v-if="loading" indeterminate color="black" class="mb-4" />

        <div class="table-wrap">
          <v-table hover>
            <thead>
              <tr>
                <th style="width: 80px">ID</th>
                <th>Название</th>
                <th style="width: 160px">Страна</th>
                <th style="width: 180px">Город</th>
                <th>Контактное лицо</th>
                <th style="width: 220px">Email</th>
                <th style="width: 160px">Телефон</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="c in clubs" :key="c.id">
                <td class="text-grey-darken-1">{{ c.id }}</td>
                <td class="font-weight-medium">{{ c.name }}</td>
                <td>{{ c.country }}</td>
                <td>{{ c.city }}</td>
                <td>{{ c.contact_person }}</td>
                <td class="text-truncate" style="max-width: 220px">{{ c.email }}</td>
                <td>{{ c.phone }}</td>
              </tr>

              <tr v-if="!loading && clubs.length === 0">
                <td colspan="7" class="text-center py-8 text-grey-darken-1">Пусто</td>
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
            @update:model-value="fetchClubs"
          />
        </div>
      </v-card-text>
    </v-card>

    <v-dialog v-model="createDialog" max-width="560">
      <v-card class="dialog-card" rounded="xl" elevation="10">
        <v-card-title class="py-3 d-flex align-center justify-space-between">
          <div class="text-h6 font-weight-medium">Добавить клуб</div>
          <v-btn icon="mdi-close" variant="text" @click="createDialog = false" />
        </v-card-title>

        <v-card-text class="pt-2">
          <v-alert v-if="createError" type="error" variant="tonal" class="mb-4" :text="createError" />

          <v-form @submit.prevent="submitCreate">
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model.trim="form.name"
                  label="Название"
                  variant="outlined"
                  density="comfortable"
                  :disabled="createLoading"
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model.trim="form.country"
                  label="Страна"
                  variant="outlined"
                  density="comfortable"
                  :disabled="createLoading"
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model.trim="form.city"
                  label="Город"
                  variant="outlined"
                  density="comfortable"
                  :disabled="createLoading"
                />
              </v-col>

              <v-col cols="12">
                <v-text-field
                  v-model.trim="form.contact_person"
                  label="Контактное лицо"
                  variant="outlined"
                  density="comfortable"
                  :disabled="createLoading"
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model.trim="form.email"
                  label="Email"
                  type="email"
                  variant="outlined"
                  density="comfortable"
                  :disabled="createLoading"
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model.trim="form.phone"
                  label="Телефон"
                  variant="outlined"
                  density="comfortable"
                  :disabled="createLoading"
                />
              </v-col>
            </v-row>

            <div class="d-flex ga-3 mt-2">
              <v-btn
                type="submit"
                color="black"
                class="text-none flex-grow-1"
                size="large"
                :loading="createLoading"
                :disabled="!form.name"
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
const loadError = ref('')
const clubs = ref([])
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
    fetchClubs()
  }, 350)
})

async function fetchClubs() {
  loading.value = true
  loadError.value = ''
  try {
    const params = new URLSearchParams({ page: page.value })
    if (search.value) params.set('search', search.value)
    const res = await api.get(`api/clubs/?${params}`)
    const data = res.data
    clubs.value = Array.isArray(data) ? data : (data.results ?? [])
    totalCount.value = Array.isArray(data) ? data.length : (data.count ?? 0)
  } catch (e) {
    loadError.value = 'Ошибка загрузки клубов'
    console.error(e)
  } finally {
    loading.value = false
  }
}

const createDialog = ref(false)
const createLoading = ref(false)
const createError = ref('')

const form = ref({
  name: '', country: '', city: '',
  contact_person: '', email: '', phone: '',
})

function openCreateDialog() {
  form.value = { name: '', country: '', city: '', contact_person: '', email: '', phone: '' }
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
    await api.post('api/clubs/', { ...form.value })
    createDialog.value = false
    showSnackbar('Клуб добавлен', 'success')
    page.value = 1
    await fetchClubs()
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

onMounted(fetchClubs)
</script>
