<template>
  <v-card>
    <v-card-title class="text-h6">Запросы / отчёты</v-card-title>
    <v-card-text>
      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">{{ error }}</v-alert>

      <v-row>
        <v-col cols="12" md="6">
          <v-card variant="outlined">
            <v-card-title class="text-subtitle-1">Запрос №4: самолёты в ремонте</v-card-title>
            <v-card-text>
              <v-btn color="primary" variant="tonal" @click="getInRepair" :loading="loading.inRepair">
                Получить
              </v-btn>
              <div class="mt-3" v-if="inRepair">
                Количество самолётов в ремонте: <b>{{ inRepair.in_repair_count }}</b>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="6">
          <v-card variant="outlined">
            <v-card-title class="text-subtitle-1">Запрос №5: работники компании</v-card-title>
            <v-card-text>
              <v-select
                v-model="companyId"
                :items="companies"
                item-title="name"
                item-value="id"
                label="Компания"
                variant="outlined"
                density="compact"
              />
              <v-btn
                class="mt-2"
                color="primary"
                variant="tonal"
                @click="getEmployeesCount"
                :loading="loading.empCount"
                :disabled="!companyId"
              >
                Получить
              </v-btn>
              <div class="mt-3" v-if="employeesCount">
                Всего: <b>{{ employeesCount.total_employees }}</b>,
                активных: <b>{{ employeesCount.active_employees }}</b>,
                неактивных: <b>{{ employeesCount.inactive_employees }}</b>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12">
          <v-card variant="outlined">
            <v-card-title class="text-subtitle-1">Отчёт: борта компании (aircrafts_by_type)</v-card-title>
            <v-card-text>
              <v-select
                v-model="companyId2"
                :items="companies"
                item-title="name"
                item-value="id"
                label="Компания"
                variant="outlined"
                density="compact"
              />
              <v-btn
                class="mt-2"
                color="primary"
                variant="tonal"
                @click="getCompanyAircraftReport"
                :loading="loading.airReport"
                :disabled="!companyId2"
              >
                Получить отчёт
              </v-btn>

              <div class="mt-4" v-if="airReport">
                <div class="text-subtitle-2 mb-2">
                  {{ airReport.company_name }} • всего бортов: <b>{{ airReport.total_aircrafts }}</b>
                </div>
                <v-data-table
                  :headers="airReportHeaders"
                  :items="airReport.aircrafts_by_type"
                  item-key="aircraft_type"
                />
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="6">
          <v-card variant="outlined">
            <v-card-title class="text-subtitle-1">Запрос №1: популярная марка самолёта на маршруте</v-card-title>
            <v-card-text>
              <div class="d-flex" style="gap: 12px">
                <v-text-field v-model="route.departure" label="Departure code" variant="outlined" density="compact" />
                <v-text-field v-model="route.arrival" label="Arrival code" variant="outlined" density="compact" />
              </div>
              <v-btn
                color="primary"
                variant="tonal"
                @click="getPopularAircraft"
                :loading="loading.popular"
                :disabled="!route.departure || !route.arrival"
              >
                Выполнить
              </v-btn>
              <v-alert v-if="popular" type="info" variant="tonal" class="mt-3">
                {{ popular.route }} • всего рейсов: <b>{{ popular.total_flights }}</b><br>
                Самый частый тип: <b>{{ popular.most_popular_aircraft.aircraft_type }}</b>
                ({{ popular.most_popular_aircraft.flights_count }} рейсов, {{ popular.most_popular_aircraft.percentage }}%)
              </v-alert>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="6">
          <v-card variant="outlined">
            <v-card-title class="text-subtitle-1">Запрос №2: рейсы с загрузкой ниже порога</v-card-title>
            <v-card-text>
              <v-text-field v-model.number="threshold" type="number" label="Порог, %" variant="outlined" density="compact" />
              <v-btn color="primary" variant="tonal" @click="getLowLoad" :loading="loading.lowLoad">
                Выполнить
              </v-btn>

              <div class="mt-4" v-if="lowLoad">
                Маршрутов: <b>{{ lowLoad.routes_count }}</b> (порог {{ lowLoad.threshold }}%)<br>
                <v-expansion-panels class="mt-3">
                  <v-expansion-panel v-for="(r, idx) in lowLoad.routes" :key="idx">
                    <v-expansion-panel-title>
                      {{ r.departure.code }} → {{ r.arrival.code }} • средняя загрузка {{ r.avg_load_percentage }}% • рейсов {{ r.flights_count }}
                    </v-expansion-panel-title>
                    <v-expansion-panel-text>
                      <v-data-table :headers="lowLoadHeaders" :items="r.flightsForUi" item-key="flight_number" />
                    </v-expansion-panel-text>
                  </v-expansion-panel>
                </v-expansion-panels>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { http } from '../api/http'
import { endpoints } from '../api/endpoints'
import { formatIsoHuman } from '../utils/datetime'

const error = ref('')
const companies = ref([])

const loading = reactive({
  inRepair: false,
  empCount: false,
  airReport: false,
  popular: false,
  lowLoad: false,
})

const inRepair = ref(null)
const companyId = ref(null)
const employeesCount = ref(null)

const companyId2 = ref(null)
const airReport = ref(null)

const route = reactive({ departure: '', arrival: '' })
const popular = ref(null)

const threshold = ref(50)
const lowLoad = ref(null)

const airReportHeaders = [
  { title: 'Тип', key: 'aircraft_type' },
  { title: 'Кол-во', key: 'count' },
  { title: '% от всех', key: 'percentage_of_total' },
  { title: 'Средн. вместимость', key: 'avg_capacity' },
  { title: 'Средн. скорость', key: 'avg_speed' },
  { title: 'Active', key: 'status_distribution.active' },
  { title: 'Repair', key: 'status_distribution.in_repair' },
]

const lowLoadHeaders = [
  { title: 'Рейс', key: 'flight_number' },
  { title: 'Вылет', key: 'departure_human' },
  { title: 'Тип самолёта', key: 'aircraft_type' },
  { title: 'Продано', key: 'tickets_sold' },
  { title: 'Вместимость', key: 'capacity' },
  { title: 'Загрузка, %', key: 'load_percentage' },
]

onMounted(loadCompanies)

async function loadCompanies() {
  error.value = ''
  try {
    const res = await http.get(endpoints.companies)
    companies.value = Array.isArray(res.data) ? res.data : (res.data.results || [])
  } catch (e) {
    error.value = 'Не удалось загрузить список компаний'
  }
}

async function getInRepair() {
  error.value = ''
  loading.inRepair = true
  try {
    const res = await http.get(endpoints.aircrafts + 'in_repair_count/')
    inRepair.value = res.data
  } catch (e) {
    error.value = 'Не удалось выполнить запрос'
  } finally {
    loading.inRepair = false
  }
}

async function getEmployeesCount() {
  error.value = ''
  loading.empCount = true
  try {
    const res = await http.get(endpoints.employees + 'company_employees_count/', {
      params: { company_id: companyId.value },
    })
    employeesCount.value = res.data
  } catch (e) {
    error.value = 'Не удалось выполнить запрос'
  } finally {
    loading.empCount = false
  }
}

async function getCompanyAircraftReport() {
  error.value = ''
  loading.airReport = true
  try {
    const res = await http.get(endpoints.aircrafts + 'company_aircrafts_report/', {
      params: { company_id: companyId2.value },
    })
    airReport.value = res.data
  } catch (e) {
    error.value = 'Не удалось получить отчёт'
  } finally {
    loading.airReport = false
  }
}

async function getPopularAircraft() {
  error.value = ''
  loading.popular = true
  popular.value = null
  try {
    const res = await http.get(endpoints.flights + 'popular_aircraft_on_route/', {
      params: { departure: route.departure, arrival: route.arrival },
    })
    popular.value = res.data
  } catch (e) {
    error.value = 'Не удалось выполнить запрос'
  } finally {
    loading.popular = false
  }
}

async function getLowLoad() {
  error.value = ''
  loading.lowLoad = true
  lowLoad.value = null
  try {
    const res = await http.get(endpoints.flights + 'low_load_routes/', {
      params: { threshold: threshold.value },
    })
    const data = res.data
    const routes = Array.isArray(data?.routes) ? data.routes : []
    lowLoad.value = {
      ...data,
      routes: routes.map((r) => ({
        ...r,
        flightsForUi: (Array.isArray(r.flights) ? r.flights : []).map((f) => ({
          ...f,
          departure_human: formatIsoHuman(f.departure_datetime),
        })),
      })),
    }
  } catch (e) {
    error.value = 'Не удалось выполнить запрос'
  } finally {
    loading.lowLoad = false
  }
}
</script>
