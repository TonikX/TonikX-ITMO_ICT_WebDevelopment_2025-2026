<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const items = ref([])
const loading = ref(false)
const dialog = ref(false)
const saving = ref(false)
const errorMessage = ref('')
const edited = ref({ id: null, number: '', title: '', category: 'basic', capacity: 25 })
const categories = [
  { title: 'Базовый', value: 'basic' },
  { title: 'Профильный', value: 'profile' },
]
const headers = [
  { title: 'Номер', key: 'number' },
  { title: 'Название', key: 'title' },
  { title: 'Категория', key: 'category' },
  { title: 'Вместимость', key: 'capacity' },
  { title: 'Действия', key: 'actions', sortable: false },
]

const load = async () => {
  loading.value = true
  try {
    const { data } = await api.get('/api/classrooms/')
    items.value = data?.results || data
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  edited.value = { id: null, number: '', title: '', category: 'basic', capacity: 25 }
  dialog.value = true
}
const openEdit = (item) => {
  edited.value = { ...item }
  dialog.value = true
}
const save = async () => {
  saving.value = true
  errorMessage.value = ''
  try {
    if (edited.value.id) {
      await api.patch(`/api/classrooms/${edited.value.id}/`, edited.value)
    } else {
      await api.post('/api/classrooms/', edited.value)
    }
    dialog.value = false
    errorMessage.value = ''
    await load()
  } catch (e) {
    const data = e.response?.data
    let detail = 'Не удалось сохранить данные'
    if (typeof data === 'string') {
      detail = data.startsWith('<!DOCTYPE') || data.startsWith('<html')
        ? 'Сервер вернул HTML-ошибку. Проверьте данные или логи.'
        : data
    } else if (data?.detail) {
      detail = data.detail
    } else if (Array.isArray(data)) {
      detail = data.join('; ')
    } else if (data && typeof data === 'object') {
      detail = Object.values(data).flat().join('; ')
    }
    errorMessage.value = detail
  } finally {
    saving.value = false
  }
}
const removeItem = async (item) => {
  if (!confirm(`Удалить кабинет "${item.number}"?`)) return
  await api.delete(`/api/classrooms/${item.id}/`)
  await load()
}

onMounted(load)
</script>

<template>
  <v-card>
    <v-card-title class="d-flex align-center">
      <span class="text-h6">Кабинеты</span>
      <v-spacer />
      <v-btn color="primary" @click="openCreate">Добавить</v-btn>
    </v-card-title>
    <v-alert
      v-if="errorMessage"
      type="warning"
      variant="tonal"
      class="mx-4 mb-2"
      density="comfortable"
      closable
      @click:close="errorMessage = ''"
    >
      {{ errorMessage }}
    </v-alert>
    <v-data-table :headers="headers" :items="items" :loading="loading" item-key="id">
      <template #item.category="{ value }">
        <v-chip size="small" :color="value === 'profile' ? 'primary' : 'grey'">
          {{ value === 'profile' ? 'Профильный' : 'Базовый' }}
        </v-chip>
      </template>
      <template #item.actions="{ item }">
        <v-btn icon="mdi-pencil" size="small" variant="text" @click="openEdit(item)" />
        <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="removeItem(item)" />
      </template>
    </v-data-table>
  </v-card>

  <v-dialog v-model="dialog" max-width="520">
    <v-card>
      <v-card-title>{{ edited.id ? 'Редактировать кабинет' : 'Новый кабинет' }}</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="save">
          <v-text-field v-model="edited.number" label="Номер" required />
          <v-text-field v-model="edited.title" label="Название" />
          <v-select v-model="edited.category" :items="categories" label="Категория" />
          <v-text-field v-model.number="edited.capacity" type="number" min="1" label="Вместимость" />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" @click="dialog = false">Отмена</v-btn>
        <v-btn color="primary" :loading="saving" @click="save">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>


