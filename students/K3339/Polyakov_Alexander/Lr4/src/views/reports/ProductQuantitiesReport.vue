<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { fetchProductQuantities } from '../../api/trading'
import type { ProductQuantityRow } from '../../types/reports'

const items = ref<ProductQuantityRow[]>([])
const loading = ref(false)
const selectedDate = ref<string | null>(null)
const error = ref<string | null>(null)

const loadData = async () => {
  loading.value = true
  error.value = null
  try {
    items.value = await fetchProductQuantities(selectedDate.value || undefined)
  } catch (e) {
    error.value = 'Failed to load report'
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

<template>
  <v-container class="py-6">
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="text-h6">Product quantities</v-card-title>
          <v-card-text>
            <v-row dense>
              <v-col cols="12" md="8">
                <v-text-field
                  v-model="selectedDate"
                  label="Up to date"
                  type="date"
                  density="comfortable"
                />
              </v-col>
              <v-col cols="12" md="4" class="d-flex align-end">
                <v-btn color="primary" :loading="loading" @click="loadData">Refresh</v-btn>
              </v-col>
            </v-row>
            <v-alert v-if="error" type="error" variant="tonal" class="mt-2">{{ error }}</v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12">
        <v-data-table
          :items="items"
          :loading="loading"
          :headers="[
            { title: 'Product code', value: 'product__code' },
            { title: 'Product name', value: 'product__name' },
            { title: 'Total quantity', value: 'total_quantity' },
          ]"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

