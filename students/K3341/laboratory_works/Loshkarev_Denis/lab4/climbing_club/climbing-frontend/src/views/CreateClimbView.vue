<template>
  <div class="page">
    <v-card class="panel-card" rounded="xl" elevation="8">
      <v-card-title class="py-3">
        <div class="text-h5 font-weight-medium">Создать восхождение</div>
      </v-card-title>

      <v-card-text class="pt-2">
        <v-alert v-if="error" type="error" variant="tonal" class="mb-4" :text="error" />
        <v-alert v-if="ok" type="success" variant="tonal" class="mb-4" :text="ok" />

        <v-form @submit.prevent="submit">
          <v-row>
            <v-col cols="12" md="6">
              <v-autocomplete
                v-model="form.route"
                :items="routes"
                item-title="label"
                item-value="id"
                label="Маршрут"
                variant="outlined"
                density="comfortable"
                :loading="loadingRoutes"
                :disabled="loading"
                no-data-text="Нет маршрутов"
                clearable
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model.trim="form.group_name"
                label="Название группы"
                variant="outlined"
                density="comfortable"
                :disabled="loading"
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model="form.start_planned"
                label="Начало (план) — YYYY-MM-DDTHH:MM"
                variant="outlined"
                density="comfortable"
                :disabled="loading"
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model="form.end_planned"
                label="Конец (план) — YYYY-MM-DDTHH:MM"
                variant="outlined"
                density="comfortable"
                :disabled="loading"
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model="form.start_actual"
                label="Начало (факт) — YYYY-MM-DDTHH:MM (опц.)"
                variant="outlined"
                density="comfortable"
                :disabled="loading"
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model="form.end_actual"
                label="Конец (факт) — YYYY-MM-DDTHH:MM (опц.)"
                variant="outlined"
                density="comfortable"
                :disabled="loading"
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-switch
                v-model="form.is_group_success"
                color="black"
                inset
                :disabled="loading"
                label="Успех группы"
              />
            </v-col>

            <v-col cols="12">
              <v-textarea
                v-model.trim="form.group_notes"
                label="Пояснение / нештатные ситуации"
                variant="outlined"
                density="comfortable"
                :disabled="loading"
                rows="3"
              />
            </v-col>
          </v-row>

          <div class="section-title mt-2">Участники</div>

          <div
            v-for="(p, idx) in form.participants_data"
            :key="idx"
            class="participant-row"
          >
            <v-row align="center">
              <v-col cols="12" md="4">
                <v-autocomplete
                  v-model="p.alpinist"
                  :items="alpinists"
                  item-title="name"
                  item-value="id"
                  label="Альпинист"
                  variant="outlined"
                  density="comfortable"
                  :loading="loadingAlpinists"
                  :disabled="loading"
                  no-data-text="Не найдено"
                  clearable
                  auto-select-first
                />
              </v-col>

              <v-col cols="12" md="3">
                <v-select
                  v-model="p.status"
                  :items="statusItems"
                  item-title="title"
                  item-value="value"
                  label="Статус"
                  variant="outlined"
                  density="comfortable"
                  :disabled="loading"
                />
              </v-col>

              <v-col cols="12" md="4">
                <v-text-field
                  v-model.trim="p.incident_details"
                  label="Детали (опц.)"
                  variant="outlined"
                  density="comfortable"
                  :disabled="loading"
                />
              </v-col>

              <v-col cols="12" md="1" class="d-flex justify-center">
                <v-btn
                  icon="mdi-delete-outline"
                  variant="text"
                  color="red-darken-1"
                  @click="removeParticipant(idx)"
                />
              </v-col>
            </v-row>
          </div>

          <v-btn
            variant="outlined"
            class="text-none mt-1 mb-4"
            prepend-icon="mdi-plus"
            @click="addParticipant"
            :disabled="loading"
          >
            Добавить участника
          </v-btn>

          <v-divider class="mb-4" />

          <v-btn
            type="submit"
            block
            color="black"
            class="text-none"
            size="large"
            :loading="loading"
            :disabled="!canSubmit"
          >
            Создать восхождение
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()

const loading = ref(false)
const loadingRoutes = ref(false)
const loadingAlpinists = ref(false)
const error = ref('')
const ok = ref('')

const routes = ref([])
const alpinists = ref([])

const statusItems = [
  { title: 'Успешно', value: 'success' },
  { title: 'Не успешно', value: 'failed' },
  { title: 'Травма', value: 'injury' },
  { title: 'Пропал без вести', value: 'missing' },
  { title: 'Летальный исход', value: 'fatal' },
  { title: 'Другое', value: 'other' },
]

const form = ref({
  route: null,
  group_name: '',
  start_planned: '',
  end_planned: '',
  start_actual: '',
  end_actual: '',
  is_group_success: false,
  group_notes: '',
  participants_data: [],
})

const canSubmit = computed(() =>
  form.value.route &&
  form.value.group_name &&
  form.value.start_planned &&
  form.value.end_planned
)

function addParticipant() {
  form.value.participants_data.push({
    alpinist: null,
    is_success: false,
    status: 'success',
    incident_details: '',
  })
}

function removeParticipant(idx) {
  form.value.participants_data.splice(idx, 1)
}

async function fetchRoutes() {
  loadingRoutes.value = true
  try {
    const res = await api.get('api/routes/?page_size=all')
    const data = res.data
    const items = Array.isArray(data) ? data : (data.results ?? [])
    routes.value = items.map(r => ({
      ...r,
      label: `${r.mountain_name} — ${r.description}`,
    }))
  } catch (e) {
    console.error('Не удалось загрузить маршруты', e)
  } finally {
    loadingRoutes.value = false
  }
}

async function fetchAlpinists() {
  loadingAlpinists.value = true
  try {
    const res = await api.get('api/alpinists/?page_size=all')
    const data = res.data
    alpinists.value = Array.isArray(data) ? data : (data.results ?? [])
  } catch (e) {
    console.error('Не удалось загрузить альпинистов', e)
  } finally {
    loadingAlpinists.value = false
  }
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

async function submit() {
  error.value = ''
  ok.value = ''
  loading.value = true

  const payload = {
    route: form.value.route,
    group_name: form.value.group_name,
    start_planned: form.value.start_planned,
    end_planned: form.value.end_planned,
    start_actual: form.value.start_actual || null,
    end_actual: form.value.end_actual || null,
    is_group_success: form.value.is_group_success,
    group_notes: form.value.group_notes,
    participants_data: form.value.participants_data.filter(p => p.alpinist),
  }

  try {
    await api.post('api/climbs/create/', payload)
    router.push({ name: 'climbs' })
  } catch (e) {
    error.value = formatErr(e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRoutes()
  fetchAlpinists()
})
</script>
