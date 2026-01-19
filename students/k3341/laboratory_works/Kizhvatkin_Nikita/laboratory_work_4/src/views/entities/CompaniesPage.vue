<template>
  <CrudTable
    title="Компании"
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
    "title": "Код",
    "key": "code"
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
    "label": "Название",
    "rules": [
      "v=>!!v||'Обязательное поле'"
    ],
    "fullWidth": true
  },
  {
    "key": "code",
    "label": "Код",
    "rules": [
      "v=>!!v||'Обязательное поле'"
    ]
  }
])

const { items, loading, error, list, create, update, remove } = useCrudResource(endpoints.companies)

onMounted(async () => {
  await bootstrap()
  await list()
})

async function bootstrap() {
  // override in pages that need select options
}

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
