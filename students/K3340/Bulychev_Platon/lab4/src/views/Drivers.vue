<template>
  <h1 class="mb-4">Drivers</h1>
  <v-btn color="primary" class="mb-4" @click="openNew">Add Driver</v-btn>
  <v-data-table :headers="headers" :items="items" :loading="loading" density="comfortable">
    <template #item.actions="{ item }">
      <v-btn icon="mdi-pencil" size="small" variant="text" @click="openEdit(item)" />
      <v-btn icon="mdi-delete" size="small" variant="text" color="red" @click="remove(item.id)" />
    </template>
  </v-data-table>
  <v-dialog v-model="dialog" max-width="500">
    <v-card :title="editing ? 'Edit Driver' : 'Add Driver'">
      <v-card-text>
        <v-text-field v-model="form.first_name" label="First Name" />
        <v-text-field v-model="form.last_name" label="Last Name" />
        <v-text-field v-model="form.passport" label="Passport" />
        <v-select v-model="form.driver_class" :items="['1','2','3']" label="Class" />
        <v-text-field v-model.number="form.experience_years" label="Experience (years)" type="number" />
        <v-text-field v-model.number="form.salary" label="Salary" type="number" />
        <v-select v-model="form.bus" :items="buses" item-title="reg_number" item-value="id" label="Bus" clearable />
        <v-select v-model="form.route" :items="routes" item-title="number" item-value="id" label="Route" clearable />
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
const { items, loading, load, create, update, remove } = useCrud('drivers')
const buses = ref([])
const routes = ref([])
onMounted(async () => {
  buses.value = (await api.get('/api/buses/')).data
  routes.value = (await api.get('/api/routes/')).data
})
const headers = [
  { title: 'Last Name', key: 'last_name' },
  { title: 'First Name', key: 'first_name' },
  { title: 'Class', key: 'driver_class' },
  { title: 'Experience', key: 'experience_years' },
  { title: 'Salary', key: 'salary' },
  { title: 'Bus', key: 'bus_reg' },
  { title: 'Route', key: 'route_number' },
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
