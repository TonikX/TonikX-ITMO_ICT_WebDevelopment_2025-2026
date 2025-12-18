<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import type { Batch, Broker } from '../../types/models'
import { createBatch, deleteBatch, fetchBatches, fetchBrokers, updateBatch } from '../../api/trading'
import { useAuthStore } from '../../store/auth'

const auth = useAuthStore()
const items = ref<Batch[]>([])
const brokers = ref<Broker[]>([])
const loading = ref(false)
const dialog = ref(false)
const formRef = ref()
const snackbar = ref(false)
const snackbarMessage = ref('')

const edited = reactive<Partial<Batch>>({
  id: undefined,
  number: '',
  broker: undefined,
  contract_date: '',
  shipment_date: '',
  prepayment: false,
  notes: '',
})

const isEdit = computed(() => !!edited.id)
const isAdmin = computed(() => auth.isAdmin)
const ownBrokerId = computed(() => auth.brokerId)

const resetForm = () => {
  edited.id = undefined
  edited.number = ''
  edited.broker = isAdmin.value ? undefined : ownBrokerId.value || undefined
  edited.contract_date = ''
  edited.shipment_date = ''
  edited.prepayment = false
  edited.notes = ''
}

const loadData = async () => {
  loading.value = true
  try {
    const batchListPromise = fetchBatches()
    const brokerPromise = isAdmin.value ? fetchBrokers() : Promise.resolve([])
    const [batchList, brokerList] = await Promise.all([batchListPromise, brokerPromise])
    items.value = batchList
    brokers.value = brokerList
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  resetForm()
  dialog.value = true
}

const openEdit = (item: Batch) => {
  Object.assign(edited, item)
  if (!isAdmin.value) {
    edited.broker = ownBrokerId.value || item.broker
  }
  dialog.value = true
}

const saveItem = async () => {
  const valid = await formRef.value?.validate()
  if (!valid) return
  loading.value = true
  try {
    if (isEdit.value && edited.id) {
      await updateBatch(edited.id, edited)
      snackbarMessage.value = 'Batch updated'
    } else {
      await createBatch(edited)
      snackbarMessage.value = 'Batch created'
    }
    dialog.value = false
    snackbar.value = true
    await loadData()
  } catch (err) {
    snackbarMessage.value = 'Save failed'
    snackbar.value = true
    console.error(err)
  } finally {
    loading.value = false
  }
}

const removeItem = async (item: Batch) => {
  const ok = window.confirm(`Delete batch "${item.number}"?`)
  if (!ok) return
  loading.value = true
  try {
    await deleteBatch(item.id)
    snackbarMessage.value = 'Deleted'
    await loadData()
  } catch (err) {
    snackbarMessage.value = 'Delete failed'
    snackbar.value = true
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadData()
})
</script>

<template>
  <v-container class="py-6">
    <v-row>
      <v-col cols="12" class="d-flex justify-space-between align-center">
        <div>
          <h2 class="text-h5 mb-1">Batches</h2>
          <div class="text-body-2 text-medium-emphasis">
            Manage trading batches and payment conditions
          </div>
        </div>
        <v-btn color="primary" prepend-icon="mdi-plus" @click="openCreate">Add</v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-data-table
          :items="items"
          :loading="loading"
          :headers="[
            { title: 'Number', value: 'number' },
            { title: 'Broker', value: 'broker' },
            { title: 'Contract date', value: 'contract_date' },
            { title: 'Shipment date', value: 'shipment_date' },
            { title: 'Prepayment', value: 'prepayment' },
            { title: 'Actions', value: 'actions', sortable: false },
          ]"
        >
          <template #item.broker="{ item }">
            Broker #{{ item.broker }}
          </template>
          <template #item.prepayment="{ item }">
            <v-chip :color="item.prepayment ? 'primary' : 'grey'" size="small">
              {{ item.prepayment ? 'Prepayment' : 'Postpaid' }}
            </v-chip>
          </template>
          <template #item.actions="{ item }">
            <v-btn icon="mdi-pencil" size="small" variant="text" @click="openEdit(item)" />
            <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="removeItem(item)" />
          </template>
        </v-data-table>
      </v-col>
    </v-row>

    <v-snackbar v-model="snackbar" timeout="3000" color="success">
      {{ snackbarMessage }}
    </v-snackbar>

    <v-dialog v-model="dialog" max-width="640">
      <v-card>
        <v-card-title>{{ isEdit ? 'Edit batch' : 'Create batch' }}</v-card-title>
        <v-card-text>
          <v-form ref="formRef" @submit.prevent="saveItem">
            <v-text-field
              v-model="edited.number"
              label="Number"
              :rules="[(v) => !!v || 'Required']"
              required
            />
            <v-select
              v-if="isAdmin"
              v-model="edited.broker"
              :items="brokers"
              item-title="id"
              item-value="id"
              label="Broker"
              :rules="[(v) => !!v || 'Required']"
              required
            />
            <v-text-field
              v-else
              v-model="edited.broker"
              label="Broker"
              disabled
            />
            <v-text-field
              v-model="edited.contract_date"
              label="Contract date"
              type="date"
              :rules="[(v) => !!v || 'Required']"
              required
            />
            <v-text-field
              v-model="edited.shipment_date"
              label="Shipment date"
              type="date"
            />
            <v-switch v-model="edited.prepayment" label="Prepayment" />
            <v-textarea v-model="edited.notes" label="Notes" rows="2" />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="dialog = false">Cancel</v-btn>
          <v-btn color="primary" :loading="loading" @click="saveItem">
            {{ isEdit ? 'Save' : 'Create' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

