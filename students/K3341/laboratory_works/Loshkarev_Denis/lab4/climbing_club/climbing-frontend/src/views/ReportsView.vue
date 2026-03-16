<template>
  <div class="page">
    <v-card class="panel-card" rounded="xl" elevation="8">
      <v-card-title class="py-3">
        <div class="text-h5 font-weight-medium">Отчёты и запросы</div>
        <div class="panel-subtitle">Аналитика по восхождениям</div>
      </v-card-title>

      <v-card-text class="pt-1">
        <v-tabs v-model="tab" color="black" align-tabs="start">
          <v-tab value="alpinists-date">По датам</v-tab>
          <v-tab value="climbs-period">Восхождения</v-tab>
          <v-tab value="mountain-stats">Статистика гор</v-tab>
          <v-tab value="unclimbed">Без восхождений</v-tab>
          <v-tab value="alp-mountain">Альпинист × гора</v-tab>
          <v-tab value="final-report">Итоговый отчёт</v-tab>
        </v-tabs>

        <v-divider class="mb-4" />

        <v-tabs-window v-model="tab">

          <v-tabs-window-item value="alpinists-date">
            <div class="report-desc">Список альпинистов, совершавших восхождения в заданный период.</div>
            <v-row class="mb-3">
              <v-col cols="12" sm="4">
                <v-text-field v-model="dateRange.start" label="Дата начала (YYYY-MM-DD)"
                  variant="outlined" density="comfortable" hide-details />
              </v-col>
              <v-col cols="12" sm="4">
                <v-text-field v-model="dateRange.end" label="Дата конца (YYYY-MM-DD)"
                  variant="outlined" density="comfortable" hide-details />
              </v-col>
              <v-col cols="12" sm="4" class="d-flex align-center">
                <v-btn color="black" class="text-none" size="large"
                  :loading="reports.alpinistsByDate.loading"
                  @click="fetchAlpinistsByDate">
                  Показать
                </v-btn>
              </v-col>
            </v-row>

            <v-alert v-if="reports.alpinistsByDate.error" type="error" variant="tonal"
              class="mb-3" :text="reports.alpinistsByDate.error" />

            <v-table v-if="reports.alpinistsByDate.data.length" hover>
              <thead>
                <tr>
                  <th style="width:80px">ID</th>
                  <th>ФИО</th>
                  <th>Адрес</th>
                  <th>Клуб</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="a in reports.alpinistsByDate.data" :key="a.id">
                  <td class="text-grey-darken-1">{{ a.id }}</td>
                  <td class="font-weight-medium">{{ a.name }}</td>
                  <td>{{ a.address }}</td>
                  <td>{{ a.club_name || '—' }}</td>
                </tr>
              </tbody>
            </v-table>
            <div v-else-if="reports.alpinistsByDate.fetched && !reports.alpinistsByDate.loading"
              class="empty-text">Нет данных за этот период</div>
          </v-tabs-window-item>

          <v-tabs-window-item value="climbs-period">
            <div class="report-desc">Список восхождений (групп), которые проходили в заданный период.</div>
            <v-row class="mb-3">
              <v-col cols="12" sm="4">
                <v-text-field v-model="dateRange.start" label="Дата начала (YYYY-MM-DD)"
                  variant="outlined" density="comfortable" hide-details />
              </v-col>
              <v-col cols="12" sm="4">
                <v-text-field v-model="dateRange.end" label="Дата конца (YYYY-MM-DD)"
                  variant="outlined" density="comfortable" hide-details />
              </v-col>
              <v-col cols="12" sm="4" class="d-flex align-center">
                <v-btn color="black" class="text-none" size="large"
                  :loading="reports.climbsByPeriod.loading"
                  @click="fetchClimbsByPeriod">
                  Показать
                </v-btn>
              </v-col>
            </v-row>

            <v-alert v-if="reports.climbsByPeriod.error" type="error" variant="tonal"
              class="mb-3" :text="reports.climbsByPeriod.error" />

            <v-table v-if="reports.climbsByPeriod.data.length" hover>
              <thead>
                <tr>
                  <th>Группа</th>
                  <th>Гора</th>
                  <th>Маршрут</th>
                  <th>Начало (факт)</th>
                  <th>Конец (факт)</th>
                  <th>Успех</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="c in reports.climbsByPeriod.data" :key="c.id">
                  <td class="font-weight-medium">{{ c.group_name }}</td>
                  <td>{{ c.mountain_name }}</td>
                  <td class="text-grey-darken-1 text-body-2">{{ c.route_details }}</td>
                  <td>{{ c.start_actual ? fmtDate(c.start_actual) : '—' }}</td>
                  <td>{{ c.end_actual ? fmtDate(c.end_actual) : '—' }}</td>
                  <td>
                    <v-chip :color="c.is_group_success ? 'green' : 'red'" size="small" label>
                      {{ c.is_group_success ? 'Да' : 'Нет' }}
                    </v-chip>
                  </td>
                </tr>
              </tbody>
            </v-table>
            <div v-else-if="reports.climbsByPeriod.fetched && !reports.climbsByPeriod.loading"
              class="empty-text">Нет данных за этот период</div>
          </v-tabs-window-item>

          <v-tabs-window-item value="mountain-stats">
            <div class="report-desc">Сколько уникальных альпинистов побывало на каждой горе.</div>
            <v-btn color="black" class="text-none mb-4" size="large"
              :loading="reports.mountainStats.loading"
              @click="fetchMountainStats">
              Загрузить
            </v-btn>

            <v-alert v-if="reports.mountainStats.error" type="error" variant="tonal"
              class="mb-3" :text="reports.mountainStats.error" />

            <v-table v-if="reports.mountainStats.data.length" hover>
              <thead>
                <tr>
                  <th>Гора</th>
                  <th style="width:180px">Кол-во альпинистов</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="s in reports.mountainStats.data" :key="s.name">
                  <td class="font-weight-medium">{{ s.name }}</td>
                  <td>{{ s.climbers_count }}</td>
                </tr>
              </tbody>
            </v-table>
            <div v-else-if="reports.mountainStats.fetched && !reports.mountainStats.loading"
              class="empty-text">Нет данных</div>
          </v-tabs-window-item>

          <v-tabs-window-item value="unclimbed">
            <div class="report-desc">Вершины, на которых ещё не было ни одного восхождения.</div>
            <v-btn color="black" class="text-none mb-4" size="large"
              :loading="reports.unclimbed.loading"
              @click="fetchUnclimbed">
              Загрузить
            </v-btn>

            <v-alert v-if="reports.unclimbed.error" type="error" variant="tonal"
              class="mb-3" :text="reports.unclimbed.error" />

            <v-table v-if="reports.unclimbed.data.length" hover>
              <thead>
                <tr>
                  <th>Название</th>
                  <th style="width:140px">Высота</th>
                  <th>Страна</th>
                  <th>Район</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="m in reports.unclimbed.data" :key="m.id">
                  <td class="font-weight-medium">{{ m.name }}</td>
                  <td>{{ m.height }} м</td>
                  <td>{{ m.country }}</td>
                  <td>{{ m.region }}</td>
                </tr>
              </tbody>
            </v-table>
            <div v-else-if="reports.unclimbed.fetched && !reports.unclimbed.loading"
              class="empty-text">Нет данных (все горы имеют восхождения)</div>
          </v-tabs-window-item>

          <v-tabs-window-item value="alp-mountain">
            <div class="report-desc">Количество восхождений каждого альпиниста на каждую гору.</div>
            <v-btn color="black" class="text-none mb-4" size="large"
              :loading="reports.alpMountain.loading"
              @click="fetchAlpMountain">
              Загрузить
            </v-btn>

            <v-alert v-if="reports.alpMountain.error" type="error" variant="tonal"
              class="mb-3" :text="reports.alpMountain.error" />

            <v-table v-if="reports.alpMountain.data.length" hover>
              <thead>
                <tr>
                  <th>Альпинист</th>
                  <th>Гора</th>
                  <th style="width:140px">Восхождений</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(s, i) in reports.alpMountain.data" :key="i">
                  <td class="font-weight-medium">{{ s.alpinist__name }}</td>
                  <td>{{ s.climb__route__mountain__name }}</td>
                  <td>{{ s.count }}</td>
                </tr>
              </tbody>
            </v-table>
            <div v-else-if="reports.alpMountain.fetched && !reports.alpMountain.loading"
              class="empty-text">Нет данных</div>
          </v-tabs-window-item>

          <v-tabs-window-item value="final-report">
            <div class="report-desc">Для каждой горы — список групп за период + участники. Grand total.</div>
            <v-row class="mb-3">
              <v-col cols="12" sm="4">
                <v-text-field v-model="dateRange.start" label="Дата начала (YYYY-MM-DD)"
                  variant="outlined" density="comfortable" hide-details />
              </v-col>
              <v-col cols="12" sm="4">
                <v-text-field v-model="dateRange.end" label="Дата конца (YYYY-MM-DD)"
                  variant="outlined" density="comfortable" hide-details />
              </v-col>
              <v-col cols="12" sm="4" class="d-flex align-center">
                <v-btn color="black" class="text-none" size="large"
                  :loading="reports.finalReport.loading"
                  @click="fetchFinalReport">
                  Показать
                </v-btn>
              </v-col>
            </v-row>

            <v-alert v-if="reports.finalReport.error" type="error" variant="tonal"
              class="mb-3" :text="reports.finalReport.error" />

            <template v-if="reports.finalReport.data">
              <div
                v-for="mtn in reports.finalReport.data.mountains"
                :key="mtn.mountain"
                class="mb-4"
              >
                <div class="report-mountain-title">
                  {{ mtn.mountain }}
                  <span class="text-grey-darken-1 text-body-2 ml-1">({{ mtn.height }} м)</span>
                </div>
                <v-table density="compact" hover>
                  <thead>
                    <tr>
                      <th>Группа</th>
                      <th>Дата</th>
                      <th style="width:160px">Участников</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="g in mtn.groups" :key="g.group_name + g.date">
                      <td class="font-weight-medium">{{ g.group_name }}</td>
                      <td>{{ g.date }}</td>
                      <td>{{ g.members_count }}</td>
                    </tr>
                  </tbody>
                </v-table>
              </div>

              <v-divider class="my-3" />
              <div class="grand-total">
                Итого участников за период:
                <b>{{ reports.finalReport.data.grand_total_participants }}</b>
              </div>

              <div v-if="!reports.finalReport.data.mountains.length" class="empty-text">
                Нет данных за этот период
              </div>
            </template>
          </v-tabs-window-item>

        </v-tabs-window>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'

const tab = ref('alpinists-date')

const dateRange = ref({ start: '', end: '' })

function makeReport() {
  return { data: [], error: '', loading: false, fetched: false }
}

const reports = ref({
  alpinistsByDate: makeReport(),
  climbsByPeriod: makeReport(),
  mountainStats: makeReport(),
  unclimbed: makeReport(),
  alpMountain: makeReport(),
  finalReport: { data: null, error: '', loading: false, fetched: false },
})

function fmtDate(dt) {
  return dt ? String(dt).slice(0, 16).replace('T', ' ') : '—'
}

function getDateParams() {
  return `?start=${dateRange.value.start}&end=${dateRange.value.end}`
}

async function fetchReport(key, url, transform) {
  const r = reports.value[key]
  r.loading = true
  r.error = ''
  r.fetched = false
  try {
    const res = await api.get(url)
    const raw = res.data
    r.data = transform ? transform(raw) : (Array.isArray(raw) ? raw : (raw.results ?? []))
    r.fetched = true
  } catch (e) {
    r.error = e?.response?.data?.error || 'Ошибка запроса'
    r.fetched = true
  } finally {
    r.loading = false
  }
}

async function fetchAlpinistsByDate() {
  await fetchReport('alpinistsByDate', `api/query/alpinists-by-date/${getDateParams()}`)
}

async function fetchClimbsByPeriod() {
  await fetchReport('climbsByPeriod', `api/query/climbs-by-period/${getDateParams()}`)
}

async function fetchMountainStats() {
  await fetchReport('mountainStats', 'api/query/mountain-stats/')
}

async function fetchUnclimbed() {
  await fetchReport('unclimbed', 'api/query/unclimbed/')
}

async function fetchAlpMountain() {
  await fetchReport('alpMountain', 'api/query/alpinist-mountain-stats/')
}

async function fetchFinalReport() {
  const r = reports.value.finalReport
  r.loading = true
  r.error = ''
  r.fetched = false
  r.data = null
  try {
    const res = await api.get(`api/query/final-report/${getDateParams()}`)
    r.data = res.data
    r.fetched = true
  } catch (e) {
    r.error = e?.response?.data?.error || 'Ошибка запроса'
    r.fetched = true
  } finally {
    r.loading = false
  }
}
</script>
