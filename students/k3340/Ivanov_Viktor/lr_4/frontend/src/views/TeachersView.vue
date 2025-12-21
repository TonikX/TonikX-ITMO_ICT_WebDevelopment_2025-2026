<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const items = ref([])
const classrooms = ref([])
const loading = ref(false)
const dialog = ref(false)
const saving = ref(false)
const errorMessage = ref('')
const edited = ref({
  id: null,
  last_name: '',
  first_name: '',
  middle_name: '',
  email: '',
  phone: '',
  assigned_room: null,
})
const headers = [
  { title: 'ФИО', key: 'full_name' },
  { title: 'Email', key: 'email' },
  { title: 'Телефон', key: 'phone' },
  { title: 'Кабинет', key: 'assigned_room_number' },
  { title: 'Действия', key: 'actions', sortable: false },
]

const load = async () => {
  loading.value = true
  try {
    const [{ data: tchs }, { data: rooms }] = await Promise.all([
      api.get('/api/teachers/?limit=200'),
      api.get('/api/classrooms/?limit=200'),
    ])
    items.value = tchs?.results || tchs
    classrooms.value = (rooms?.results || rooms).map((r) => ({ title: r.number, value: r.id }))
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  edited.value = {
    id: null,
    last_name: '',
    first_name: '',
    middle_name: '',
    email: '',
    phone: '',
    assigned_room: null,
  }
  dialog.value = true
}
const openEdit = (item) => {
  edited.value = {
    id: item.id,
    last_name: item.last_name,
    first_name: item.first_name,
    middle_name: item.middle_name,
    email: item.email,
    phone: item.phone,
    assigned_room: item.assigned_room || null,
  }
  dialog.value = true
}
const save = async () => {
  saving.value = true
  errorMessage.value = ''
  try {
    if (edited.value.id) {
      await api.patch(`/api/teachers/${edited.value.id}/`, edited.value)
    } else {
      await api.post('/api/teachers/', edited.value)
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
  if (!confirm(`Удалить учителя "${item.full_name}"?`)) return
  await api.delete(`/api/teachers/${item.id}/`)
  await load()
}

onMounted(load)
</script>

<template>
  <v-card>
    <v-card-title class="d-flex align-center">
      <span class="text-h6">Учителя</span>
      <v-spacer />
      <v-btn color="primary" @click="openCreate">Добавить</v-btn>
    </v-card-title>
    <v-data-table :headers="headers" :items="items" :loading="loading" item-key="id">
      <template #item.full_name="{ item }">
        {{ item.full_name }}
      </template>
      <template #item.assigned_room_number="{ item }">
        {{ item.assigned_room_number || '—' }}
      </template>
      <template #item.actions="{ item }">
        <v-btn icon="mdi-pencil" size="small" variant="text" @click="openEdit(item)" />
        <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="removeItem(item)" />
      </template>
    </v-data-table>
  </v-card>

  <v-dialog v-model="dialog" max-width="540">
    <v-card>
      <v-card-title>{{ edited.id ? 'Редактировать учителя' : 'Новый учитель' }}</v-card-title>
      <v-card-text>
        <v-alert
          v-if="errorMessage"
          type="error"
          variant="tonal"
          density="compact"
          class="mb-3"
          closable
          @click:close="errorMessage = ''"
        >
          {{ errorMessage }}
        </v-alert>
        <v-form @submit.prevent="save">
          <v-text-field v-model="edited.last_name" label="Фамилия" required />
          <v-text-field v-model="edited.first_name" label="Имя" required />
          <v-text-field v-model="edited.middle_name" label="Отчество" />
          <v-text-field v-model="edited.email" label="Email" type="email" />
          <v-text-field v-model="edited.phone" label="Телефон" />
          <v-select v-model="edited.assigned_room" :items="classrooms" label="Закреплённый кабинет" clearable />
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


