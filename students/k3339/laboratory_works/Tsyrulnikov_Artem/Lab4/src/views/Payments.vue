<template>
  <div>
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="text-h4">Платежи</h1>
      <v-btn color="primary" @click="openDialog()">Добавить</v-btn>
    </div>
    <v-data-table :headers="headers" :items="items" :loading="loading">
      <template #item.order="{ item }">Заказ #{{ item.order }}</template>
      <template #item.is_paid="{ item }">
        <v-chip :color="item.is_paid ? 'success' : 'warning'">{{ item.is_paid ? 'Оплачен' : 'Не оплачен' }}</v-chip>
      </template>
      <template #item.actions="{ item }">
        <v-btn icon="mdi-pencil" size="small" @click="openDialog(item)" />
        <v-btn icon="mdi-delete" size="small" color="error" @click="remove(item.id)" />
      </template>
    </v-data-table>

    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>{{ form.id ? 'Редактировать' : 'Добавить' }}</v-card-title>
        <v-card-text>
          <v-select v-model="form.order" :items="orders" :item-title="o => `Заказ #${o.id}`" item-value="id" label="Заказ" />
          <v-text-field v-model="form.payment_date" label="Дата оплаты" type="date" />
          <v-checkbox v-model="form.is_paid" label="Оплачен" />
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
const orders = ref([])
const loading = ref(false)
const dialog = ref(false)
const form = reactive({ id: null, order: null, payment_date: '', is_paid: false })

const headers = [
  { title: 'Заказ', key: 'order' },
  { title: 'Дата выставления', key: 'issued_date' },
  { title: 'Дата оплаты', key: 'payment_date' },
  { title: 'Статус', key: 'is_paid' },
  { title: 'Действия', key: 'actions', sortable: false }
]

const load = async () => {
  loading.value = true
  const [p, o] = await Promise.all([api.get('/payments/'), api.get('/orders/')])
  items.value = p.data.results || p.data
  orders.value = o.data.results || o.data
  loading.value = false
}

const openDialog = (item = null) => {
  Object.assign(form, item || { id: null, order: null, payment_date: '', is_paid: false })
  dialog.value = true
}

const save = async () => {
  if (form.id) await api.put(`/payments/${form.id}/`, form)
  else await api.post('/payments/', form)
  dialog.value = false
  load()
}

const remove = async (id) => {
  if (confirm('Удалить?')) {
    await api.delete(`/payments/${id}/`)
    load()
  }
}

onMounted(load)
</script>
