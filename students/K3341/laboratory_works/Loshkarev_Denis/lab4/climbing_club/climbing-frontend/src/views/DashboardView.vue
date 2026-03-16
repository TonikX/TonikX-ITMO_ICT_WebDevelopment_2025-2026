<template>
  <div class="page">

    <v-row class="mb-4">
      <v-col v-for="s in stats" :key="s.label" cols="12" sm="6" md="3">
        <v-card class="stat-card" rounded="xl" elevation="4">
          <v-card-text class="d-flex align-center ga-4 py-4">
            <v-icon :icon="s.icon" size="38" :color="s.color" />
            <div>
              <div class="stat-value">{{ s.loading ? '—' : s.value }}</div>
              <div class="stat-label">{{ s.label }}</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="7">
        <v-card class="panel-card" rounded="xl" elevation="8" height="100%">
          <v-card-title class="py-3 d-flex align-center justify-space-between">
            <div>
              <div class="text-h6 font-weight-medium">Последние восхождения</div>
              <div class="panel-subtitle">10 последних по дате начала</div>
            </div>
            <v-btn
              variant="text"
              class="text-none"
              size="small"
              :to="{ name: 'climbs' }"
              append-icon="mdi-arrow-right"
            >
              Посмотреть все
            </v-btn>
          </v-card-title>

          <v-card-text class="pt-0">
            <v-progress-linear v-if="loadingClimbs" indeterminate color="black" class="mb-3" />

            <v-table v-if="recentClimbs.length" density="compact" hover>
              <thead>
                <tr>
                  <th>Группа</th>
                  <th>Гора</th>
                  <th style="width: 110px">Дата</th>
                  <th style="width: 80px">Итог</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="c in recentClimbs" :key="c.id">
                  <td class="font-weight-medium">{{ c.group_name }}</td>
                  <td class="text-grey-darken-1">{{ c.mountain_name }}</td>
                  <td class="text-body-2">{{ fmtDate(c.start_actual || c.start_planned) }}</td>
                  <td>
                    <v-chip
                      :color="c.is_group_success ? 'green-darken-1' : 'red-darken-1'"
                      size="x-small"
                      label
                    >
                      {{ c.is_group_success ? 'Успех' : 'Неудача' }}
                    </v-chip>
                  </td>
                </tr>
              </tbody>
            </v-table>

            <div v-else-if="!loadingClimbs" class="empty-text">
              Восхождений ещё нет
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="5">
        <v-row>
          <v-col cols="12">
            <v-card class="panel-card" rounded="xl" elevation="8">
              <v-card-title class="py-3">
                <div class="text-h6 font-weight-medium">Топ вершин</div>
                <div class="panel-subtitle">По числу уникальных альпинистов</div>
              </v-card-title>

              <v-card-text class="pt-0">
                <v-progress-linear v-if="loadingMtnStats" indeterminate color="black" class="mb-3" />

                <template v-if="topMountains.length">
                  <div v-for="(m, i) in topMountains" :key="m.name" class="mountain-row">
                    <div class="d-flex align-center justify-space-between mb-1">
                      <div class="d-flex align-center ga-2">
                        <span class="rank-badge">{{ i + 1 }}</span>
                        <span class="text-body-2 font-weight-medium">{{ m.name }}</span>
                      </div>
                      <span class="text-body-2 text-grey-darken-1">{{ m.climbers_count }} чел.</span>
                    </div>
                    <v-progress-linear
                      :model-value="topMountains[0].climbers_count
                        ? (m.climbers_count / topMountains[0].climbers_count) * 100
                        : 0"
                      color="black"
                      bg-color="grey-lighten-3"
                      rounded
                      height="4"
                    />
                  </div>
                </template>

                <div v-else-if="!loadingMtnStats" class="empty-text">Нет данных</div>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12">
            <v-card class="panel-card" rounded="xl" elevation="8">
              <v-card-title class="py-3">
                <div class="text-h6 font-weight-medium">Без восхождений</div>
                <div class="panel-subtitle">Вершины, куда ещё не ходили</div>
              </v-card-title>

              <v-card-text class="pt-0">
                <v-progress-linear v-if="loadingUnclimbed" indeterminate color="black" class="mb-3" />

                <template v-if="unclimbed.length">
                  <v-chip
                    v-for="m in unclimbed"
                    :key="m.id"
                    size="small"
                    label
                    class="mr-1 mb-1"
                    color="black"
                  >
                    {{ m.name }}
                  </v-chip>
                </template>

                <div v-else-if="!loadingUnclimbed" class="empty-text">
                  Все вершины покорены 
                </div>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12">
            <v-card class="panel-card" rounded="xl" elevation="8">
              <v-card-title class="py-3">
                <div class="text-h6 font-weight-medium">API</div>
                <div class="panel-subtitle">Документация и проверка соединения</div>
              </v-card-title>

              <v-card-text class="pt-0 d-flex align-center ga-3 flex-wrap">
                <v-btn
                  variant="outlined"
                  class="text-none"
                  prepend-icon="mdi-file-document-outline"
                  href="http://localhost:8010/api/docs/"
                  target="_blank"
                >
                  Swagger
                </v-btn>

                <v-btn
                  variant="outlined"
                  class="text-none"
                  prepend-icon="mdi-wifi"
                  :loading="pinging"
                  :color="pingColor"
                  @click="pingApi"
                >
                  {{ pingLabel }}
                </v-btn>
              </v-card-text>
            </v-card>
          </v-col>

        </v-row>
      </v-col>
    </v-row>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
      {{ snackbar.text }}
      <template #actions>
        <v-btn variant="text" @click="snackbar.show = false">Ок</v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '../api'

const stats = reactive([
  { label: 'Альпинистов', value: 0, icon: 'mdi-account-group',  color: 'blue-darken-1',   loading: true },
  { label: 'Вершин',      value: 0, icon: 'mdi-terrain',       color: 'green-darken-1',  loading: true },
  { label: 'Клубов',      value: 0, icon: 'mdi-flag',           color: 'orange-darken-1', loading: true },
  { label: 'Восхождений', value: 0, icon: 'mdi-hiking',         color: 'purple-darken-1', loading: true },
])

async function fetchCounts() {
  const endpoints = [
    { url: 'api/alpinists/', idx: 0 },
    { url: 'api/mountains/', idx: 1 },
    { url: 'api/clubs/',     idx: 2 },
  ]
  for (const { url, idx } of endpoints) {
    try {
      const res = await api.get(url)
      const data = res.data
      stats[idx].value = Array.isArray(data) ? data.length : (data.count ?? 0)
    } catch {
      stats[idx].value = '?'
    } finally {
      stats[idx].loading = false
    }
  }
}

const recentClimbs = ref([])
const loadingClimbs = ref(true)

async function fetchRecentClimbs() {
  loadingClimbs.value = true
  try {
    const res = await api.get('api/climbs/recent/')
    const data = res.data
    recentClimbs.value = Array.isArray(data) ? data : (data.results ?? [])
    stats[3].value = Array.isArray(data) ? data.length : (data.count ?? recentClimbs.value.length)
    stats[3].loading = false
  } catch {
    stats[3].loading = false
  } finally {
    loadingClimbs.value = false
  }
}

const topMountains = ref([])
const loadingMtnStats = ref(true)

async function fetchMountainStats() {
  loadingMtnStats.value = true
  try {
    const res = await api.get('api/query/mountain-stats/')
    const data = res.data
    const items = Array.isArray(data) ? data : (data.results ?? [])
    topMountains.value = items
      .filter(m => m.climbers_count > 0)
      .sort((a, b) => b.climbers_count - a.climbers_count)
      .slice(0, 5)
  } catch (e) {
    console.error(e)
  } finally {
    loadingMtnStats.value = false
  }
}

const unclimbed = ref([])
const loadingUnclimbed = ref(true)

async function fetchUnclimbed() {
  loadingUnclimbed.value = true
  try {
    const res = await api.get('api/query/unclimbed/?page_size=all')
    const data = res.data
    unclimbed.value = Array.isArray(data) ? data : (data.results ?? [])
  } catch (e) {
    console.error(e)
  } finally {
    loadingUnclimbed.value = false
  }
}

const pinging = ref(false)
const pingLabel = ref('Ping API')
const pingColor = ref(undefined)

async function pingApi() {
  pinging.value = true
  pingLabel.value = 'Ping API'
  pingColor.value = undefined
  try {
    await api.get('api/mountains/?page=1')
    pingColor.value = 'green-darken-1'
    pingLabel.value = 'Доступен'
    showSnackbar('Backend отвечает ✓', 'success')
  } catch {
    pingColor.value = 'red-darken-1'
    pingLabel.value = 'Недоступен'
    showSnackbar('Backend не отвечает ✗', 'error')
  } finally {
    pinging.value = false
    setTimeout(() => {
      pingLabel.value = 'Ping API'
      pingColor.value = undefined
    }, 4000)
  }
}

const snackbar = ref({ show: false, text: '', color: 'success' })

function showSnackbar(text, color = 'success') {
  snackbar.value = { show: true, text, color }
}

function fmtDate(dt) {
  if (!dt) return '—'
  return String(dt).slice(0, 10)
}

onMounted(() => {
  fetchCounts()
  fetchRecentClimbs()
  fetchMountainStats()
  fetchUnclimbed()
})
</script>
