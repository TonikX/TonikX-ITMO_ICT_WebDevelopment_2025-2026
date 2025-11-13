<template>
  <div>
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="text-h4">Управление бронированиями</h1>
      <v-btn color="primary" @click="openDialog()">
        <v-icon start>mdi-plus</v-icon>
        Добавить бронирование
      </v-btn>
    </div>

    <v-card>
      <v-data-table
        :headers="headers"
        :items="reservations"
        :loading="loading"
        item-key="id"
        no-data-text="Нет данных"
        items-per-page-text="Строк на странице:"
        loading-text="Загрузка..."
      >
        <template v-slot:item.reserved_from="{ item }">
          {{ formatDateTime(item.reserved_from) }}
        </template>
        <template v-slot:item.reserved_to="{ item }">
          {{ item.reserved_to ? formatDateTime(item.reserved_to) : 'Не указано' }}
        </template>
        <template v-slot:item.is_active="{ item }">
          <v-chip :color="item.is_active ? 'success' : 'grey'">
            {{ item.is_active ? 'Активно' : 'Завершено' }}
          </v-chip>
        </template>
        <template v-slot:item.actions="{ item }">
          <v-btn icon="mdi-pencil" size="small" @click="openDialog(item)"></v-btn>
          <v-btn icon="mdi-delete" size="small" color="error" @click="deleteReservation(item.id)"></v-btn>
        </template>
      </v-data-table>
    </v-card>

    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title>{{ editingReservation ? 'Редактировать бронирование' : 'Добавить бронирование' }}</v-card-title>
        <v-card-text>
          <v-form ref="formRef">
            <v-select
              v-model="form.reader"
              :items="readers"
              item-title="text"
              item-value="id"
              label="Читатель"
              variant="outlined"
              density="comfortable"
              class="mb-3"
              required
            ></v-select>
            <v-select
              v-model="form.reading_room"
              :items="readingRooms"
              item-title="text"
              item-value="id"
              label="Читальный зал"
              variant="outlined"
              density="comfortable"
              class="mb-3"
              required
            ></v-select>
            <v-menu
              v-model="dateMenuFrom"
              :close-on-content-click="false"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ props }">
                <v-text-field
                  :model-value="formattedDateFrom"
                  label="Начало бронирования"
                  prepend-inner-icon="mdi-calendar-clock"
                  readonly
                  v-bind="props"
                  variant="outlined"
                  density="comfortable"
                  class="mb-3"
                  required
                ></v-text-field>
              </template>
              <v-card>
                <v-card-text class="pa-0">
                  <v-date-picker
                    v-model="datePickerFrom"
                    @update:model-value="updateDateFrom"
                    locale="ru"
                    hide-header
                  ></v-date-picker>
                  <v-divider></v-divider>
                  <div class="pa-4">
                    <v-text-field
                      v-model="timeFrom"
                      label="Время"
                      type="time"
                      variant="outlined"
                      density="compact"
                      @update:model-value="updateDateFrom"
                    ></v-text-field>
                  </div>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn text @click="dateMenuFrom = false">Закрыть</v-btn>
                </v-card-actions>
              </v-card>
            </v-menu>
            
            <v-menu
              v-model="dateMenuTo"
              :close-on-content-click="false"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ props }">
                <v-text-field
                  :model-value="formattedDateTo"
                  label="Конец бронирования"
                  prepend-inner-icon="mdi-calendar-clock"
                  readonly
                  v-bind="props"
                  variant="outlined"
                  density="comfortable"
                  class="mb-3"
                  clearable
                  @click:clear="clearDateTo"
                ></v-text-field>
              </template>
              <v-card>
                <v-card-text class="pa-0">
                  <v-date-picker
                    v-model="datePickerTo"
                    @update:model-value="updateDateTo"
                    locale="ru"
                    hide-header
                  ></v-date-picker>
                  <v-divider></v-divider>
                  <div class="pa-4">
                    <v-text-field
                      v-model="timeTo"
                      label="Время"
                      type="time"
                      variant="outlined"
                      density="compact"
                      @update:model-value="updateDateTo"
                    ></v-text-field>
                  </div>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn text @click="dateMenuTo = false">Закрыть</v-btn>
                </v-card-actions>
              </v-card>
            </v-menu>
            <v-checkbox 
              v-model="form.is_active" 
              label="Активно"
              color="primary"
            ></v-checkbox>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveReservation" :loading="saving">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { reservationsAPI, readersAPI, readingRoomsAPI } from '@/services/api'
import dayjs from 'dayjs'

const reservations = ref([])
const readers = ref([])
const readingRooms = ref([])
const loading = ref(false)
const dialog = ref(false)
const editingReservation = ref(null)
const saving = ref(false)

const form = ref({
  reader: null,
  reading_room: null,
  reserved_from: '',
  reserved_to: '',
  is_active: true
})

// Датапикеры
const dateMenuFrom = ref(false)
const dateMenuTo = ref(false)
const datePickerFrom = ref(new Date())
const datePickerTo = ref(new Date())
const timeFrom = ref(dayjs().format('HH:mm'))
const timeTo = ref(dayjs().add(1, 'hour').format('HH:mm'))

const formattedDateFrom = computed(() => {
  if (!form.value.reserved_from) return ''
  return dayjs(form.value.reserved_from).format('DD.MM.YYYY HH:mm')
})

const formattedDateTo = computed(() => {
  if (!form.value.reserved_to) return ''
  return dayjs(form.value.reserved_to).format('DD.MM.YYYY HH:mm')
})

const updateDateFrom = () => {
  const dateStr = dayjs(datePickerFrom.value).format('YYYY-MM-DD')
  form.value.reserved_from = `${dateStr}T${timeFrom.value}`
}

const updateDateTo = () => {
  const dateStr = dayjs(datePickerTo.value).format('YYYY-MM-DD')
  form.value.reserved_to = `${dateStr}T${timeTo.value}`
}

const clearDateTo = () => {
  form.value.reserved_to = ''
}

const headers = [
  { title: 'Читатель', key: 'reader_name' },
  { title: 'Зал', key: 'reading_room_number' },
  { title: 'Начало', key: 'reserved_from' },
  { title: 'Конец', key: 'reserved_to' },
  { title: 'Статус', key: 'is_active' },
  { title: 'Действия', key: 'actions', sortable: false }
]

const formatDateTime = (datetime) => {
  return dayjs(datetime).format('DD.MM.YYYY HH:mm')
}

const loadReservations = async () => {
  try {
    loading.value = true
    const response = await reservationsAPI.getAll()
    reservations.value = response.data.results || response.data
  } catch (error) {
    console.error('Ошибка загрузки бронирований:', error)
  } finally {
    loading.value = false
  }
}

const loadReaders = async () => {
  try {
    const response = await readersAPI.getAll()
    const data = response.data.results || response.data
    readers.value = data.map(r => ({
      id: r.id,
      text: `${r.last_name} ${r.first_name} (${r.library_card})`
    }))
  } catch (error) {
    console.error('Ошибка загрузки читателей:', error)
  }
}

const loadReadingRooms = async () => {
  try {
    const response = await readingRoomsAPI.getAll()
    const data = response.data.results || response.data
    readingRooms.value = data.map(r => ({
      id: r.id,
      text: `Зал ${r.number} (этаж ${r.floor})`
    }))
  } catch (error) {
    console.error('Ошибка загрузки залов:', error)
  }
}

const openDialog = (reservation = null) => {
  editingReservation.value = reservation
  if (reservation) {
    const fromDate = dayjs(reservation.reserved_from)
    const toDate = reservation.reserved_to ? dayjs(reservation.reserved_to) : null
    
    form.value = {
      reader: reservation.reader,
      reading_room: reservation.reading_room,
      reserved_from: fromDate.format('YYYY-MM-DDTHH:mm'),
      reserved_to: toDate ? toDate.format('YYYY-MM-DDTHH:mm') : '',
      is_active: reservation.is_active
    }
    
    datePickerFrom.value = fromDate.toDate()
    timeFrom.value = fromDate.format('HH:mm')
    
    if (toDate) {
      datePickerTo.value = toDate.toDate()
      timeTo.value = toDate.format('HH:mm')
    }
  } else {
    const now = dayjs()
    const later = now.add(1, 'hour')
    
    form.value = {
      reader: null,
      reading_room: null,
      reserved_from: now.format('YYYY-MM-DDTHH:mm'),
      reserved_to: '',
      is_active: true
    }
    
    datePickerFrom.value = now.toDate()
    timeFrom.value = now.format('HH:mm')
    datePickerTo.value = later.toDate()
    timeTo.value = later.format('HH:mm')
  }
  dialog.value = true
}

const saveReservation = async () => {
  try {
    saving.value = true
    const data = {
      ...form.value,
      reserved_from: form.value.reserved_from,
      reserved_to: form.value.reserved_to || null
    }
    if (editingReservation.value) {
      await reservationsAPI.update(editingReservation.value.id, data)
    } else {
      await reservationsAPI.create(data)
    }
    dialog.value = false
    loadReservations()
  } catch (error) {
    console.error('Ошибка сохранения бронирования:', error)
  } finally {
    saving.value = false
  }
}

const deleteReservation = async (id) => {
  if (confirm('Удалить бронирование?')) {
    try {
      await reservationsAPI.delete(id)
      loadReservations()
    } catch (error) {
      console.error('Ошибка удаления бронирования:', error)
    }
  }
}

onMounted(() => {
  loadReservations()
  loadReaders()
  loadReadingRooms()
})
</script>

