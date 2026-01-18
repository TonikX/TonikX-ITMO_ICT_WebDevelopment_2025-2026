<template>
  <v-container>
    <v-card>
      <v-card-title>Информация о клиенте</v-card-title>
      <v-card-text>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-select
              v-model="selectedClient"
              :items="residents"
              item-title="full_name"
              item-value="id"
              label="Выберите клиента"
              outlined
              dense
            ></v-select>
          </v-col>

          <v-col cols="12" md="4">
            <v-menu v-model="startMenu" :close-on-content-click="false" transition="scale-transition" offset-y>
              <template #activator="{ props }">
                <v-text-field
                  v-model="startDate"
                  label="Дата начала"
                  readonly
                  v-bind="props"
                  outlined
                  dense
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="startDatePicker"
                @update:model-value="val => { startDate = formatDate(val); startDatePicker = val; startMenu=false }"
                locale="ru"
                no-title
              ></v-date-picker>
            </v-menu>
          </v-col>

          <v-col cols="12" md="4">
            <v-menu v-model="endMenu" :close-on-content-click="false" transition="scale-transition" offset-y>
              <template #activator="{ props }">
                <v-text-field
                  v-model="endDate"
                  label="Дата окончания"
                  readonly
                  v-bind="props"
                  outlined
                  dense
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="endDatePicker"
                @update:model-value="val => { endDate = formatDate(val); endDatePicker = val; endMenu=false }"
                locale="ru"
                no-title
              ></v-date-picker>
            </v-menu>
          </v-col>
        </v-row>

        <v-btn color="#1B5E20" class="mt-2" @click="searchClient">
          Поиск
        </v-btn>

        <div v-if="error" style="color:red" class="mt-2">{{ error }}</div>

        <v-table v-if="clientInfo" class="mt-4">
          <thead>
            <tr>
              <th>Фамилия</th>
              <th>Имя</th>
              <th>Отчество</th>
              <th>Паспорт</th>
              <th>Город</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{{ clientInfo.surname }}</td>
              <td>{{ clientInfo.name }}</td>
              <td>{{ clientInfo.patronymic }}</td>
              <td>{{ clientInfo.passport_number }}</td>
              <td>{{ clientInfo.city }}</td>
            </tr>
          </tbody>
        </v-table>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'

const residents = ref([])
const selectedClient = ref(null)
const clientInfo = ref(null)
const error = ref('')

const startDate = ref('')
const endDate = ref('')
const startMenu = ref(false)
const endMenu = ref(false)
const startDatePicker = ref(null)
const endDatePicker = ref(null)

const formatDate = (date) => {
  const d = new Date(date)
  const yyyy = d.getFullYear()
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const dd = String(d.getDate()).padStart(2, '0')
  return `${yyyy}-${mm}-${dd}`
}

const loadResidents = async () => {
  try {
    const res = await api.get('residents/')
    residents.value = res.data.map(r => ({
      ...r,
      full_name: `${r.surname} ${r.name} ${r.patronymic}`
    }))
  } catch (e) {
    console.error('Ошибка загрузки клиентов', e)
  }
}

onMounted(() => {
  loadResidents()
})

const searchClient = async () => {
  error.value = ''
  clientInfo.value = null

  if (!selectedClient.value || !startDate.value || !endDate.value) {
    error.value = 'Заполните все поля'
    return
  }

  try {
    const res = await api.get(
      `req/clients_with_city/?id_client=${selectedClient.value}&start_date=${startDate.value}&end_date=${endDate.value}`
    )
    clientInfo.value = res.data
  } catch (e) {
    console.error(e)
    error.value = 'Ошибка получения данных'
  }
}
</script>
