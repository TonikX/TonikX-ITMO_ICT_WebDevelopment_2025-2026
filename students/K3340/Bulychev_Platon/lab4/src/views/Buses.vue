<template>
  <h1 class="mb-4">Buses</h1>
  <v-btn color="primary" class="mb-4" @click="openNew">Add Bus</v-btn>
  <v-data-table :headers="headers" :items="items" :loading="loading" density="comfortable">
    <template #item.actions="{ item }">
      <v-btn icon="mdi-pencil" size="small" variant="text" @click="openEdit(item)" />
      <v-btn icon="mdi-delete" size="small" variant="text" color="red" @click="remove(item.id)" />
    </template>
  </v-data-table>
  <v-dialog v-model="dialog" max-width="500">
    <v-card :title="editing ? 'Edit Bus' : 'Add Bus'">
      <v-card-text>
        <v-text-field v-model="form.reg_number" label="Reg Number" />
        <v-select v-model="form.bus_type" :items="busTypes" item-title="name" item-value="id" label="Type" />
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
const { items, loading, create, update, remove } = useCrud('buses')
const busTypes = ref([])
onMounted(async () => { busTypes.value = (await api.get('/api/bus-types/')).data })
const headers = [
  { title: 'Reg Number', key: 'reg_number' },
  { title: 'Type', key: 'bus_type_name' },
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
