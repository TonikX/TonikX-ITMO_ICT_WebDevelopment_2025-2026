<template>
  <v-container>
    <v-card>
      <v-card-title>Персонал уборки по дню</v-card-title>

      <v-card-text>
        <v-row dense>
          <!-- Клиент -->
          <v-col cols="12" md="6">
            <v-select
              v-model="selectedClient"
              :items="clients"
              item-title="full_name"
              item-value="id"
              label="Клиент"
              outlined
              dense
            />
          </v-col>

          <!-- День недели -->
          <v-col cols="12" md="6">
            <v-select
              v-model="weekDay"
              :items="weekDays"
              item-title="label"
              item-value="value"
              label="День недели"
              outlined
              dense
            />
          </v-col>
        </v-row>

        <v-btn color="#1B5E20" class="mt-3" @click="loadCleaningStaff">
          Показать
        </v-btn>

        <div v-if="error" class="mt-2" style="color:red">
          {{ error }}
        </div>

        <v-card v-if="result" class="mt-4" variant="outlined">
          <v-card-title>Результат</v-card-title>
          <v-card-text>
            <pre>{{ result }}</pre>
          </v-card-text>
        </v-card>
      </v-card-text>
    </v-card>
  </v-container>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'

const clients = ref([])
const selectedClient = ref(null)
const weekDay = ref(null)
const error = ref('')
const result = ref(null)

const weekDays = [
  { label: 'Понедельник', value: 'mon' },
  { label: 'Вторник', value: 'tue' },
  { label: 'Среда', value: 'wed' },
  { label: 'Четверг', value: 'thu' },
  { label: 'Пятница', value: 'fri' },
  { label: 'Суббота', value: 'sat' },
  { label: 'Воскресенье', value: 'sun' }
]

const loadClients = async () => {
  try {
    const res = await api.get('residents/')
    clients.value = res.data.map(c => ({
      ...c,
      full_name: `${c.surname} ${c.name} ${c.patronymic}`
    }))
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  loadClients()
})


const loadCleaningStaff = async () => {
  error.value = ''
  result.value = null

  if (!selectedClient.value || !weekDay.value) {
    error.value = 'Выберите клиента и день недели'
    return
  }

  try {
    const res = await api.get(
      `req/cleaing_staff/?id_client=${selectedClient.value}&week_day=${weekDay.value}`
    )
    result.value = res.data
  } catch (e) {
    console.error(e)
    error.value = 'Ошибка получения данных'
  }
}
</script>
