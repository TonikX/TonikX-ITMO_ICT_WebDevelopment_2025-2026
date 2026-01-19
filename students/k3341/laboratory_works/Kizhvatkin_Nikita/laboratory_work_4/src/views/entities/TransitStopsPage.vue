<template>
  <CrudTable
    title="Транзитные остановки"
    :headers="headers"
    :fields="fields"
    :items="itemsForTable"
    :loading="loading"
    :error="error"
    @create="onCreate"
    @update="onUpdate"
    @delete="onDelete"
  />
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import CrudTable from '../../components/CrudTable.vue'
import { useCrudResource } from '../../composables/useCrudResource'
import { endpoints } from '../../api/endpoints'
import { http } from '../../api/http'
import DateTimeField from '../../components/DateTimeField.vue'
import { toIsoFromDt, splitIso, formatIsoHuman } from '../../utils/datetime'

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Рейс', key: 'flight_display' },
  { title: 'Аэропорт', key: 'airport_code' },
  { title: 'Прибытие', key: 'arrival_human' },
  { title: 'Вылет', key: 'departure_human' },
  { title: '', key: 'actions', sortable: false },
]

const fields = ref([
  {
    key: 'flight',
    label: 'Рейс',
    component: 'v-select',
    rules: ['v=>!!v||"Обязательное поле"'],
  },
  {
    key: 'airport',
    label: 'Аэропорт',
    component: 'v-select',
    rules: ['v=>!!v||"Обязательное поле"'],
  },

  // DateTimeField хранит {date,time}; перед отправкой соберём ISO
  {
    key: 'arrival_dt',
    label: 'Дата/время прибытия',
    component: DateTimeField,
    rules: ['v=>!!(v?.date)||"Обязательное поле"'],
    fullWidth: true,
  },
  {
    key: 'departure_dt',
    label: 'Дата/время вылета',
    component: DateTimeField,
    rules: ['v=>!!(v?.date)||"Обязательное поле"'],
    fullWidth: true,
  },
])

const { items, loading, error, list, create, update, remove } =
  useCrudResource(endpoints.transitStops)

const flightsById = ref(new Map())

const itemsForTable = computed(() => {
  const arr = Array.isArray(items.value) ? items.value : []
  return arr.map((x) => {
    const flightObj = flightsById.value.get(x.flight)
    const flightDisplay = flightObj
      ? `${flightObj.flight_number} (ID: ${flightObj.id})`
      : String(x.flight ?? '')

    return {
      ...x,
      flight_display: flightDisplay,
      arrival_human: formatIsoHuman(x.arrival_datetime),
      departure_human: formatIsoHuman(x.departure_datetime),
    }
  })
})

async function bootstrap() {
  const [resFlights, resAirports] = await Promise.all([
    http.get(endpoints.flights),
    http.get(endpoints.airports),
  ])

  const flights = Array.isArray(resFlights.data)
    ? resFlights.data
    : (resFlights.data.results || [])

  const airports = Array.isArray(resAirports.data)
    ? resAirports.data
    : (resAirports.data.results || [])

  flightsById.value = new Map(flights.map((f) => [f.id, f]))

  for (const f of fields.value) {
    if (f.key === 'flight') {
      f.items = flights
      f.itemTitle = 'flight_number'
      f.itemValue = 'id'
    }
    if (f.key === 'airport') {
      f.items = airports
      f.itemTitle = 'code'
      f.itemValue = 'id'
    }
  }
}

onMounted(async () => {
  await bootstrap()
  await list()
})

async function onCreate(payload) {
  await create(cleanPayload(payload))
  await list()
}

async function onUpdate({ id, payload }) {
  await update(id, cleanPayload(payload))
  await list()
}

async function onDelete(id) {
  await remove(id)
  await list()
}

function cleanPayload(p) {
  const forbidden = [
    'company_name',
    'departure_airport_name', 'departure_airport_code',
    'arrival_airport_name', 'arrival_airport_code',
    'aircraft_tail_number', 'aircraft_type', 'aircraft_capacity',
    'crew_members', 'transit_stops',
    'position_display', 'employee_name', 'employee_position', 'crew_name',
    'airport_code', 'airport_name',
    'arrival_human', 'departure_human', 'flight_display',
  ]

  const out = { ...p }
  for (const k of forbidden) delete out[k]

  // DateTimeField -> ISO строки для API
  if (out.arrival_dt) out.arrival_datetime = toIsoFromDt(out.arrival_dt)
  if (out.departure_dt) out.departure_datetime = toIsoFromDt(out.departure_dt)

  delete out.arrival_dt
  delete out.departure_dt

  return out
}
</script>
