<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const items = ref([])
const classes = ref([])
const loading = ref(false)
const dialog = ref(false)
const saving = ref(false)
const errorMessage = ref('')
const genders = [
  { title: 'Мальчик', value: 'male' },
  { title: 'Девочка', value: 'female' },
]
const edited = ref({
  id: null,
  last_name: '',
  first_name: '',
  middle_name: '',
  gender: 'male',
  school_class: null,
  is_active: true,
})
const headers = [
  { title: 'ФИО', key: 'full_name' },
  { title: 'Пол', key: 'gender' },
  { title: 'Класс', key: 'school_class_title' },
  { title: 'Активен', key: 'is_active' },
  { title: 'Действия', key: 'actions', sortable: false },
]

const displayFullName = (item) => {
  if (item.full_name) return item.full_name
  return [item.last_name, item.first_name, item.middle_name].filter(Boolean).join(' ')
}

const displayClass = (item) => item.school_class_title || item.school_class_label || '—'

const load = async () => {
  loading.value = true
  try {
    const [{ data: studs }, { data: cls }] = await Promise.all([
      api.get('/api/students/?limit=200'),
      api.get('/api/classes/?limit=200'),
    ])
    items.value = studs?.results || studs
    classes.value = (cls?.results || cls).map((c) => ({ title: c.title, value: c.id }))
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
    gender: 'male',
    school_class: null,
    is_active: true,
  }
  dialog.value = true
}
const openEdit = (item) => {
  edited.value = {
    id: item.id,
    last_name: item.last_name,
    first_name: item.first_name,
    middle_name: item.middle_name,
    gender: item.gender,
    school_class: item.school_class,
    is_active: item.is_active,
  }
  dialog.value = true
}
const save = async () => {
  saving.value = true
  errorMessage.value = ''
  try {
    if (edited.value.id) {
      await api.patch(`/api/students/${edited.value.id}/`, edited.value)
    } else {
      await api.post('/api/students/', edited.value)
    }
    dialog.value = false
    errorMessage.value = ''
    await load()
  } catch (e) {
    const data = e.response?.data
    let detail = 'Не удалось сохранить данные'
    if (typeof data === 'string') {
      detail = data.startsWith('<!DOCTYPE') || data.startsWith('<html')
        ? 'Сервер вернул HTML-ошибку. Проверьте корректность данных или логи сервера.'
        : data
    } else if (data?.detail) {
      detail = data.detail
    } else if (Array.isArray(data)) {
      detail = data.join('; ')
    } else if (data && typeof data === 'object') {
      detail = Object.values(data)
        .flat()
        .join('; ')
    }
    errorMessage.value = detail
  } finally {
    saving.value = false
  }
}
const removeItem = async (item) => {
  const name = displayFullName(item) || 'ученик'
  if (!confirm(`Удалить ученика "${name}"?`)) return
  await api.delete(`/api/students/${item.id}/`)
  await load()
}

onMounted(load)
</script>

<template>
  <v-card>
    <v-card-title class="d-flex align-center">
      <span class="text-h6">Ученики</span>
      <v-spacer />
      <v-btn color="primary" @click="openCreate">Добавить</v-btn>
    </v-card-title>
    <v-data-table :headers="headers" :items="items" :loading="loading" item-key="id">
      <template #item.full_name="{ item }">
        {{ displayFullName(item) }}
      </template>
      <template #item.gender="{ value }">
        <v-chip size="small" :color="value === 'male' ? 'blue' : 'pink'">
          {{ value === 'male' ? 'М' : 'Ж' }}
        </v-chip>
      </template>
      <template #item.is_active="{ value }">
        <v-chip size="small" :color="value ? 'green' : 'grey'">
          {{ value ? 'Да' : 'Нет' }}
        </v-chip>
      </template>
      <template #item.school_class_title="{ item }">
        {{ displayClass(item) }}
      </template>
      <template #item.actions="{ item }">
        <v-btn icon="mdi-pencil" size="small" variant="text" @click="openEdit(item)" />
        <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="removeItem(item)" />
      </template>
    </v-data-table>
  </v-card>

  <v-dialog v-model="dialog" max-width="540">
    <v-card>
      <v-card-title>{{ edited.id ? 'Редактировать ученика' : 'Новый ученик' }}</v-card-title>
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
          <v-select v-model="edited.gender" :items="genders" label="Пол" />
          <v-select v-model="edited.school_class" :items="classes" label="Класс" required />
          <v-switch v-model="edited.is_active" label="Активен" />
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

