<template>
  <div>
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="text-h4">Заказы</h1>
      <v-btn color="primary" @click="openDialog()">Добавить</v-btn>
    </div>
    <v-data-table :headers="headers" :items="items" :loading="loading">
      <template #item.client="{ item }">{{ clients.find(c => c.id === item.client)?.name }}</template>
      <template #item.service="{ item }">{{ services.find(s => s.id === item.service)?.name }}</template>
      <template #item.executor="{ item }">{{ employees.find(e => e.id === item.executor)?.last_name }}</template>
      <template #item.actions="{ item }">
        <v-btn icon="mdi-pencil" size="small" @click="openDialog(item)" />
        <v-btn icon="mdi-delete" size="small" color="error" @click="remove(item.id)" />
      </template>
    </v-data-table>

    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>{{ form.id ? 'Редактировать' : 'Добавить' }}</v-card-title>
        <v-card-text>
          <v-select v-model="form.client" :items="clients" item-title="name" item-value="id" label="Клиент" />
          <v-select v-model="form.service" :items="services" item-title="name" item-value="id" label="Услуга" />
          <v-select v-model="form.executor" :items="employees" :item-title="e => `${e.last_name} ${e.first_name}`" item-value="id" label="Исполнитель" />
          <v-text-field v-model="form.quantity" label="Количество" type="number" />
          <v-text-field v-model="form.total_cost" label="Стоимость" type="number" />
          <v-select v-model="form.status" :items="statuses" label="Статус" />
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
const clients = ref([])
const services = ref([])
const employees = ref([])
const loading = ref(false)
const dialog = ref(false)
const statuses = ['new', 'in_progress', 'completed']
const form = reactive({ id: null, client: null, service: null, executor: null, quantity: 1, total_cost: '', status: 'new' })

const headers = [
  { title: 'Клиент', key: 'client' },
  { title: 'Услуга', key: 'service' },
  { title: 'Исполнитель', key: 'executor' },
  { title: 'Кол-во', key: 'quantity' },
  { title: 'Стоимость', key: 'total_cost' },
  { title: 'Статус', key: 'status' },
  { title: 'Действия', key: 'actions', sortable: false }
]

const load = async () => {
  loading.value = true
  const [o, c, s, e] = await Promise.all([
    api.get('/orders/'), api.get('/clients/'), api.get('/services/'), api.get('/employees/')
  ])
  items.value = o.data.results || o.data
  clients.value = c.data.results || c.data
  services.value = s.data.results || s.data
  employees.value = e.data.results || e.data
  loading.value = false
}

const openDialog = (item = null) => {
  Object.assign(form, item || { id: null, client: null, service: null, executor: null, quantity: 1, total_cost: '', status: 'new' })
  dialog.value = true
}

const save = async () => {
  if (form.id) await api.put(`/orders/${form.id}/`, form)
  else await api.post('/orders/', form)
  dialog.value = false
  load()
}

const remove = async (id) => {
  if (confirm('Удалить?')) {
    await api.delete(`/orders/${id}/`)
    load()
  }
}

onMounted(load)
</script>
