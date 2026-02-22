<template>
  <h1 class="mb-4">Routes</h1>
  <v-btn color="primary" class="mb-4" @click="openNew">Add Route</v-btn>
  <v-data-table :headers="headers" :items="items" :loading="loading" density="comfortable">
    <template #item.actions="{ item }">
      <v-btn icon="mdi-pencil" size="small" variant="text" @click="openEdit(item)" />
      <v-btn icon="mdi-delete" size="small" variant="text" color="red" @click="remove(item.id)" />
    </template>
  </v-data-table>
  <v-dialog v-model="dialog" max-width="500">
    <v-card :title="editing ? 'Edit Route' : 'Add Route'">
      <v-card-text>
        <v-text-field v-model="form.number" label="Number" />
        <v-text-field v-model="form.start_point" label="Start Point" />
        <v-text-field v-model="form.end_point" label="End Point" />
        <v-text-field v-model="form.start_time" label="Start Time" type="time" />
        <v-text-field v-model="form.end_time" label="End Time" type="time" />
        <v-text-field v-model.number="form.interval_minutes" label="Interval (min)" type="number" />
        <v-text-field v-model.number="form.duration_minutes" label="Duration (min)" type="number" />
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
import { ref } from 'vue'
import { useCrud } from '../composables/useCrud'
const { items, loading, create, update, remove } = useCrud('routes')
const headers = [
  { title: '#', key: 'number' },
  { title: 'From', key: 'start_point' },
  { title: 'To', key: 'end_point' },
  { title: 'Start', key: 'start_time' },
  { title: 'End', key: 'end_time' },
  { title: 'Interval', key: 'interval_minutes' },
  { title: 'Duration', key: 'duration_minutes' },
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
