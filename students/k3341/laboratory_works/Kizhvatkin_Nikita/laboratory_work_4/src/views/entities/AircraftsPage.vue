<template>
  <CrudTable
    title="Самолёты"
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
    "title": "Бортовой номер",
    "key": "tail_number"
  },
  {
    "title": "Тип",
    "key": "aircraft_type"
  },
  {
    "title": "Вместимость",
    "key": "capacity"
  },
  {
    "title": "Скорость",
    "key": "speed"
  },
  {
    "title": "Компания",
    "key": "company_name"
  },
  {
    "title": "Статус",
    "key": "status"
  },
  {
    "title": "",
    "key": "actions",
    "sortable": false
  }
]
const fields = ref([
  {
    "key": "tail_number",
    "label": "Бортовой номер",
    "rules": [
      "v=>!!v||'Обязательное поле'"
    ]
  },
  {
    "key": "aircraft_type",
    "label": "Тип самолёта",
    "rules": [
      "v=>!!v||'Обязательное поле'"
    ]
  },
  {
    "key": "capacity",
    "label": "Вместимость",
    "type": "number",
    "rules": [
      "v=>v!==null&&v!==''||'Обязательное поле'"
    ]
  },
  {
    "key": "speed",
    "label": "Скорость",
    "type": "number",
    "rules": [
      "v=>v!==null&&v!==''||'Обязательное поле'"
    ]
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
    "key": "status",
    "label": "Статус",
    "component": "v-select",
    "items": [
      {
        "title": "active",
        "value": "active"
      },
      {
        "title": "repair",
        "value": "repair"
      }
    ],
    "itemTitle": "title",
    "itemValue": "value"
  }
])

const { items, loading, error, list, create, update, remove } = useCrudResource(endpoints.aircrafts)

async function bootstrap() {
  // Load companies for select lists
  const resCompanies = await http.get(endpoints.companies)
  const companies = Array.isArray(resCompanies.data) ? resCompanies.data : (resCompanies.data.results || [])
  // set items
  for (const f of fields.value) {
    if (f.key === 'company') {
      f.component = 'v-select'
      f.items = companies
      f.itemTitle = 'name'
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
    'departure_airport_name','departure_airport_code',
    'arrival_airport_name','arrival_airport_code',
    'aircraft_tail_number','aircraft_capacity',
    'crew_members','transit_stops',
    'position_display','employee_name','employee_position','crew_name',
    'airport_code','airport_name',
  ]
  const out = { ...p }
  for (const k of forbidden) delete out[k]
  return out
}
</script>
