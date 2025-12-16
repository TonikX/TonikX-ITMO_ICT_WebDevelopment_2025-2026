<template>
  <v-container v-if="employee">
    <v-btn variant="text" to="/staff" class="mb-2" prepend-icon="mdi-arrow-left">Назад к списку</v-btn>

    <v-card class="mb-6" elevation="2" rounded="lg">
      <div class="d-flex align-center pa-6">
        <v-avatar size="80" color="primary" class="mr-6 text-h4 font-weight-bold">
          {{ employee.last_name[0] }}{{ employee.first_name[0] }}
        </v-avatar>
        <div>
          <h1 class="text-h4 font-weight-bold">{{ employee.last_name }} {{ employee.first_name }}</h1>
          <div class="text-subtitle-1 text-grey">{{ employee.patronymic }}</div>
          <v-chip
            class="mt-2"
            :color="employee.is_active ? 'success' : 'error'"
            variant="tonal"
          >
            {{ employee.is_active ? 'Активный сотрудник' : 'Уволен' }}
          </v-chip>
        </div>
        <v-spacer></v-spacer>
        <div>
          <v-btn
            v-if="employee.is_active"
            color="error"
            variant="outlined"
            prepend-icon="mdi-account-remove"
            @click="fireEmployee"
          >
            Уволить
          </v-btn>
          <v-btn
            v-else
            color="success"
            variant="outlined"
            prepend-icon="mdi-account-check"
            @click="restoreEmployee"
          >
            Восстановить
          </v-btn>
        </div>
      </div>
    </v-card>

    <v-row>
      <v-col cols="12" md="4">
        <v-card class="h-100" elevation="2" rounded="lg">
          <v-card-title class="bg-grey-lighten-4">
            <v-icon class="mr-2">mdi-calendar-plus</v-icon> Добавить смену
          </v-card-title>
          <v-card-text class="pt-4">
            <v-form @submit.prevent="addSchedule">
              <v-select
                v-model="newSchedule.weekday"
                :items="weekdays"
                item-title="title"
                item-value="value"
                label="День недели"
                variant="outlined"
                density="comfortable"
                required
              />
              <v-text-field
                v-model="newSchedule.floor"
                label="Этаж"
                type="number"
                variant="outlined"
                density="comfortable"
                required
              />
              <v-btn
                type="submit"
                color="primary"
                block
                size="large"
                class="mt-2"
                :disabled="!employee.is_active"
              >
                Назначить
              </v-btn>
              <div v-if="!employee.is_active" class="text-caption text-error mt-2 text-center">
                Нельзя назначать смены уволенному
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="8">
        <v-card class="h-100" elevation="2" rounded="lg">
          <v-card-title class="d-flex align-center">
            <v-icon class="mr-2">mdi-calendar-clock</v-icon>
            График уборки
          </v-card-title>
          <v-divider></v-divider>
          <v-table hover>
            <thead>
            <tr class="bg-grey-lighten-4">
              <th class="text-left">День недели</th>
              <th class="text-left">Этаж</th>
              <th class="text-right">Действия</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="item in schedules" :key="item.id">
              <td class="font-weight-medium">{{ getWeekdayName(item.weekday) }}</td>
              <td><v-chip size="small">{{ item.floor }} этаж</v-chip></td>
              <td class="text-right">
                <v-btn icon="mdi-delete" size="small" variant="text" color="grey" @click="deleteSchedule(item.id)"></v-btn>
              </td>
            </tr>
            <tr v-if="schedules.length === 0">
              <td colspan="3" class="text-center text-grey py-8">
                <v-icon size="large" class="mb-2">mdi-calendar-blank</v-icon>
                <div>График пуст</div>
              </td>
            </tr>
            </tbody>
          </v-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api/api'

const route = useRoute()
const employee = ref(null)
const schedules = ref([])

const newSchedule = reactive({
  weekday: null,
  floor: ''
})

const weekdays = [
  { title: 'Понедельник', value: 0 },
  { title: 'Вторник', value: 1 },
  { title: 'Среда', value: 2 },
  { title: 'Четверг', value: 3 },
  { title: 'Пятница', value: 4 },
  { title: 'Суббота', value: 5 },
  { title: 'Воскресенье', value: 6 },
]

const loadData = async () => {
  const empId = route.params.id
  const empRes = await api.get(`/api/employees/${empId}/`)
  employee.value = empRes.data

  const schedRes = await api.get(`/api/schedules/?employee=${empId}`)
  schedules.value = schedRes.data.sort((a, b) => a.weekday - b.weekday)
}

const addSchedule = async () => {
  try {
    await api.post('/api/schedules/', {
      employee: employee.value.id,
      weekday: newSchedule.weekday,
      floor: newSchedule.floor
    })
    newSchedule.floor = ''
    newSchedule.weekday = null
    loadData()
  } catch (e) {
    alert('Ошибка: Возможно, на этот день и этаж уже есть запись.')
  }
}

const deleteSchedule = async (id) => {
  await api.delete(`/api/schedules/${id}/`)
  loadData()
}

const fireEmployee = async () => {
  if(!confirm('Уволить сотрудника?')) return
  await api.patch(`/api/employees/${employee.value.id}/`, { is_active: false })
  loadData()
}

const restoreEmployee = async () => {
  await api.patch(`/api/employees/${employee.value.id}/`, { is_active: true })
  loadData()
}

const getWeekdayName = (val) => weekdays.find(w => w.value === val)?.title || val

onMounted(loadData)
</script>
