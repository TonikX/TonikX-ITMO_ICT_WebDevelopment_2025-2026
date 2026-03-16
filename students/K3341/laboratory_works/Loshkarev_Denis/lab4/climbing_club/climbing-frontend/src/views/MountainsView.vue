<template>
  <div class="page">
    <v-card class="panel-card" rounded="xl" elevation="8">
      <v-card-title class="py-3 d-flex align-center justify-space-between flex-wrap ga-2">
        <div>
          <div class="text-h5 font-weight-medium">Вершины</div>
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

          <v-select
            v-model="ordering"
            :items="orderingItems"
            item-title="title"
            item-value="value"
            label="Сортировка"
            variant="outlined"
            density="comfortable"
            hide-details
            class="ordering-field"
            :disabled="loading"
            @update:model-value="onOrderingChange"
          />

          <v-btn
            color="black"
            class="text-none"
            size="large"
            @click="openCreateDialog"
          >
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
                <th>Название</th>
                <th style="width: 140px">Высота</th>
                <th style="width: 220px">Страна</th>
                <th style="width: 220px">Район</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="m in mountains" :key="m.id">
                <td class="text-grey-darken-1">{{ m.id }}</td>
                <td class="font-weight-medium">{{ m.name }}</td>
                <td>{{ m.height }} м</td>
                <td>{{ m.country }}</td>
                <td>{{ m.region }}</td>
              </tr>

              <tr v-if="!loading && mountains.length === 0">
                <td colspan="5" class="text-center py-8 text-grey-darken-1">
                  Пусто
                </td>
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
            @update:model-value="fetchMountains"
          />
        </div>
      </v-card-text>
    </v-card>

    <v-dialog v-model="createDialog" max-width="560">
      <v-card class="dialog-card" rounded="xl" elevation="10">
        <v-card-title class="py-3 d-flex align-center justify-space-between">
          <div class="text-h6 font-weight-medium">Добавить вершину</div>
          <v-btn icon="mdi-close" variant="text" @click="createDialog = false" />
        </v-card-title>

        <v-card-text class="pt-2">
          <v-alert
            v-if="createError"
            type="error"
            variant="tonal"
            class="mb-4"
            :text="createError"
          />

          <v-form @submit.prevent="createMountain">
            <v-text-field
              v-model.trim="form.name"
              label="Название"
              variant="outlined"
              density="comfortable"
              :disabled="createLoading"
              class="mb-3"
            />

            <v-text-field
              v-model.number="form.height"
              label="Высота (м)"
              type="number"
              variant="outlined"
              density="comfortable"
              :disabled="createLoading"
              class="mb-3"
            />

            <v-text-field
              v-model.trim="form.country"
              label="Страна"
              variant="outlined"
              density="comfortable"
              :disabled="createLoading"
              class="mb-3"
            />

            <v-text-field
              v-model.trim="form.region"
              label="Район"
              variant="outlined"
              density="comfortable"
              :disabled="createLoading"
            />

            <v-btn
              type="submit"
              block
              color="black"
              class="mt-5 text-none"
              size="large"
              :loading="createLoading"
              :disabled="!canSubmit"
            >
              Сохранить
            </v-btn>

            <v-btn
              block
              variant="text"
              class="mt-2 text-none"
              :disabled="createLoading"
              @click="createDialog = false"
            >
              Отмена
            </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar.show" :timeout="2200" color="grey-darken-4">
      {{ snackbar.text }}
      <template #actions>
        <v-btn variant="text" @click="snackbar.show = false">Ок</v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import api from '../api'

const mountains = ref([])
const loading = ref(false)

const search = ref('')
const ordering = ref('id')

const page = ref(1)
const pageSize = ref(10)
const totalCount = ref(0)

const orderingItems = [
  { title: 'ID', value: 'id' },
  { title: 'Название', value: 'name' },
  { title: 'Высота', value: 'height' },
  { title: 'Страна', value: 'country' },
  { title: 'Район', value: 'region' },
]

const createDialog = ref(false)
const createLoading = ref(false)
const createError = ref('')

const form = reactive({
  name: '',
  height: null,
  country: '',
  region: '',
})

const snackbar = reactive({
  show: false,
  text: '',
})

const totalPages = computed(() => Math.max(1, Math.ceil(totalCount.value / pageSize.value)))

const canSubmit = computed(() => {
  return (
    form.name &&
    form.country &&
    form.region &&
    Number.isFinite(Number(form.height)) &&
    Number(form.height) > 0
  )
})

function resetForm() {
  form.name = ''
  form.height = null
  form.country = ''
  form.region = ''
}

function openCreateDialog() {
  createError.value = ''
  resetForm()
  createDialog.value = true
}

function onOrderingChange() {
  page.value = 1
  fetchMountains()
}

async function fetchMountains() {
  loading.value = true
  try {
    const resp = await api.get('api/mountains/', {
      params: {
        ordering: ordering.value,
        page: page.value,
        search: search.value ? search.value : undefined,
      },
    })

    mountains.value = resp.data?.results || []
    totalCount.value = resp.data?.count ?? mountains.value.length
  } catch (e) {
    console.error(e)
    snackbar.text = 'Не удалось загрузить вершины'
    snackbar.show = true
  } finally {
    loading.value = false
  }
}

let searchTimer = null
watch(search, () => {
  page.value = 1
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    fetchMountains()
  }, 350)
})

async function createMountain() {
  createError.value = ''
  if (!canSubmit.value) return

  createLoading.value = true
  try {
    await api.post('api/mountains/', {
      name: form.name,
      height: Number(form.height),
      country: form.country,
      region: form.region,
    })

    createDialog.value = false
    snackbar.text = 'Вершина добавлена'
    snackbar.show = true

    page.value = 1
    await fetchMountains()
  } catch (e) {
    console.error(e)
    const data = e?.response?.data
    createError.value =
      data && typeof data === 'object'
        ? Object.entries(data)
            .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : String(v)}`)
            .join(' | ')
        : 'Ошибка сохранения'
  } finally {
    createLoading.value = false
  }
}

onMounted(fetchMountains)
</script>
