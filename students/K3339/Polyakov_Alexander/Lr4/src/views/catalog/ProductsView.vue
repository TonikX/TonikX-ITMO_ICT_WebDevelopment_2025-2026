<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import type { Manufacturer, Product } from '../../types/models'
import {
  createProduct,
  deleteProduct,
  fetchManufacturers,
  fetchProducts,
  updateProduct,
} from '../../api/trading'

const items = ref<Product[]>([])
const manufacturers = ref<Manufacturer[]>([])
const loading = ref(false)
const dialog = ref(false)
const formRef = ref()
const snackbar = ref(false)
const snackbarMessage = ref('')

const edited = reactive<Partial<Product>>({
  id: undefined,
  code: '',
  name: '',
  manufacturer: undefined,
  unit: 'piece',
  shelf_life_days: 0,
})

const isEdit = computed(() => !!edited.id)

const resetForm = () => {
  edited.id = undefined
  edited.code = ''
  edited.name = ''
  edited.manufacturer = undefined
  edited.unit = 'piece'
  edited.shelf_life_days = 0
}

const loadData = async () => {
  loading.value = true
  try {
    const [prod, mans] = await Promise.all([fetchProducts(), fetchManufacturers()])
    items.value = prod
    manufacturers.value = mans
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  resetForm()
  dialog.value = true
}

const openEdit = (item: Product) => {
  Object.assign(edited, item)
  dialog.value = true
}

const saveItem = async () => {
  const valid = await formRef.value?.validate()
  if (!valid) return
  loading.value = true
  try {
    if (isEdit.value && edited.id) {
      await updateProduct(edited.id, edited)
      snackbarMessage.value = 'Product updated'
    } else {
      await createProduct(edited)
      snackbarMessage.value = 'Product created'
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

const removeItem = async (item: Product) => {
  const ok = window.confirm(`Delete product "${item.name}"?`)
  if (!ok) return
  loading.value = true
  try {
    await deleteProduct(item.id)
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
          <h2 class="text-h5 mb-1">Products</h2>
          <div class="text-body-2 text-medium-emphasis">Manage products and link manufacturers</div>
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
            { title: 'Code', value: 'code' },
            { title: 'Name', value: 'name' },
            { title: 'Manufacturer', value: 'manufacturer' },
            { title: 'Unit', value: 'unit' },
            { title: 'Shelf life (days)', value: 'shelf_life_days' },
            { title: 'Actions', value: 'actions', sortable: false },
          ]"
        >
          <template #item.manufacturer="{ item }">
            {{ manufacturers.find((m) => m.id === item.manufacturer)?.name || '—' }}
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

    <v-dialog v-model="dialog" max-width="560">
      <v-card>
        <v-card-title>{{ isEdit ? 'Edit product' : 'Create product' }}</v-card-title>
        <v-card-text>
          <v-form ref="formRef" @submit.prevent="saveItem">
            <v-text-field
              v-model="edited.code"
              label="Code"
              :rules="[(v) => !!v || 'Required']"
              required
            />
            <v-text-field
              v-model="edited.name"
              label="Name"
              :rules="[(v) => !!v || 'Required']"
              required
            />
            <v-select
              v-model="edited.manufacturer"
              :items="manufacturers"
              item-title="name"
              item-value="id"
              label="Manufacturer"
              :rules="[(v) => !!v || 'Required']"
              required
            />
            <v-select
              v-model="edited.unit"
              label="Unit"
              :items="[
                { title: 'Piece', value: 'piece' },
                { title: 'Kilogram', value: 'kg' },
                { title: 'Ton', value: 'ton' },
              ]"
            />
            <v-text-field
              v-model.number="edited.shelf_life_days"
              label="Shelf life (days)"
              type="number"
              min="0"
              :rules="[(v) => v >= 0 || 'Non-negative']"
              required
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

