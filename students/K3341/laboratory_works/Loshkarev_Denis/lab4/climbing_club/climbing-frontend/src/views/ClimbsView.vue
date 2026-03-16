<template>
  <div class="page page--wide">
    <v-card class="panel-card" rounded="xl" elevation="8">
      <v-card-title class="py-3 d-flex align-center justify-space-between flex-wrap ga-2">
        <div>
          <div class="text-h5 font-weight-medium">Восхождения</div>
          <div class="panel-subtitle">Список всех групп</div>
        </div>

        <div class="d-flex align-center ga-2 flex-wrap">
          <v-text-field
            v-model.trim="search"
            label="Поиск по группе / горе"
            variant="outlined"
            density="comfortable"
            hide-details
            clearable
            class="search-field"
          />
          <v-btn color="black" class="text-none" size="large" :to="{ name: 'climbs-create' }">
            + Создать
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
                <th>Группа</th>
                <th>Гора</th>
                <th>Маршрут</th>
                <th style="width:120px">Начало (факт)</th>
                <th style="width:120px">Конец (факт)</th>
                <th style="width:90px">Итог</th>
                <th style="width:80px">Участ.</th>
                <th style="width:60px"></th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="c in climbs"
                :key="c.id"
                class="climb-row"
                @click="openDetail(c)"
              >
                <td class="text-grey-darken-1">{{ c.id }}</td>
                <td class="font-weight-medium">{{ c.group_name }}</td>
                <td>{{ c.mountain_name }}</td>
                <td class="text-body-2 text-grey-darken-1 text-truncate" style="max-width:220px">
                  {{ c.route_details }}
                </td>
                <td class="text-body-2">{{ fmtDate(c.start_actual) }}</td>
                <td class="text-body-2">{{ fmtDate(c.end_actual) }}</td>
                <td>
                  <v-chip
                    :color="c.is_group_success ? 'green-darken-1' : 'red-darken-1'"
                    size="x-small"
                    label
                  >
                    {{ c.is_group_success ? 'Успех' : 'Неудача' }}
                  </v-chip>
                </td>
                <td class="text-center">{{ c.details?.length ?? 0 }}</td>
                <td>
                  <v-btn
                    icon="mdi-eye-outline"
                    variant="text"
                    size="small"
                    @click.stop="openDetail(c)"
                  />
                </td>
              </tr>

              <tr v-if="!loading && climbs.length === 0">
                <td colspan="9" class="text-center py-8 text-grey-darken-1">Пусто</td>
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
            @update:model-value="fetchClimbs"
          />
        </div>
      </v-card-text>
    </v-card>

    <v-dialog v-model="detailDialog" max-width="700" scrollable>
      <v-card class="dialog-card" rounded="xl" elevation="10">
        <v-card-title class="py-3 d-flex align-center justify-space-between">
          <div class="d-flex align-center ga-3">
            <v-icon icon="mdi-hiking" size="22" />
            <span class="text-h6 font-weight-medium">{{ selected?.group_name }}</span>
            <v-chip
              v-if="selected"
              :color="selected.is_group_success ? 'green-darken-1' : 'red-darken-1'"
              size="small"
              label
            >
              {{ selected?.is_group_success ? 'Успех' : 'Неудача' }}
            </v-chip>
          </div>
          <v-btn icon="mdi-close" variant="text" @click="detailDialog = false" />
        </v-card-title>

        <v-divider />

        <v-card-text v-if="selected" class="pt-4">
          <v-row>
            <v-col cols="12" md="6">
              <div class="detail-section-title">Маршрут и гора</div>
              <div class="detail-row">
                <v-icon icon="mdi-terrain" size="16" class="mr-1 text-grey" />
                <span class="detail-label">Гора:</span>
                <span class="detail-value">{{ selected.mountain_name }}</span>
              </div>
              <div class="detail-row">
                <v-icon icon="mdi-map-marker-path" size="16" class="mr-1 text-grey" />
                <span class="detail-label">Маршрут:</span>
                <span class="detail-value">{{ selected.route_details }}</span>
              </div>
            </v-col>

            <v-col cols="12" md="6">
              <div class="detail-section-title">Даты</div>
              <div class="detail-row">
                <v-icon icon="mdi-calendar-arrow-right" size="16" class="mr-1 text-grey" />
                <span class="detail-label">Начало (план):</span>
                <span class="detail-value">{{ fmtDateTime(selected.start_planned) }}</span>
              </div>
              <div class="detail-row">
                <v-icon icon="mdi-calendar-arrow-left" size="16" class="mr-1 text-grey" />
                <span class="detail-label">Конец (план):</span>
                <span class="detail-value">{{ fmtDateTime(selected.end_planned) }}</span>
              </div>
              <div class="detail-row">
                <v-icon icon="mdi-flag-checkered" size="16" class="mr-1 text-grey" />
                <span class="detail-label">Начало (факт):</span>
                <span class="detail-value">{{ fmtDateTime(selected.start_actual) }}</span>
              </div>
              <div class="detail-row">
                <v-icon icon="mdi-flag-checkered" size="16" class="mr-1 text-grey" />
                <span class="detail-label">Конец (факт):</span>
                <span class="detail-value">{{ fmtDateTime(selected.end_actual) }}</span>
              </div>
            </v-col>

            <v-col v-if="selected.group_notes" cols="12">
              <div class="detail-section-title">Пояснения / нештатные ситуации</div>
              <div class="notes-box">{{ selected.group_notes }}</div>
            </v-col>
          </v-row>

          <div class="detail-section-title mt-4">
            Состав группы
            <span class="text-grey-darken-1 text-body-2 font-weight-regular ml-1">
              ({{ selected.details?.length ?? 0 }} чел.)
            </span>
          </div>

          <v-table density="compact" hover v-if="selected.details?.length">
            <thead>
              <tr>
                <th>Альпинист</th>
                <th style="width:130px">Статус</th>
                <th>Детали</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in selected.details" :key="p.alpinist_name">
                <td class="font-weight-medium">{{ p.alpinist_name }}</td>
                <td>
                  <v-chip
                    :color="statusColor(p.status)"
                    size="x-small"
                    label
                  >
                    {{ statusLabel(p.status) }}
                  </v-chip>
                </td>
                <td class="text-body-2 text-grey-darken-1">
                  {{ p.incident_details || '—' }}
                </td>
              </tr>
            </tbody>
          </v-table>

          <div v-else class="empty-text">Участников нет</div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import api from '../api'

const loading = ref(false)
const climbs = ref([])
const totalCount = ref(0)
const page = ref(1)
const PAGE_SIZE = 10
const totalPages = computed(() => Math.ceil(totalCount.value / PAGE_SIZE))

const search = ref('')

let searchTimer = null
watch(search, () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => { page.value = 1; fetchClimbs() }, 350)
})

async function fetchClimbs() {
  loading.value = true
  try {
    const params = new URLSearchParams({ page: page.value })
    if (search.value) params.set('search', search.value)
    const res = await api.get(`api/climbs/?${params}`)
    const data = res.data
    climbs.value = Array.isArray(data) ? data : (data.results ?? [])
    totalCount.value = Array.isArray(data) ? data.length : (data.count ?? 0)
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const detailDialog = ref(false)
const selected = ref(null)

function openDetail(climb) {
  selected.value = climb
  detailDialog.value = true
}

function fmtDate(dt) {
  if (!dt) return '—'
  return String(dt).slice(0, 10)
}

function fmtDateTime(dt) {
  if (!dt) return '—'
  return String(dt).slice(0, 16).replace('T', ' ')
}

const STATUS_LABELS = {
  success: 'Успешно',
  failed:  'Неудача',
  injury:  'Травма',
  missing: 'Пропал',
  fatal:   'Летальный',
  other:   'Другое',
}

const STATUS_COLORS = {
  success: 'green-darken-1',
  failed:  'red-darken-1',
  injury:  'orange-darken-1',
  missing: 'purple-darken-1',
  fatal:   'grey-darken-3',
  other:   'blue-grey',
}

function statusLabel(s) { return STATUS_LABELS[s] ?? s }
function statusColor(s) { return STATUS_COLORS[s] ?? 'grey' }

onMounted(fetchClimbs)
</script>
