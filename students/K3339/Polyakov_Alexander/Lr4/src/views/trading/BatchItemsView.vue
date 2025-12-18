<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import type { Batch, BatchItem, Product } from '../../types/models'
import {
  createBatchItem,
  deleteBatchItem,
  fetchBatchItems,
  fetchBatches,
  fetchProducts,
  updateBatchItem,
} from '../../api/trading'

const items = ref<BatchItem[]>([])
const batches = ref<Batch[]>([])
const products = ref<Product[]>([])
const loading = ref(false)
const dialog = ref(false)
const formRef = ref()
const snackbar = ref(false)
const snackbarMessage = ref('')

const edited = reactive<Partial<BatchItem>>({
  id: undefined,
  batch: undefined,
  product: undefined,
  production_date: '',
  quantity: '',
  unit_price: '',
})

const isEdit = computed(() => !!edited.id)

const resetForm = () => {
  edited.id = undefined
  edited.batch = undefined
  edited.product = undefined
  edited.production_date = ''
  edited.quantity = ''
  edited.unit_price = ''
}

const loadData = async () => {
  loading.value = true
  try {
    const [list, batchList, productList] = await Promise.all([
      fetchBatchItems(),
      fetchBatches(),
      fetchProducts(),
    ])
    items.value = list
    batches.value = batchList
    products.value = productList
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  resetForm()
  dialog.value = true
}

const openEdit = (item: BatchItem) => {
  Object.assign(edited, item)
  dialog.value = true
}

const saveItem = async () => {
  const valid = await formRef.value?.validate()
  if (!valid) return
  loading.value = true
  try {
    if (isEdit.value && edited.id) {
      await updateBatchItem(edited.id, edited)
      snackbarMessage.value = 'Batch item updated'
    } else {
      await createBatchItem(edited)
      snackbarMessage.value = 'Batch item created'
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

const removeItem = async (item: BatchItem) => {
  const ok = window.confirm(`Delete item #${item.id}?`)
  if (!ok) return
  loading.value = true
  try {
    await deleteBatchItem(item.id)
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
          <h2 class="text-h5 mb-1">Batch Items</h2>
          <div class="text-body-2 text-medium-emphasis">
            Manage items inside batches with expiry calculation
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
            { title: 'Batch', value: 'batch' },
            { title: 'Product', value: 'product' },
            { title: 'Production date', value: 'production_date' },
            { title: 'Quantity', value: 'quantity' },
            { title: 'Unit price', value: 'unit_price' },
            { title: 'Total', value: 'total_price' },
            { title: 'Expired', value: 'is_expired' },
            { title: 'Actions', value: 'actions', sortable: false },
          ]"
        >
          <template #item.batch="{ item }">
            {{ batches.find((b) => b.id === item.batch)?.number || item.batch }}
          </template>
          <template #item.product="{ item }">
            {{ products.find((p) => p.id === item.product)?.name || item.product }}
          </template>
          <template #item.is_expired="{ item }">
            <v-chip :color="item.is_expired ? 'error' : 'success'" size="small">
              {{ item.is_expired ? 'Expired' : 'OK' }}
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
        <v-card-title>{{ isEdit ? 'Edit batch item' : 'Create batch item' }}</v-card-title>
        <v-card-text>
          <v-form ref="formRef" @submit.prevent="saveItem">
            <v-select
              v-model="edited.batch"
              :items="batches"
              item-title="number"
              item-value="id"
              label="Batch"
              :rules="[(v) => !!v || 'Required']"
              required
            />
            <v-select
              v-model="edited.product"
              :items="products"
              item-title="name"
              item-value="id"
              label="Product"
              :rules="[(v) => !!v || 'Required']"
              required
            />
            <v-text-field
              v-model="edited.production_date"
              label="Production date"
              type="date"
              :rules="[(v) => !!v || 'Required']"
              required
            />
            <v-text-field
              v-model="edited.quantity"
              label="Quantity"
              type="number"
              min="0"
              :rules="[(v) => v === '' || Number(v) >= 0 || 'Non-negative']"
            />
            <v-text-field
              v-model="edited.unit_price"
              label="Unit price"
              type="number"
              min="0"
              :rules="[(v) => v === '' || Number(v) >= 0 || 'Non-negative']"
            />
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

