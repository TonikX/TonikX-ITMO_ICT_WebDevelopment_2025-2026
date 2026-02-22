<template>
  <h1 class="mb-4">Schedules</h1>
  <v-btn color="primary" class="mb-4" @click="openNew">Add Schedule</v-btn>
  <v-data-table :headers="headers" :items="items" :loading="loading" density="comfortable">
    <template #item.actions="{ item }">
      <v-btn icon="mdi-pencil" size="small" variant="text" @click="openEdit(item)" />
      <v-btn icon="mdi-delete" size="small" variant="text" color="red" @click="remove(item.id)" />
    </template>
  </v-data-table>
  <v-dialog v-model="dialog" max-width="500">
    <v-card :title="editing ? 'Edit Schedule' : 'Add Schedule'">
      <v-card-text>
        <v-select v-model="form.driver" :items="drivers" :item-title="d => d.last_name + ' ' + d.first_name" item-value="id" label="Driver" />
        <v-select v-model="form.bus" :items="buses" item-title="reg_number" item-value="id" label="Bus" />
        <v-select v-model="form.route" :items="routes" item-title="number" item-value="id" label="Route" />
        <v-text-field v-model="form.date" label="Date" type="date" />
        <v-text-field v-model="form.shift_start" label="Shift Start" type="time" />
        <v-text-field v-model="form.shift_end" label="Shift End" type="time" />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn @click="dialog = false">Cancel</v-btn>
        <v-btn color="primary" @click="save">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCrud } from '../composables/useCrud'
import api from '../api'
const { items, loading, create, update, remove } = useCrud('schedules')
const drivers = ref([])
const buses = ref([])
const routes = ref([])
onMounted(async () => {
  drivers.value = (await api.get('/api/drivers/')).data
  buses.value = (await api.get('/api/buses/')).data
  routes.value = (await api.get('/api/routes/')).data
})
const headers = [
  { title: 'Driver', key: 'driver_name' },
  { title: 'Bus', key: 'bus_reg' },
  { title: 'Route', key: 'route_number' },
  { title: 'Date', key: 'date' },
  { title: 'Start', key: 'shift_start' },
  { title: 'End', key: 'shift_end' },
  { title: '', key: 'actions', sortable: false },
]
const dialog = ref(false)
const editing = ref(null)
const form = ref({})
const openNew = () => { form.value = {}; editing.value = null; dialog.value = true }
const openEdit = (item) => { form.value = { ...item }; editing.value = item.id; dialog.value = true }
const save = async () => {
  editing.value ? await update(editing.value, form.value) : await create(form.value)
  dialog.value = false
}
</script>
