<template>
  <h1 class="mb-4">Absences</h1>
  <v-btn color="primary" class="mb-4" @click="openNew">Add Absence</v-btn>
  <v-data-table :headers="headers" :items="items" :loading="loading" density="comfortable">
    <template #item.actions="{ item }">
      <v-btn icon="mdi-pencil" size="small" variant="text" @click="openEdit(item)" />
      <v-btn icon="mdi-delete" size="small" variant="text" color="red" @click="remove(item.id)" />
    </template>
  </v-data-table>
  <v-dialog v-model="dialog" max-width="500">
    <v-card :title="editing ? 'Edit Absence' : 'Add Absence'">
      <v-card-text>
        <v-select v-model="form.bus" :items="buses" item-title="reg_number" item-value="id" label="Bus" />
        <v-text-field v-model="form.date" label="Date" type="date" />
        <v-select v-model="form.reason" :items="reasons" item-title="text" item-value="value" label="Reason" />
        <v-textarea v-model="form.note" label="Note" rows="2" />
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
const { items, loading, create, update, remove } = useCrud('absences')
const buses = ref([])
onMounted(async () => { buses.value = (await api.get('/api/buses/')).data })
const reasons = [
  { text: 'Bus breakdown', value: 'breakdown' },
  { text: 'No driver', value: 'no_driver' },
  { text: 'Other', value: 'other' },
]
const headers = [
  { title: 'Bus', key: 'bus_reg' },
  { title: 'Date', key: 'date' },
  { title: 'Reason', key: 'reason_display' },
  { title: 'Note', key: 'note' },
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
