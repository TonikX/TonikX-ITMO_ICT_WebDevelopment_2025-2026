<template>
  <v-card>
    <v-card-title class="d-flex align-center">
      <div class="text-h6">Рейсы</div>
      <v-spacer />

      <v-text-field
        v-model="search"
        density="compact"
        variant="outlined"
        hide-details
        label="Поиск (номер рейса)"
        style="max-width: 320px"
      />

      <v-btn
        v-if="canWrite"
        class="ml-3"
        color="primary"
        prepend-icon="mdi-plus"
        @click="openCreate"
      >
        Добавить
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
        {{ error }}
      </v-alert>

      <v-data-table
        :headers="headers"
        :items="filtered"
        :loading="loading"
        item-value="id"
      >
        <template #item.flight_number="{ item }">
          <router-link :to="{ name: 'flightDetails', params: { id: unwrap(item).id } }">
            {{ unwrap(item).flight_number }}
          </router-link>
        </template>

        <template #item.departure_datetime="{ item }">
          {{ formatIsoHuman(unwrap(item).departure_datetime) }}
        </template>

        <template v-if="canWrite" #item.actions="{ item }">
          <v-btn size="small" variant="text" icon="mdi-pencil" @click="openEdit(item)" />
          <v-btn size="small" variant="text" icon="mdi-delete" @click="openDelete(item)" />
        </template>

        <template #no-data>
          <div class="pa-6 text-medium-emphasis">Нет данных</div>
        </template>
      </v-data-table>
    </v-card-text>

    <!-- create/edit dialog -->
    <v-dialog v-model="dialog" max-width="900">
      <v-card>
        <v-card-title class="text-h6">{{ dialogTitle }}</v-card-title>

        <v-card-text>
          <v-form ref="formRef" @submit.prevent="submit">
            <div class="d-flex flex-wrap" style="gap: 12px">
              <template v-for="field in fields" :key="field.key">
                <div :style="{ flex: field.fullWidth ? '1 0 100%' : '1 0 320px' }">
                  <component
                    :is="resolveComponent(field)"
                    v-model="model[field.key]"
                    :label="field.label"
                    :rules="field.rules || []"
                    :items="field.items"
                    :item-title="field.itemTitle"
                    :item-value="field.itemValue"
                    :type="field.type"
                    variant="outlined"
                    density="compact"
                    :clearable="true"
                  />
                </div>
              </template>
            </div>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" :disabled="!canWrite" @click="submit">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- confirm delete -->
    <v-dialog v-model="confirmDelete" max-width="520">
      <v-card>
        <v-card-title class="text-h6">Удалить рейс?</v-card-title>
        <v-card-text>
          <div>Это действие нельзя отменить.</div>
          <div class="mt-2 text-medium-emphasis">ID: {{ selected?.id }}</div>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="confirmDelete = false">Отмена</v-btn>
          <v-btn color="error" :disabled="!canWrite" @click="doDelete">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { VTextField, VSelect } from 'vuetify/components'

import DateTimeField from '../../components/DateTimeField.vue'
import { splitIso, toIsoFromDt, formatIsoHuman } from '../../utils/datetime'

import { useCrudResource } from '../../composables/useCrudResource'
import { endpoints } from '../../api/endpoints'
import { http } from '../../api/http'
import { useAuthStore } from '../../stores/auth'

const auth = useAuthStore()
auth.hydrate()

const canWrite = computed(() => {
  const u = auth.user
  return !!(u && (u.is_staff || u.is_superuser))
})

const headers = computed(() => {
  const base = [
    { title: 'ID', key: 'id' },
    { title: 'Номер', key: 'flight_number' },
    { title: 'Дистанция', key: 'distance' },
    { title: 'Вылет', key: 'departure_airport_code' },
    { title: 'Прилёт', key: 'arrival_airport_code' },
    { title: 'Дата вылета', key: 'departure_datetime' },
    { title: 'Самолёт', key: 'aircraft_tail_number' },
    { title: 'Продано', key: 'tickets_sold' },
  ]
  if (canWrite.value) base.push({ title: '', key: 'actions', sortable: false })
  return base
})

const fields = ref([
  { key: 'flight_number', label: 'Номер рейса', rules: [v => !!v || 'Обязательное поле'] },
  { key: 'distance', label: 'Дистанция', type: 'number', rules: [v => (v !== null && v !== '') || 'Обязательное поле'] },

  { key: 'departure_airport', label: 'Аэропорт вылета', component: 'select', rules: [v => !!v || 'Обязательное поле'] },
  { key: 'arrival_airport', label: 'Аэропорт прилёта', component: 'select', rules: [v => !!v || 'Обязательное поле'] },

  { key: 'departure_datetime', label: 'Дата/время вылета', component: 'datetime', rules: [v => !!v?.date || 'Обязательное поле'], fullWidth: true },
  { key: 'arrival_datetime', label: 'Дата/время прилёта', component: 'datetime', rules: [v => !!v?.date || 'Обязательное поле'], fullWidth: true },

  { key: 'aircraft', label: 'Самолёт', component: 'select', rules: [v => !!v || 'Обязательное поле'] },
  { key: 'tickets_sold', label: 'Продано билетов', type: 'number', rules: [v => (v !== null && v !== '') || 'Обязательное поле'] },
  { key: 'crew', label: 'Экипаж (опционально)', component: 'select' },
])

function resolveComponent(field) {
  if (field.component === 'select') return VSelect
  if (field.component === 'datetime') return DateTimeField
  return VTextField
}

function unwrap(item) {
  return item?.raw ?? item
}

const { items, loading, error, list, create, update, remove, retrieve } =
  useCrudResource(endpoints.flights)

const search = ref('')
const dialog = ref(false)
const confirmDelete = ref(false)
const selected = ref(null)
const model = ref({})
const mode = ref('create')
const formRef = ref(null)

const dialogTitle = computed(() =>
  mode.value === 'create' ? 'Создание рейса' : 'Редактирование рейса'
)

const filtered = computed(() => {
  const s = search.value.trim().toLowerCase()
  if (!s) return items.value
  return items.value.filter(x => String(x.flight_number || '').toLowerCase().includes(s))
})

onMounted(async () => {
  await bootstrap()
  await list()
})

async function bootstrap() {
  const [resAirports, resAircrafts, resCrews] = await Promise.all([
    http.get(endpoints.airports),
    http.get(endpoints.aircrafts),
    http.get(endpoints.crews),
  ])

  const airports = Array.isArray(resAirports.data) ? resAirports.data : (resAirports.data.results || [])
  const aircrafts = Array.isArray(resAircrafts.data) ? resAircrafts.data : (resAircrafts.data.results || [])
  const crews = Array.isArray(resCrews.data) ? resCrews.data : (resCrews.data.results || [])

  for (const f of fields.value) {
    if (f.key === 'departure_airport' || f.key === 'arrival_airport') {
      f.items = airports
      f.itemTitle = 'code'
      f.itemValue = 'id'
    }
    if (f.key === 'aircraft') {
      f.items = aircrafts
      f.itemTitle = 'tail_number'
      f.itemValue = 'id'
    }
    if (f.key === 'crew') {
      f.items = [{ id: null, name: '(без экипажа)' }, ...crews]
      f.itemTitle = 'name'
      f.itemValue = 'id'
    }
  }
}

function openCreate() {
  if (!canWrite.value) return
  mode.value = 'create'
  selected.value = null
  model.value = {
    flight_number: '',
    distance: null,
    departure_airport: null,
    arrival_airport: null,
    departure_datetime: { date: '', time: '' },
    arrival_datetime: { date: '', time: '' },
    aircraft: null,
    tickets_sold: 0,
    crew: null,
  }
  dialog.value = true
}

async function openEdit(item) {
  if (!canWrite.value) return
  mode.value = 'edit'
  const row = unwrap(item)
  selected.value = row

  const full = await retrieve(row.id)

  model.value = {
    flight_number: full.flight_number,
    distance: full.distance,
    departure_airport: full.departure_airport,
    arrival_airport: full.arrival_airport,
    departure_datetime: splitIso(full.departure_datetime),
    arrival_datetime: splitIso(full.arrival_datetime),
    aircraft: full.aircraft,
    tickets_sold: full.tickets_sold,
    crew: full.crew ?? null,
  }

  dialog.value = true
}

function openDelete(item) {
  if (!canWrite.value) return
  selected.value = unwrap(item)
  confirmDelete.value = true
}

async function submit() {
  const res = await formRef.value?.validate?.()
  if (res && !res.valid) return

  const payload = {
    ...model.value,
    departure_datetime: toIsoFromDt(model.value.departure_datetime),
    arrival_datetime: toIsoFromDt(model.value.arrival_datetime),
  }

  if (payload.crew === null) delete payload.crew

  if (mode.value === 'create') await create(payload)
  else await update(selected.value.id, payload)

  dialog.value = false
  await list()
}

async function doDelete() {
  await remove(selected.value.id)
  confirmDelete.value = false
  await list()
}
</script>
