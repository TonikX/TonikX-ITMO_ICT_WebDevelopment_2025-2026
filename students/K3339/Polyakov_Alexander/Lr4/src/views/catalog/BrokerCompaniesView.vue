<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import type { BrokerCompany } from '../../types/models'
import {
  createBrokerCompany,
  deleteBrokerCompany,
  fetchBrokerCompanies,
  updateBrokerCompany,
} from '../../api/trading'

const items = ref<BrokerCompany[]>([])
const loading = ref(false)
const dialog = ref(false)
const formRef = ref()
const snackbar = ref(false)
const snackbarMessage = ref('')

const edited = reactive<Partial<BrokerCompany>>({
  id: undefined,
  name: '',
  monthly_fee: '',
  contact_info: '',
})

const isEdit = computed(() => !!edited.id)

const resetForm = () => {
  edited.id = undefined
  edited.name = ''
  edited.monthly_fee = ''
  edited.contact_info = ''
}

const loadData = async () => {
  loading.value = true
  try {
    items.value = await fetchBrokerCompanies()
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  resetForm()
  dialog.value = true
}

const openEdit = (item: BrokerCompany) => {
  Object.assign(edited, item)
  dialog.value = true
}

const saveItem = async () => {
  const valid = await formRef.value?.validate()
  if (!valid) return
  loading.value = true
  try {
    if (isEdit.value && edited.id) {
      await updateBrokerCompany(edited.id, edited)
      snackbarMessage.value = 'Company updated'
    } else {
      await createBrokerCompany(edited)
      snackbarMessage.value = 'Company created'
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

const removeItem = async (item: BrokerCompany) => {
  const ok = window.confirm(`Delete company "${item.name}"?`)
  if (!ok) return
  loading.value = true
  try {
    await deleteBrokerCompany(item.id)
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
          <h2 class="text-h5 mb-1">Broker Companies</h2>
          <div class="text-body-2 text-medium-emphasis">Maintain broker agencies and fees</div>
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
            { title: 'Name', value: 'name' },
            { title: 'Monthly fee', value: 'monthly_fee' },
            { title: 'Contact', value: 'contact_info' },
            { title: 'Actions', value: 'actions', sortable: false },
          ]"
        >
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
        <v-card-title>{{ isEdit ? 'Edit company' : 'Create company' }}</v-card-title>
        <v-card-text>
          <v-form ref="formRef" @submit.prevent="saveItem">
            <v-text-field
              v-model="edited.name"
              label="Name"
              :rules="[(v) => !!v || 'Required']"
              required
            />
            <v-text-field
              v-model="edited.monthly_fee"
              label="Monthly fee"
              type="number"
              min="0"
              :rules="[(v) => v === '' || Number(v) >= 0 || 'Non-negative']"
            />
            <v-textarea v-model="edited.contact_info" label="Contact info" rows="3" />
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

