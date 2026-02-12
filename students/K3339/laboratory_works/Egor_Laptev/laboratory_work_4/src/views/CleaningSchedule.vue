<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>График уборки</span>
            <v-btn color="primary" @click="openDialog(null)">Добавить</v-btn>
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="items"
              :loading="loading"
              item-key="id"
            >
              <template v-slot:item.weekday="{ item }">
                {{ translateWeekday(item.weekday) }}
              </template>
              <template v-slot:item.employee="{ item }">
                {{ item.employee ? `${item.employee.last_name} ${item.employee.first_name}` : '-' }}
              </template>
              <template v-slot:item.floor="{ item }">
                {{ item.floor?.number || '-' }}
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn icon="mdi-pencil" size="small" @click="openDialog(item)" class="mr-2"></v-btn>
                <v-btn icon="mdi-delete" size="small" color="error" @click="deleteItem(item)"></v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>{{ editingItem ? 'Редактировать' : 'Добавить' }} запись</v-card-title>
        <v-card-text>
          <v-form ref="formRef" v-model="valid" lazy-validation>
            <v-select
              v-model="form.weekday"
              :items="weekdays"
              label="День недели"
              :rules="[v => !!v || 'Обязательное поле']"
              variant="outlined"
            />
            <v-select
              v-model="form.employee_id"
              :items="employees"
              item-title="display"
              item-value="id"
              label="Сотрудник"
              :rules="[v => !!v || 'Обязательное поле']"
              variant="outlined"
            />
            <v-select
              v-model="form.floor_id"
              :items="floors"
              item-title="number"
              item-value="id"
              label="Этаж"
              :rules="[v => !!v || 'Обязательное поле']"
              variant="outlined"
            />
          </v-form>
          <v-alert v-if="error" type="error" class="mt-3">{{ error }}</v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" :disabled="!valid || saving" @click="saveItem">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { hotelAPI } from '../services/api'

const items = ref([])
const employees = ref([])
const floors = ref([])
const loading = ref(false)
const dialog = ref(false)
const valid = ref(false)
const saving = ref(false)
const error = ref('')
const editingItem = ref(null)

const form = ref({
  weekday: '',
  employee_id: null,
  floor_id: null,
})

const weekdays = [
  { title: 'Понедельник', value: 'monday' },
  { title: 'Вторник', value: 'tuesday' },
  { title: 'Среда', value: 'wednesday' },
  { title: 'Четверг', value: 'thursday' },
  { title: 'Пятница', value: 'friday' },
  { title: 'Суббота', value: 'saturday' },
  { title: 'Воскресенье', value: 'sunday' },
]

const weekdayMap = {
  monday: 'Понедельник',
  tuesday: 'Вторник',
  wednesday: 'Среда',
  thursday: 'Четверг',
  friday: 'Пятница',
  saturday: 'Суббота',
  sunday: 'Воскресенье',
}

const translateWeekday = (weekday) => {
  return weekdayMap[weekday?.toLowerCase()] || weekday
}

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'День недели', key: 'weekday' },
  { title: 'Сотрудник', key: 'employee' },
  { title: 'Этаж', key: 'floor' },
  { title: 'Действия', key: 'actions', sortable: false },
]

const loadData = async () => {
  loading.value = true
  try {
    const [cleaningRes, employeesRes, floorsRes] = await Promise.all([
      hotelAPI.cleaning.list(),
      hotelAPI.employees.list(),
      hotelAPI.floors.list(),
    ])
    items.value = cleaningRes.data
    employees.value = employeesRes.data
      .filter(e => e.employed)
      .map(e => ({
        ...e,
        display: `${e.last_name} ${e.first_name}${e.middle_name ? ' ' + e.middle_name : ''}`
      }))
    floors.value = floorsRes.data
  } catch (err) {
    error.value = 'Ошибка при загрузке данных'
  } finally {
    loading.value = false
  }
}

const openDialog = (item) => {
  editingItem.value = item
  if (item) {
    form.value = {
      weekday: item.weekday,
      employee_id: item.employee?.id,
      floor_id: item.floor?.id,
    }
  } else {
    form.value = {
      weekday: '',
      employee_id: null,
      floor_id: null,
    }
  }
  error.value = ''
  dialog.value = true
}

const formRef = ref(null)

const saveItem = async () => {
  error.value = ''
  
  if (!valid.value) {
    return
  }

  saving.value = true
  try {
    if (editingItem.value) {
      await hotelAPI.cleaning.update(editingItem.value.id, form.value)
    } else {
      await hotelAPI.cleaning.create(form.value)
    }
    dialog.value = false
    await loadData()
  } catch (err) {
    if (err.response?.data) {
      const data = err.response.data
      if (typeof data === 'object') {
        error.value = Object.values(data).flat().join(', ')
      } else {
        error.value = data
      }
    } else {
      error.value = 'Ошибка при сохранении'
    }
  } finally {
    saving.value = false
  }
}

const deleteItem = async (item) => {
  if (!confirm('Удалить запись из графика уборки?')) return
  try {
    await hotelAPI.cleaning.delete(item.id)
    await loadData()
  } catch (err) {
    error.value = 'Ошибка при удалении'
  }
}

onMounted(() => {
  loadData()
})
</script>

