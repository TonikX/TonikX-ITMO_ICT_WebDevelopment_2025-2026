<template>
  <CrudTable
    title="Состав экипажа (связь)"
    :headers="headers"
    :fields="fields"
    :items="items"
    :loading="loading"
    :error="error"
    @create="onCreate"
    @update="onUpdate"
    @delete="onDelete"
  >
  </CrudTable>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import CrudTable from '../../components/CrudTable.vue'
import { useCrudResource } from '../../composables/useCrudResource'
import { endpoints } from '../../api/endpoints'
import { http } from '../../api/http'

const headers = [
  {
    "title": "ID",
    "key": "id"
  },
  {
    "title": "Экипаж",
    "key": "crew_name"
  },
  {
    "title": "Сотрудник",
    "key": "employee_name"
  },
  {
    "title": "Допуск",
    "key": "is_approved"
  },
  {
    "title": "",
    "key": "actions",
    "sortable": false
  }
]
const fields = ref([
  {
    "key": "crew",
    "label": "Экипаж",
    "component": "v-select",
    "rules": [
      "v=>!!v||'Обязательное поле'"
    ]
  },
  {
    "key": "employee",
    "label": "Сотрудник",
    "component": "v-select",
    "rules": [
      "v=>!!v||'Обязательное поле'"
    ]
  },
  {
    "key": "is_approved",
    "label": "Допуск к рейсу",
    "component": "v-select",
    "rules": [
      "v=>v===true||v===false||'Обязательное поле'"
    ]
  }
])

const { items, loading, error, list, create, update, remove } = useCrudResource(endpoints.crewMembers)

async function bootstrap() {
  const [resCrews, resEmployees] = await Promise.all([
    http.get(endpoints.crews),
    http.get(endpoints.employees),
  ])
  const crews = Array.isArray(resCrews.data) ? resCrews.data : (resCrews.data.results || [])
  const employees = Array.isArray(resEmployees.data) ? resEmployees.data : (resEmployees.data.results || [])
  for (const f of fields.value) {
    if (f.key === 'crew') {
      f.component = 'v-select'
      f.items = crews
      f.itemTitle = 'name'
      f.itemValue = 'id'
    }
    if (f.key === 'employee') {
      f.component = 'v-select'
      f.items = employees
      f.itemTitle = 'last_name'
      f.itemValue = 'id'
    }
    if (f.key === 'is_approved') {
      f.component = 'v-select'
      f.items = [
        { title: 'Допущен', value: true },
        { title: 'Не допущен', value: false },
      ]
      f.itemTitle = 'title'
      f.itemValue = 'value'
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
  // remove readonly helper fields from serializer if user edited them in dialog
  const forbidden = [
    'company_name',
    'departure_airport_name','departure_airport_code',
    'arrival_airport_name','arrival_airport_code',
    'aircraft_tail_number','aircraft_type','aircraft_capacity',
    'crew_members','transit_stops',
    'position_display','employee_name','employee_position','crew_name',
    'airport_code','airport_name',
  ]
  const out = { ...p }
  for (const k of forbidden) delete out[k]
  return out
}
</script>
