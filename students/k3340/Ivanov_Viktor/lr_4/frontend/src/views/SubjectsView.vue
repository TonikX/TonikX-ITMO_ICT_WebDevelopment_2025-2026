<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const items = ref([])
const loading = ref(false)
const dialog = ref(false)
const saving = ref(false)
const edited = ref({ id: null, code: '', name: '', category: 'basic', description: '' })
const categories = [
  { title: 'Общая', value: 'basic' },
  { title: 'Профильная', value: 'profile' },
]
const headers = [
  { title: 'Код', key: 'code' },
  { title: 'Название', key: 'name' },
  { title: 'Категория', key: 'category' },
  { title: 'Описание', key: 'description' },
  { title: 'Действия', key: 'actions', sortable: false },
]
const load = async () => {
  loading.value = true
  try {
    const { data } = await api.get('/api/subjects/')
    items.value = data?.results || data
  } finally {
    loading.value = false
  }
}
const openCreate = () => {
  edited.value = { id: null, code: '', name: '', category: 'basic', description: '' }
  dialog.value = true
}
const openEdit = (item) => {
  edited.value = { ...item }
  dialog.value = true
}
const save = async () => {
  saving.value = true
  try {
    if (edited.value.id) {
      await api.patch(`/api/subjects/${edited.value.id}/`, edited.value)
    } else {
      await api.post('/api/subjects/', edited.value)
    }
    dialog.value = false
    await load()
  } finally {
    saving.value = false
  }
}
const removeItem = async (item) => {
  if (!confirm(`Удалить предмет "${item.name}"?`)) return
  await api.delete(`/api/subjects/${item.id}/`)
  await load()
}

onMounted(load)
</script>

<template>
  <v-row>
    <v-col cols="12">
      <v-card>
        <v-card-title class="d-flex align-center">
          <span class="text-h6">Предметы</span>
          <v-spacer />
          <v-btn color="primary" @click="openCreate">Добавить</v-btn>
        </v-card-title>
        <v-data-table :headers="headers" :items="items" :loading="loading" item-key="id">
          <template #item.category="{ value }">
            <v-chip size="small" :color="value === 'profile' ? 'primary' : 'grey'">
              {{ value === 'profile' ? 'Профильная' : 'Общая' }}
            </v-chip>
          </template>
          <template #item.actions="{ item }">
            <v-btn icon="mdi-pencil" size="small" variant="text" @click="openEdit(item)" />
            <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="removeItem(item)" />
          </template>
        </v-data-table>
      </v-card>
    </v-col>
  </v-row>

  <v-dialog v-model="dialog" max-width="520">
    <v-card>
      <v-card-title>{{ edited.id ? 'Редактировать предмет' : 'Новый предмет' }}</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="save">
          <v-text-field v-model="edited.code" label="Код" required />
          <v-text-field v-model="edited.name" label="Название" required />
          <v-select v-model="edited.category" :items="categories" label="Категория" />
          <v-textarea v-model="edited.description" label="Описание" rows="2" />
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


