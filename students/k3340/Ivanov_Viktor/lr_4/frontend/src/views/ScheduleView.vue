<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const items = ref([])
const classes = ref([])
const subjects = ref([])
const teachers = ref([])
const rooms = ref([])
const loading = ref(false)
const dialog = ref(false)
const saving = ref(false)
const errorMessage = ref('')
const edited = ref({
  id: null,
  school_class: null,
  subject: null,
  teacher: null,
  room: null,
  weekday: 1,
  lesson_number: 1,
})
const weekdays = [
  { title: 'Пн', value: 1 },
  { title: 'Вт', value: 2 },
  { title: 'Ср', value: 3 },
  { title: 'Чт', value: 4 },
  { title: 'Пт', value: 5 },
  { title: 'Сб', value: 6 },
]
const headers = [
  { title: 'Класс', key: 'school_class_title' },
  { title: 'День', key: 'weekday' },
  { title: 'Урок', key: 'lesson_number' },
  { title: 'Предмет', key: 'subject_name' },
  { title: 'Учитель', key: 'teacher_name' },
  { title: 'Кабинет', key: 'room_number' },
  { title: 'Действия', key: 'actions', sortable: false },
]

const load = async () => {
  loading.value = true
  try {
    const [sched, cls, sbj, tch, rms] = await Promise.all([
      api.get('/api/schedule/?limit=500'),
      api.get('/api/classes/?limit=200'),
      api.get('/api/subjects/?limit=200'),
      api.get('/api/teachers/?limit=200'),
      api.get('/api/classrooms/?limit=200'),
    ])
    items.value = sched.data?.results || sched.data
    classes.value = (cls.data?.results || cls.data).map((c) => ({ title: c.title, value: c.id }))
    subjects.value = (sbj.data?.results || sbj.data).map((s) => ({ title: s.name, value: s.id }))
    teachers.value = (tch.data?.results || tch.data).map((t) => ({ title: t.full_name, value: t.id }))
    rooms.value = (rms.data?.results || rms.data).map((r) => ({ title: r.number, value: r.id }))
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  edited.value = { id: null, school_class: null, subject: null, teacher: null, room: null, weekday: 1, lesson_number: 1 }
  dialog.value = true
}
const openEdit = (item) => {
  edited.value = {
    id: item.id,
    school_class: item.school_class,
    subject: item.subject,
    teacher: item.teacher,
    room: item.room,
    weekday: item.weekday,
    lesson_number: item.lesson_number,
  }
  dialog.value = true
}
const save = async () => {
  saving.value = true
  errorMessage.value = ''
  try {
    if (edited.value.id) {
      await api.patch(`/api/schedule/${edited.value.id}/`, edited.value)
    } else {
      await api.post('/api/schedule/', edited.value)
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
const lessonLabel = (item) => {
  const cls = item.school_class_title || 'класс'
  const subj = item.subject_name || 'предмет'
  const num = item.lesson_number ?? '?'
  return `${cls} • ${subj} • урок ${num}`
}

const removeItem = async (item) => {
  const label = lessonLabel(item)
  if (!confirm(`Удалить урок ${label}?`)) return
  await api.delete(`/api/schedule/${item.id}/`)
  await load()
}

onMounted(load)
</script>

<template>
  <v-card>
    <v-card-title class="d-flex align-center">
      <span class="text-h6">Расписание</span>
      <v-spacer />
      <v-btn color="primary" @click="openCreate">Добавить</v-btn>
    </v-card-title>
    <v-data-table :headers="headers" :items="items" :loading="loading" item-key="id">
      <template #item.weekday="{ value }">
        {{ weekdays.find((d) => d.value === value)?.title || value }}
      </template>
      <template #item.actions="{ item }">
        <v-btn icon="mdi-pencil" size="small" variant="text" @click="openEdit(item)" />
        <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="removeItem(item)" />
      </template>
    </v-data-table>
  </v-card>

  <v-dialog v-model="dialog" max-width="560">
    <v-card>
      <v-card-title>{{ edited.id ? 'Редактировать урок' : 'Новый урок' }}</v-card-title>
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
          <v-select v-model="edited.school_class" :items="classes" label="Класс" required />
          <v-select v-model="edited.subject" :items="subjects" label="Предмет" required />
          <v-select v-model="edited.teacher" :items="teachers" label="Учитель" required />
          <v-select v-model="edited.room" :items="rooms" label="Кабинет" clearable />
          <v-select v-model="edited.weekday" :items="weekdays" label="День недели" />
          <v-text-field v-model.number="edited.lesson_number" type="number" min="1" max="10" label="Номер урока" />
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


