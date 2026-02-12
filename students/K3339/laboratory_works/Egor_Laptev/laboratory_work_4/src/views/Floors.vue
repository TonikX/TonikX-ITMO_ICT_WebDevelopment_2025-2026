<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Этажи</span>
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
        <v-card-title>{{ editingItem ? 'Редактировать' : 'Добавить' }} этаж</v-card-title>
        <v-card-text>
          <v-form ref="formRef" v-model="valid" lazy-validation>
            <v-text-field
              v-model.number="form.number"
              label="Номер этажа"
              type="number"
              :rules="[v => v !== null && v !== undefined && v > 0 || 'Номер должен быть положительным']"
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
        <v-card-title>Статистика по этажам</v-card-title>
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
  number: null,
})

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Номер', key: 'number' },
  { title: 'Действия', key: 'actions', sortable: false },
]

const statsHeaders = [
  { title: 'ID', key: 'id' },
  { title: 'Номер', key: 'number' },
  { title: 'Количество номеров', key: 'rooms_count' },
  { title: 'Количество уборок', key: 'cleaning_count' },
]

const loadData = async () => {
  loading.value = true
  try {
    const response = await hotelAPI.floors.list()
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
    const response = await hotelAPI.floors.stats()
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
    form.value = { number: null }
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
      await hotelAPI.floors.update(editingItem.value.id, form.value)
    } else {
      await hotelAPI.floors.create(form.value)
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
  if (!confirm(`Удалить этаж ${item.number}?`)) return
  try {
    await hotelAPI.floors.delete(item.id)
    await loadData()
  } catch (err) {
    error.value = 'Ошибка при удалении'
  }
}

onMounted(() => {
  loadData()
})
</script>

