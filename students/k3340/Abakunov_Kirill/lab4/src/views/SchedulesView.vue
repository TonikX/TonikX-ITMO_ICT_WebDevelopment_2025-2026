<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4">
          <v-icon class="mr-2">mdi-calendar-clock</v-icon>
          Расписание уборки
        </h1>
      </v-col>
      <v-col cols="auto" v-if="authStore.isAuthenticated">
        <v-btn color="primary" @click="openCreateDialog">
          <v-icon left>mdi-plus</v-icon>
          Добавить запись
        </v-btn>
      </v-col>
    </v-row>

    <!-- Фильтры -->
    <v-card class="mb-4 pa-4">
      <v-row align="center">
        <v-col cols="12" sm="4">
          <v-select
            v-model="filterFloor"
            label="Этаж"
            :items="floors"
            clearable
            hide-details
          ></v-select>
        </v-col>
        <v-col cols="12" sm="4">
          <v-select
            v-model="filterWeekday"
            label="День недели"
            :items="weekdays"
            item-title="text"
            item-value="value"
            clearable
            hide-details
          ></v-select>
        </v-col>
        <v-col cols="12" sm="4">
          <v-btn color="primary" @click="loadSchedules" variant="tonal" block>
            <v-icon left>mdi-refresh</v-icon>
            Обновить
          </v-btn>
        </v-col>
      </v-row>
    </v-card>

    <v-progress-linear v-if="loading" indeterminate color="primary"></v-progress-linear>

    <!-- Расписание по дням недели -->
    <v-row>
      <v-col 
        v-for="day in weekdays" 
        :key="day.value" 
        cols="12" 
        sm="6" 
        md="4" 
        lg="3"
      >
        <v-card class="h-100">
          <v-card-title class="bg-primary text-white">
            {{ day.text }}
          </v-card-title>
          <v-card-text class="pa-0">
            <v-list density="compact">
              <template v-for="schedule in getSchedulesByDay(day.value)" :key="schedule.id">
                <v-list-item>
                  <template v-slot:prepend>
                    <v-avatar color="warning" size="32">
                      <span class="text-caption">{{ schedule.floor }}</span>
                    </v-avatar>
                  </template>
                  <v-list-item-title>{{ schedule.staff_name }}</v-list-item-title>
                  <v-list-item-subtitle>{{ schedule.floor }} этаж</v-list-item-subtitle>
                  <template v-slot:append v-if="authStore.isAuthenticated">
                    <v-btn icon size="x-small" @click="editSchedule(schedule)">
                      <v-icon size="small">mdi-pencil</v-icon>
                    </v-btn>
                    <v-btn icon size="x-small" color="error" @click="confirmDelete(schedule)">
                      <v-icon size="small">mdi-delete</v-icon>
                    </v-btn>
                  </template>
                </v-list-item>
                <v-divider></v-divider>
              </template>
              <v-list-item v-if="getSchedulesByDay(day.value).length === 0">
                <v-list-item-title class="text-grey text-center">
                  Нет записей
                </v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалог создания/редактирования -->
    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>
          {{ isEditing ? 'Редактировать расписание' : 'Добавить расписание' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="formRef">
            <v-select
              v-model="form.staff"
              label="Служащий"
              :items="activeStaff"
              item-title="full_name"
              item-value="id"
              :rules="[rules.required]"
            ></v-select>
            <v-text-field
              v-model.number="form.floor"
              label="Этаж"
              type="number"
              :rules="[rules.required, rules.minValue(1)]"
            ></v-text-field>
            <v-select
              v-model="form.weekday"
              label="День недели"
              :items="weekdays"
              item-title="text"
              item-value="value"
              :rules="[rules.required]"
            ></v-select>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveSchedule" :loading="saving">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог удаления -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Подтверждение удаления</v-card-title>
        <v-card-text>
          Удалить запись расписания для {{ scheduleToDelete?.staff_name }} 
          ({{ scheduleToDelete?.floor }} этаж)?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="deleteDialog = false">Отмена</v-btn>
          <v-btn color="error" @click="deleteSchedule" :loading="saving">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, inject } from 'vue'
import { schedulesAPI, staffAPI, roomsAPI } from '@/api'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const showSnackbar = inject('showSnackbar')

const schedules = ref([])
const activeStaff = ref([])
const loading = ref(false)
const saving = ref(false)
const dialog = ref(false)
const deleteDialog = ref(false)
const isEditing = ref(false)
const editingId = ref(null)
const scheduleToDelete = ref(null)
const formRef = ref(null)
const filterFloor = ref(null)
const filterWeekday = ref(null)

const weekdays = [
  { value: 1, text: 'Понедельник' },
  { value: 2, text: 'Вторник' },
  { value: 3, text: 'Среда' },
  { value: 4, text: 'Четверг' },
  { value: 5, text: 'Пятница' },
  { value: 6, text: 'Суббота' },
  { value: 7, text: 'Воскресенье' },
]

const floors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

const form = reactive({
  staff: null,
  floor: 1,
  weekday: 1,
})

const rules = {
  required: (v) => !!v || v === 0 || 'Обязательное поле',
  minValue: (min) => (v) => v >= min || `Минимум ${min}`,
}

const filteredSchedules = computed(() => {
  let result = schedules.value

  if (filterFloor.value) {
    result = result.filter(s => s.floor === filterFloor.value)
  }

  if (filterWeekday.value) {
    result = result.filter(s => s.weekday === filterWeekday.value)
  }

  return result
})

const getSchedulesByDay = (weekday) => {
  return filteredSchedules.value.filter(s => s.weekday === weekday)
}

const loadSchedules = async () => {
  loading.value = true
  try {
    const response = await schedulesAPI.getAll()
    schedules.value = response.data.results || response.data
  } catch (error) {
    showSnackbar('Ошибка загрузки расписаний', 'error')
  } finally {
    loading.value = false
  }
}

const loadActiveStaff = async () => {
  try {
    const response = await staffAPI.getActive()
    activeStaff.value = response.data.staff || []
  } catch (error) {
    console.error('Error loading staff:', error)
  }
}

const openCreateDialog = () => {
  isEditing.value = false
  editingId.value = null
  Object.assign(form, { staff: null, floor: 1, weekday: 1 })
  dialog.value = true
}

const editSchedule = (schedule) => {
  isEditing.value = true
  editingId.value = schedule.id
  Object.assign(form, {
    staff: schedule.staff,
    floor: schedule.floor,
    weekday: schedule.weekday,
  })
  dialog.value = true
}

const saveSchedule = async () => {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  saving.value = true
  try {
    if (isEditing.value) {
      await schedulesAPI.update(editingId.value, form)
      showSnackbar('Расписание обновлено', 'success')
    } else {
      await schedulesAPI.create(form)
      showSnackbar('Расписание добавлено', 'success')
    }
    dialog.value = false
    loadSchedules()
  } catch (error) {
    const errorMsg = error.response?.data?.non_field_errors?.[0] || 'Ошибка сохранения'
    showSnackbar(errorMsg, 'error')
  } finally {
    saving.value = false
  }
}

const confirmDelete = (schedule) => {
  scheduleToDelete.value = schedule
  deleteDialog.value = true
}

const deleteSchedule = async () => {
  saving.value = true
  try {
    await schedulesAPI.delete(scheduleToDelete.value.id)
    showSnackbar('Расписание удалено', 'success')
    deleteDialog.value = false
    loadSchedules()
  } catch (error) {
    showSnackbar('Ошибка удаления', 'error')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadSchedules()
  loadActiveStaff()
})
</script>
