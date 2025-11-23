<template>
  <div>
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="text-h4">Клиенты</h1>
      <v-btn color="primary" @click="openDialog()">Добавить</v-btn>
    </div>
    <v-data-table :headers="headers" :items="items" :loading="loading">
      <template #item.actions="{ item }">
        <v-btn icon="mdi-pencil" size="small" @click="openDialog(item)" />
        <v-btn icon="mdi-delete" size="small" color="error" @click="remove(item.id)" />
      </template>
    </v-data-table>

    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>{{ form.id ? 'Редактировать' : 'Добавить' }}</v-card-title>
        <v-card-text>
          <v-text-field v-model="form.name" label="Название" />
          <v-text-field v-model="form.contact_person" label="Контактное лицо" />
          <v-text-field v-model="form.phone" label="Телефон" />
          <v-text-field v-model="form.email" label="Email" />
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
const loading = ref(false)
const dialog = ref(false)
const form = reactive({ id: null, name: '', contact_person: '', phone: '', email: '' })

const headers = [
  { title: 'Название', key: 'name' },
  { title: 'Контакт', key: 'contact_person' },
  { title: 'Телефон', key: 'phone' },
  { title: 'Email', key: 'email' },
  { title: 'Действия', key: 'actions', sortable: false }
]

const load = async () => {
  loading.value = true
  const res = await api.get('/clients/')
  items.value = res.data.results || res.data
  loading.value = false
}

const openDialog = (item = null) => {
  Object.assign(form, item || { id: null, name: '', contact_person: '', phone: '', email: '' })
  dialog.value = true
}

const save = async () => {
  if (form.id) await api.put(`/clients/${form.id}/`, form)
  else await api.post('/clients/', form)
  dialog.value = false
  load()
}

const remove = async (id) => {
  if (confirm('Удалить?')) {
    await api.delete(`/clients/${id}/`)
    load()
  }
}

onMounted(load)
</script>
