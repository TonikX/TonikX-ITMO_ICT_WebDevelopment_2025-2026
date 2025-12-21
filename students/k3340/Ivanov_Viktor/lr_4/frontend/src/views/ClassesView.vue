<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const items = ref([])
const teachers = ref([])
const loading = ref(false)
const dialog = ref(false)
const saving = ref(false)
const errorMessage = ref('')
const edited = ref({ id: null, title: '', grade_level: 1, profile: 'basic', homeroom_teacher: null })
const profiles = [
  { title: 'Базовый', value: 'basic' },
  { title: 'Профильный', value: 'profile' },
]
const headers = [
  { title: 'Название', key: 'title' },
  { title: 'Класс', key: 'grade_level' },
  { title: 'Профиль', key: 'profile' },
  { title: 'Классный руководитель', key: 'homeroom_teacher_name' },
  { title: 'Действия', key: 'actions', sortable: false },
]

const displayProfile = (value) => (value === 'profile' ? 'Профильный' : 'Базовый')
const displayTitle = (item) => item.title || 'класс'

const load = async () => {
  loading.value = true
  try {
    const [{ data: classes }, { data: tchs }] = await Promise.all([
      api.get('/api/classes/'),
      api.get('/api/teachers/?limit=100'),
    ])
    items.value = classes?.results || classes
    teachers.value = (tchs?.results || tchs).map((t) => ({ title: t.full_name, value: t.id }))
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  edited.value = { id: null, title: '', grade_level: 1, profile: 'basic', homeroom_teacher: null }
  dialog.value = true
}
const openEdit = (item) => {
  edited.value = { id: item.id, title: item.title, grade_level: item.grade_level, profile: item.profile, homeroom_teacher: item.homeroom_teacher || null }
  dialog.value = true
}
const save = async () => {
  saving.value = true
  try {
    if (edited.value.id) {
      await api.patch(`/api/classes/${edited.value.id}/`, edited.value)
    } else {
      await api.post('/api/classes/', edited.value)
    }
    dialog.value = false
    await load()
  } finally {
    saving.value = false
  }
}
const removeItem = async (item) => {
  const title = displayTitle(item)
  if (!confirm(`Удалить класс "${title}"?`)) return
  errorMessage.value = ''
  try {
    await api.delete(`/api/classes/${item.id}/`)
    await load()
  } catch (e) {
    const detail = e.response?.data?.detail || 'Невозможно удалить класс: есть связанные записи (например, ученики).'
    errorMessage.value = detail
  }
}

onMounted(load)
</script>

<template>
  <v-card>
    <v-card-title class="d-flex align-center">
      <span class="text-h6">Классы</span>
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
      <template #item.profile="{ value }">
        <v-chip size="small" :color="value === 'profile' ? 'primary' : 'grey'">
          {{ displayProfile(value) }}
        </v-chip>
      </template>
      <template #item.homeroom_teacher_name="{ item }">
        {{ item.homeroom_teacher_name || '—' }}
      </template>
      <template #item.actions="{ item }">
        <v-btn icon="mdi-pencil" size="small" variant="text" @click="openEdit(item)" />
        <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="removeItem(item)" />
      </template>
    </v-data-table>
  </v-card>

  <v-dialog v-model="dialog" max-width="520">
    <v-card>
      <v-card-title>{{ edited.id ? 'Редактировать класс' : 'Новый класс' }}</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="save">
          <v-text-field v-model="edited.title" label="Обозначение (например 10А)" required />
          <v-text-field v-model.number="edited.grade_level" type="number" min="1" max="11" label="Параллель (1-11)" required />
          <v-select v-model="edited.profile" :items="profiles" label="Профиль" />
          <v-select
            v-model="edited.homeroom_teacher"
            :items="teachers"
            label="Классный руководитель"
            clearable
          />
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


