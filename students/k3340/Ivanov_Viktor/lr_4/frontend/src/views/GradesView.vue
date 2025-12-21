<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const items = ref([])
const students = ref([])
const subjects = ref([])
const teachers = ref([])
const loading = ref(false)
const dialog = ref(false)
const saving = ref(false)
const errorMessage = ref('')
const edited = ref({
  id: null,
  student: null,
  subject: null,
  quarter: 1,
  value: 5,
  comment: '',
  graded_by: null,
})
const quarters = [
  { title: 'I', value: 1 },
  { title: 'II', value: 2 },
  { title: 'III', value: 3 },
  { title: 'IV', value: 4 },
]
const headers = [
  { title: 'Ученик', key: 'student_name' },
  { title: 'Предмет', key: 'subject_name' },
  { title: 'Четверть', key: 'quarter' },
  { title: 'Оценка', key: 'value' },
  { title: 'Учитель', key: 'graded_by_name' },
  { title: 'Комментарий', key: 'comment' },
  { title: 'Действия', key: 'actions', sortable: false },
]

const load = async () => {
  loading.value = true
  try {
    const [gr, studs, sbj, tch] = await Promise.all([
      api.get('/api/grades/?limit=300'),
      api.get('/api/students/?limit=300'),
      api.get('/api/subjects/?limit=200'),
      api.get('/api/teachers/?limit=200'),
    ])
    items.value = gr.data?.results || gr.data
    students.value = (studs.data?.results || studs.data).map((s) => ({ title: s.full_name, value: s.id }))
    subjects.value = (sbj.data?.results || sbj.data).map((s) => ({ title: s.name, value: s.id }))
    teachers.value = (tch.data?.results || tch.data).map((t) => ({ title: t.full_name, value: t.id }))
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  edited.value = { id: null, student: null, subject: null, quarter: 1, value: 5, comment: '', graded_by: null }
  dialog.value = true
}
const openEdit = (item) => {
  edited.value = {
    id: item.id,
    student: item.student,
    subject: item.subject,
    quarter: item.quarter,
    value: item.value,
    comment: item.comment || '',
    graded_by: item.graded_by || null,
  }
  dialog.value = true
}
const save = async () => {
  saving.value = true
  errorMessage.value = ''
  try {
    if (edited.value.id) {
      await api.patch(`/api/grades/${edited.value.id}/`, edited.value)
    } else {
      await api.post('/api/grades/', edited.value)
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
  const subj = item.subject_name || 'предмет'
  const student = item.student_name || 'ученик'
  const val = item.value ?? '?'
  if (!confirm(`Удалить оценку ${val} по ${subj} (${student})?`)) return
  await api.delete(`/api/grades/${item.id}/`)
  await load()
}

onMounted(load)
</script>

<template>
  <v-card>
    <v-card-title class="d-flex align-center">
      <span class="text-h6">Оценки</span>
      <v-spacer />
      <v-btn color="primary" @click="openCreate">Добавить</v-btn>
    </v-card-title>
    <v-data-table :headers="headers" :items="items" :loading="loading" item-key="id">
      <template #item.quarter="{ value }">
        {{ ['I', 'II', 'III', 'IV'][value - 1] || value }}
      </template>
      <template #item.actions="{ item }">
        <v-btn icon="mdi-pencil" size="small" variant="text" @click="openEdit(item)" />
        <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="removeItem(item)" />
      </template>
    </v-data-table>
  </v-card>

  <v-dialog v-model="dialog" max-width="560">
    <v-card>
      <v-card-title>{{ edited.id ? 'Редактировать оценку' : 'Новая оценка' }}</v-card-title>
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
          <v-select v-model="edited.student" :items="students" label="Ученик" required />
          <v-select v-model="edited.subject" :items="subjects" label="Предмет" required />
          <v-select v-model="edited.quarter" :items="quarters" label="Четверть" />
          <v-text-field v-model.number="edited.value" type="number" min="2" max="5" label="Оценка" />
          <v-select v-model="edited.graded_by" :items="teachers" label="Учитель" clearable />
          <v-textarea v-model="edited.comment" label="Комментарий" rows="2" />
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


