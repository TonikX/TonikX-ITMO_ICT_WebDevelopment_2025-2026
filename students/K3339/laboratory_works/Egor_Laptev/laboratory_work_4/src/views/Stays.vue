<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Проживания</span>
            <div>
              <v-btn color="info" @click="loadSummary" class="mr-2">Сводка</v-btn>
              <v-btn color="primary" @click="openDialog(null)">Добавить</v-btn>
            </div>
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="items"
              :loading="loading"
              item-key="id"
            >
              <template v-slot:item.guest="{ item }">
                {{ item.guest ? `${item.guest.last_name} ${item.guest.first_name}` : '-' }}
              </template>
              <template v-slot:item.room="{ item }">
                {{ item.room?.number || '-' }}
              </template>
              <template v-slot:item.check_in="{ item }">
                {{ formatDate(item.check_in) }}
              </template>
              <template v-slot:item.check_out="{ item }">
                {{ formatDate(item.check_out) }}
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
        <v-card-title>{{ editingItem ? 'Редактировать' : 'Добавить' }} проживание</v-card-title>
        <v-card-text>
          <v-form ref="formRef" v-model="valid" lazy-validation>
            <v-select
              v-model="form.guest_id"
              :items="guests"
              item-title="display"
              item-value="id"
              label="Гость"
              :rules="[v => !!v || 'Обязательное поле']"
              variant="outlined"
            />
            <v-select
              v-model="form.room_id"
              :items="rooms"
              item-title="number"
              item-value="id"
              label="Номер"
              :rules="[v => !!v || 'Обязательное поле']"
              variant="outlined"
            />
            <v-text-field
              v-model="form.check_in"
              label="Дата заезда"
              type="date"
              :rules="[v => !!v || 'Обязательное поле']"
              variant="outlined"
            />
            <v-text-field
              v-model="form.check_out"
              label="Дата выезда"
              type="date"
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

    <v-dialog v-model="summaryDialog" max-width="500">
      <v-card>
        <v-card-title>Сводка по проживаниям</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="summaryDate"
            label="Дата"
            type="date"
            variant="outlined"
            class="mb-3"
          />
          <v-btn @click="loadSummary" :loading="summaryLoading" class="mb-3">Загрузить</v-btn>
          <div v-if="summary">
            <v-list>
              <v-list-item>
                <v-list-item-title>Дата</v-list-item-title>
                <v-list-item-subtitle>{{ summary.date }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Всего проживаний</v-list-item-title>
                <v-list-item-subtitle>{{ summary.total_stays }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Активных сейчас</v-list-item-title>
                <v-list-item-subtitle>{{ summary.active_now }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Предстоящих</v-list-item-title>
                <v-list-item-subtitle>{{ summary.upcoming }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Активных номеров</v-list-item-title>
                <v-list-item-subtitle>{{ summary.active_rooms }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="summaryDialog = false">Закрыть</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { hotelAPI } from '../services/api'

const items = ref([])
const guests = ref([])
const rooms = ref([])
const loading = ref(false)
const summaryLoading = ref(false)
const dialog = ref(false)
const summaryDialog = ref(false)
const valid = ref(false)
const saving = ref(false)
const error = ref('')
const editingItem = ref(null)
const summary = ref(null)
const summaryDate = ref(new Date().toISOString().split('T')[0])

const form = ref({
  guest_id: null,
  room_id: null,
  check_in: '',
  check_out: '',
})

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Гость', key: 'guest' },
  { title: 'Номер', key: 'room' },
  { title: 'Заезд', key: 'check_in' },
  { title: 'Выезд', key: 'check_out' },
  { title: 'Действия', key: 'actions', sortable: false },
]

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('ru-RU')
}

const loadData = async () => {
  loading.value = true
  try {
    const [staysRes, guestsRes, roomsRes] = await Promise.all([
      hotelAPI.stays.list(),
      hotelAPI.guests.list(),
      hotelAPI.rooms.list(),
    ])
    items.value = staysRes.data
    guests.value = guestsRes.data.map(g => ({
      ...g,
      display: `${g.last_name} ${g.first_name} (${g.passport_number})`
    }))
    rooms.value = roomsRes.data
  } catch (err) {
    error.value = 'Ошибка при загрузке данных'
  } finally {
    loading.value = false
  }
}

const loadSummary = async () => {
  summaryLoading.value = true
  summaryDialog.value = true
  try {
    const response = await hotelAPI.stays.summary(summaryDate.value)
    summary.value = response.data
  } catch (err) {
    error.value = 'Ошибка при загрузке сводки'
  } finally {
    summaryLoading.value = false
  }
}

const openDialog = (item) => {
  editingItem.value = item
  if (item) {
    form.value = {
      guest_id: item.guest?.id,
      room_id: item.room?.id,
      check_in: item.check_in,
      check_out: item.check_out,
    }
  } else {
    form.value = {
      guest_id: null,
      room_id: null,
      check_in: '',
      check_out: '',
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
      await hotelAPI.stays.update(editingItem.value.id, form.value)
    } else {
      await hotelAPI.stays.create(form.value)
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
  if (!confirm('Удалить проживание?')) return
  try {
    await hotelAPI.stays.delete(item.id)
    await loadData()
  } catch (err) {
    error.value = 'Ошибка при удалении'
  }
}

onMounted(() => {
  loadData()
})
</script>

