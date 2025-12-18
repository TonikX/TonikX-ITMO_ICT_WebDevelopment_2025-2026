<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import type { Broker, BrokerCompany } from '../../types/models'
import {
  createBroker,
  deleteBroker,
  fetchBrokerCompanies,
  fetchBrokers,
  updateBroker,
} from '../../api/trading'

const items = ref<Broker[]>([])
const companies = ref<BrokerCompany[]>([])
const loading = ref(false)
const dialog = ref(false)
const formRef = ref()
const snackbar = ref(false)
const snackbarMessage = ref('')

const edited = reactive<Partial<Broker>>({
  id: undefined,
  company: undefined,
  commission_rate: '0.10',
  active: true,
})

const isEdit = computed(() => !!edited.id)

const resetForm = () => {
  edited.id = undefined
  edited.company = undefined
  edited.commission_rate = '0.10'
  edited.active = true
}

const loadData = async () => {
  loading.value = true
  try {
    const [brokers, comps] = await Promise.all([fetchBrokers(), fetchBrokerCompanies()])
    items.value = brokers
    companies.value = comps
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  resetForm()
  dialog.value = true
}

const openEdit = (item: Broker) => {
  Object.assign(edited, item)
  dialog.value = true
}

const saveItem = async () => {
  const valid = await formRef.value?.validate()
  if (!valid) return
  loading.value = true
  try {
    if (isEdit.value && edited.id) {
      await updateBroker(edited.id, edited)
      snackbarMessage.value = 'Broker updated'
    } else {
      await createBroker(edited)
      snackbarMessage.value = 'Broker created'
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

const removeItem = async (item: Broker) => {
  const ok = window.confirm(`Delete broker #${item.id}?`)
  if (!ok) return
  loading.value = true
  try {
    await deleteBroker(item.id)
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

onMounted(loadData)
</script>

<template>
  <v-container class="py-6">
    <v-row>
      <v-col cols="12" class="d-flex justify-space-between align-center">
        <div>
          <h2 class="text-h5 mb-1">Brokers</h2>
          <div class="text-body-2 text-medium-emphasis">Assign brokers to companies</div>
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
            { title: 'ID', value: 'id' },
            { title: 'Company', value: 'company' },
            { title: 'Commission rate', value: 'commission_rate' },
            { title: 'Active', value: 'active' },
            { title: 'Actions', value: 'actions', sortable: false },
          ]"
        >
          <template #item.company="{ item }">
            {{ companies.find((c) => c.id === item.company)?.name || '—' }}
          </template>
          <template #item.active="{ item }">
            <v-chip :color="item.active ? 'success' : 'grey'" size="small">
              {{ item.active ? 'Active' : 'Inactive' }}
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

    <v-dialog v-model="dialog" max-width="520">
      <v-card>
        <v-card-title>{{ isEdit ? 'Edit broker' : 'Create broker' }}</v-card-title>
        <v-card-text>
          <v-form ref="formRef" @submit.prevent="saveItem">
            <v-select
              v-model="edited.company"
              :items="companies"
              item-title="name"
              item-value="id"
              label="Company"
              :rules="[(v) => !!v || 'Required']"
              required
            />
            <v-text-field
              v-model="edited.commission_rate"
              label="Commission rate (0-1)"
              type="number"
              min="0"
              max="1"
              step="0.01"
              :rules="[(v) => v === '' || (Number(v) >= 0 && Number(v) <= 1) || 'Between 0 and 1']"
            />
            <v-switch v-model="edited.active" label="Active" />
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

