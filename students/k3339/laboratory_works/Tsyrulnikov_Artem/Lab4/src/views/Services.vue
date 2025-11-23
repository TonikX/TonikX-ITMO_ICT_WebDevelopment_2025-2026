<template>
  <div>
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="text-h4">Услуги</h1>
      <v-btn color="primary" @click="openDialog()">Добавить</v-btn>
    </div>
    <v-data-table :headers="headers" :items="items" :loading="loading">
      <template #item.category="{ item }">{{ categories.find(c => c.id === item.category)?.name }}</template>
      <template #item.actions="{ item }">
        <v-btn icon="mdi-pencil" size="small" @click="openDialog(item)" />
        <v-btn icon="mdi-delete" size="small" color="error" @click="remove(item.id)" />
      </template>
    </v-data-table>

    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>{{ form.id ? 'Редактировать' : 'Добавить' }}</v-card-title>
        <v-card-text>
          <v-select v-model="form.category" :items="categories" item-title="name" item-value="id" label="Категория" />
          <v-text-field v-model="form.name" label="Название" />
          <v-text-field v-model="form.price" label="Цена" type="number" />
          <v-text-field v-model="form.unit" label="Единица" />
          <v-textarea v-model="form.materials" label="Материалы" rows="2" />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="save">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '@/api'

const items = ref([])
const categories = ref([])
const loading = ref(false)
const dialog = ref(false)
const form = reactive({ id: null, category: null, name: '', price: '', unit: '', materials: '' })

const headers = [
  { title: 'Категория', key: 'category' },
  { title: 'Название', key: 'name' },
  { title: 'Цена', key: 'price' },
  { title: 'Единица', key: 'unit' },
  { title: 'Действия', key: 'actions', sortable: false }
]

const load = async () => {
  loading.value = true
  const [s, c] = await Promise.all([api.get('/services/'), api.get('/categories/')])
  items.value = s.data.results || s.data
  categories.value = c.data.results || c.data
  loading.value = false
}

const openDialog = (item = null) => {
  Object.assign(form, item || { id: null, category: null, name: '', price: '', unit: '', materials: '' })
  dialog.value = true
}

const save = async () => {
  if (form.id) await api.put(`/services/${form.id}/`, form)
  else await api.post('/services/', form)
  dialog.value = false
  load()
}

const remove = async (id) => {
  if (confirm('Удалить?')) {
    await api.delete(`/services/${id}/`)
    load()
  }
}

onMounted(load)
</script>
