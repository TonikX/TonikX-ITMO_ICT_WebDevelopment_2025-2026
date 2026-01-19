<template>
  <CrudTable
    title="Экипажи"
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
    "title": "Название",
    "key": "name"
  },
  {
    "title": "Компания",
    "key": "company_name"
  },
  {
    "title": "Активен",
    "key": "is_active"
  },
  {
    "title": "",
    "key": "actions",
    "sortable": false
  }
]
const fields = ref([
  {
    "key": "name",
    "label": "Название экипажа",
    "rules": [
      "v=>!!v||'Обязательное поле'"
    ],
    "fullWidth": true
  },
  {
    "key": "company",
    "label": "Компания",
    "component": "v-select",
    "rules": [
      "v=>!!v||'Обязательное поле'"
    ]
  },
  {
    "key": "is_active",
    "label": "Активен",
    "component": "v-select",
    "rules": [
      "v=>v===true||v===false||'Обязательное поле'"
    ]
  }
])

const { items, loading, error, list, create, update, remove } = useCrudResource(endpoints.crews)

async function bootstrap() {
  const resCompanies = await http.get(endpoints.companies)
  const companies = Array.isArray(resCompanies.data) ? resCompanies.data : (resCompanies.data.results || [])
  for (const f of fields.value) {
    if (f.key === 'company') {
      f.component = 'v-select'
      f.items = companies
      f.itemTitle = 'name'
      f.itemValue = 'id'
    }
    if (f.key === 'is_active') {
      f.component = 'v-select'
      f.items = [
        { title: 'Да', value: true },
        { title: 'Нет', value: false },
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
