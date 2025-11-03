<template>
  <div>
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="text-h4">Управление читальными залами</h1>
      <v-btn color="primary" @click="openDialog()">
        <v-icon start>mdi-plus</v-icon>
        Добавить зал
      </v-btn>
    </div>

    <v-card>
      <v-data-table
        :headers="headers"
        :items="readingRooms"
        :loading="loading"
        item-key="id"
        no-data-text="Нет данных"
        items-per-page-text="Строк на странице:"
        loading-text="Загрузка..."
      >
        <template v-slot:item.room_type_display="{ item }">
          <v-chip :color="getReadingRoomTypeColor(item.room_type)">
            {{ item.room_type_display }}
          </v-chip>
        </template>
        <template v-slot:item.hourly_rate="{ item }">
          {{ item.hourly_rate }} ₽
        </template>
        <template v-slot:item.actions="{ item }">
          <v-btn icon="mdi-pencil" size="small" @click="openDialog(item)"></v-btn>
          <v-btn icon="mdi-delete" size="small" color="error" @click="deleteReadingRoom(item.id)"></v-btn>
        </template>
      </v-data-table>
    </v-card>

    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title>{{ editingReadingRoom ? 'Редактировать зал' : 'Добавить зал' }}</v-card-title>
        <v-card-text>
          <v-form ref="formRef">
            <v-text-field 
              v-model.number="form.number" 
              label="Номер зала" 
              type="number" 
              variant="outlined"
              density="comfortable"
              class="mb-3"
              required
            ></v-text-field>
            <v-text-field 
              v-model.number="form.floor" 
              label="Этаж" 
              type="number" 
              variant="outlined"
              density="comfortable"
              class="mb-3"
              required
            ></v-text-field>
            <v-select 
              v-model="form.room_type" 
              label="Тип зала" 
              :items="readingRoomTypes"
              variant="outlined"
              density="comfortable"
              class="mb-3"
              required
            ></v-select>
            <v-text-field 
              v-model.number="form.capacity" 
              label="Вместимость (мест)" 
              type="number"
              variant="outlined"
              density="comfortable"
              class="mb-3"
              required
            ></v-text-field>
            <v-text-field 
              v-model.number="form.hourly_rate" 
              label="Цена за час (₽)" 
              type="number"
              step="0.01"
              variant="outlined"
              density="comfortable"
              class="mb-3"
              required
            ></v-text-field>
            <v-textarea 
              v-model="form.description" 
              label="Описание"
              variant="outlined"
              density="comfortable"
              rows="3"
            ></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveReadingRoom" :loading="saving">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { readingRoomsAPI } from '@/services/api'

const readingRooms = ref([])
const loading = ref(false)
const dialog = ref(false)
const editingReadingRoom = ref(null)
const saving = ref(false)

const form = ref({
  number: null,
  floor: null,
  room_type: '',
  capacity: null,
  hourly_rate: null,
  description: ''
})

const readingRoomTypes = [
  { title: 'Малый зал', value: 'small' },
  { title: 'Средний зал', value: 'medium' },
  { title: 'Большой зал', value: 'large' }
]

const headers = [
  { title: 'Номер', key: 'number' },
  { title: 'Этаж', key: 'floor' },
  { title: 'Тип', key: 'room_type_display' },
  { title: 'Вместимость', key: 'capacity' },
  { title: 'Цена/час', key: 'hourly_rate' },
  { title: 'Действия', key: 'actions', sortable: false }
]

const getReadingRoomTypeColor = (type) => {
  const colors = { small: 'blue', medium: 'green', large: 'orange' }
  return colors[type] || 'grey'
}

const loadReadingRooms = async () => {
  try {
    loading.value = true
    const response = await readingRoomsAPI.getAll()
    readingRooms.value = response.data.results || response.data
  } catch (error) {
    console.error('Ошибка загрузки залов:', error)
  } finally {
    loading.value = false
  }
}

const openDialog = (readingRoom = null) => {
  editingReadingRoom.value = readingRoom
  if (readingRoom) {
    form.value = { ...readingRoom }
  } else {
    form.value = {
      number: null,
      floor: null,
      room_type: '',
      capacity: null,
      hourly_rate: null,
      description: ''
    }
  }
  dialog.value = true
}

const saveReadingRoom = async () => {
  try {
    saving.value = true
    if (editingReadingRoom.value) {
      await readingRoomsAPI.update(editingReadingRoom.value.id, form.value)
    } else {
      await readingRoomsAPI.create(form.value)
    }
    dialog.value = false
    loadReadingRooms()
  } catch (error) {
    console.error('Ошибка сохранения зала:', error)
  } finally {
    saving.value = false
  }
}

const deleteReadingRoom = async (id) => {
  if (confirm('Удалить зал?')) {
    try {
      await readingRoomsAPI.delete(id)
      loadReadingRooms()
    } catch (error) {
      console.error('Ошибка удаления зала:', error)
    }
  }
}

onMounted(() => {
  loadReadingRooms()
})
</script>

