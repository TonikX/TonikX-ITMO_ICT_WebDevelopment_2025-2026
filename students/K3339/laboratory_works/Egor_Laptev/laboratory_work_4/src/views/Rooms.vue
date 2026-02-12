<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Номера</span>
            <v-btn color="primary" @click="openDialog(null)">Добавить</v-btn>
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="items"
              :loading="loading"
              item-key="id"
            >
              <template v-slot:item.type="{ item }">
                {{ item.type?.name || '-' }}
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
        <v-card-title>{{ editingItem ? 'Редактировать' : 'Добавить' }} номер</v-card-title>
        <v-card-text>
          <v-form ref="formRef" v-model="valid" lazy-validation>
            <v-text-field
              v-model="form.number"
              label="Номер комнаты"
              :rules="[v => !!v || 'Обязательное поле']"
              variant="outlined"
            />
            <v-text-field
              v-model="form.phone"
              label="Телефон"
              variant="outlined"
            />
            <v-select
              v-model="form.type_id"
              :items="roomTypes"
              item-title="name"
              item-value="id"
              label="Тип номера"
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
const roomTypes = ref([])
const floors = ref([])
const loading = ref(false)
const dialog = ref(false)
const valid = ref(false)
const saving = ref(false)
const error = ref('')
const editingItem = ref(null)

const form = ref({
  number: '',
  phone: '',
  type_id: null,
  floor_id: null,
})

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Номер', key: 'number' },
  { title: 'Телефон', key: 'phone' },
  { title: 'Тип', key: 'type' },
  { title: 'Этаж', key: 'floor' },
  { title: 'Действия', key: 'actions', sortable: false },
]

const loadData = async () => {
  loading.value = true
  try {
    const [roomsRes, typesRes, floorsRes] = await Promise.all([
      hotelAPI.rooms.list(),
      hotelAPI.roomTypes.list(),
      hotelAPI.floors.list(),
    ])
    items.value = roomsRes.data
    roomTypes.value = typesRes.data
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
      number: item.number,
      phone: item.phone || '',
      type_id: item.type?.id,
      floor_id: item.floor?.id,
    }
  } else {
    form.value = { number: '', phone: '', type_id: null, floor_id: null }
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
      await hotelAPI.rooms.update(editingItem.value.id, form.value)
    } else {
      await hotelAPI.rooms.create(form.value)
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
  if (!confirm(`Удалить номер ${item.number}?`)) return
  try {
    await hotelAPI.rooms.delete(item.id)
    await loadData()
  } catch (err) {
    error.value = 'Ошибка при удалении'
  }
}

onMounted(() => {
  loadData()
})
</script>

