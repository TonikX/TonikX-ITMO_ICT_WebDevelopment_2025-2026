<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Типы номеров</span>
            <div>
              <v-btn color="info" @click="loadStats" class="mr-2">Статистика</v-btn>
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
        <v-card-title>{{ editingItem ? 'Редактировать' : 'Добавить' }} тип номера</v-card-title>
        <v-card-text>
          <v-form ref="formRef" v-model="valid" lazy-validation>
            <v-text-field
              v-model="form.name"
              label="Название"
              :rules="[v => !!v || 'Обязательное поле']"
              variant="outlined"
            />
            <v-text-field
              v-model.number="form.capacity"
              label="Вместимость"
              type="number"
              :rules="[v => v !== null && v !== undefined && v > 0 || 'Должно быть больше нуля']"
              variant="outlined"
            />
            <v-text-field
              v-model.number="form.price_per_day"
              label="Цена за день"
              type="number"
              step="0.01"
              :rules="[v => v !== null && v !== undefined && v > 0 || 'Должно быть больше нуля']"
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

    <v-dialog v-model="statsDialog" max-width="600">
      <v-card>
        <v-card-title>Статистика по типам номеров</v-card-title>
        <v-card-text>
          <v-data-table
            :headers="statsHeaders"
            :items="stats"
            :loading="statsLoading"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="statsDialog = false">Закрыть</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { hotelAPI } from '../services/api'

const items = ref([])
const stats = ref([])
const loading = ref(false)
const statsLoading = ref(false)
const dialog = ref(false)
const statsDialog = ref(false)
const valid = ref(false)
const saving = ref(false)
const error = ref('')
const editingItem = ref(null)

const form = ref({
  name: '',
  capacity: null,
  price_per_day: null,
})

const formRef = ref(null)

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Название', key: 'name' },
  { title: 'Вместимость', key: 'capacity' },
  { title: 'Цена за день', key: 'price_per_day' },
  { title: 'Действия', key: 'actions', sortable: false },
]

const statsHeaders = [
  { title: 'ID', key: 'id' },
  { title: 'Название', key: 'name' },
  { title: 'Вместимость', key: 'capacity' },
  { title: 'Цена за день', key: 'price_per_day' },
  { title: 'Количество номеров', key: 'rooms_count' },
]

const loadData = async () => {
  loading.value = true
  try {
    const response = await hotelAPI.roomTypes.list()
    items.value = response.data
  } catch (err) {
    error.value = 'Ошибка при загрузке данных'
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  statsLoading.value = true
  statsDialog.value = true
  try {
    const response = await hotelAPI.roomTypes.stats()
    stats.value = response.data
  } catch (err) {
    error.value = 'Ошибка при загрузке статистики'
  } finally {
    statsLoading.value = false
  }
}

const openDialog = (item) => {
  editingItem.value = item
  if (item) {
    form.value = { ...item }
  } else {
    form.value = { name: '', capacity: null, price_per_day: null }
  }
  error.value = ''
  dialog.value = true
}

const saveItem = async () => {
  error.value = ''
  
  if (!valid.value) {
    return
  }

  saving.value = true
  try {
    if (editingItem.value) {
      await hotelAPI.roomTypes.update(editingItem.value.id, form.value)
    } else {
      await hotelAPI.roomTypes.create(form.value)
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
  if (!confirm(`Удалить тип номера "${item.name}"?`)) return
  try {
    await hotelAPI.roomTypes.delete(item.id)
    await loadData()
  } catch (err) {
    error.value = 'Ошибка при удалении'
  }
}

onMounted(() => {
  loadData()
})
</script>

