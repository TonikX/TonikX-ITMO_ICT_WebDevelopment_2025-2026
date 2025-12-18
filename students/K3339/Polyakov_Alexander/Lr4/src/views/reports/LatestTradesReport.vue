<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { fetchLatestTrades } from '../../api/trading'
import type { LatestTradeRow } from '../../types/reports'

const loading = ref(false)
const error = ref<string | null>(null)
const totalProducts = ref(0)
const totalQuantity = ref<string | number>('0')
const items = ref<LatestTradeRow[]>([])

const loadData = async () => {
  loading.value = true
  error.value = null
  try {
    const data = await fetchLatestTrades()
    totalProducts.value = data.total_products
    totalQuantity.value = data.total_quantity
    items.value = data.items
  } catch (e) {
    error.value = 'Failed to load'
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
      <v-col cols="12" class="d-flex justify-space-between align-center">
        <div>
          <h2 class="text-h5 mb-1">Latest trades</h2>
          <div class="text-body-2 text-medium-emphasis">Summary of last trades per product</div>
        </div>
        <v-btn color="primary" :loading="loading" @click="loadData">Refresh</v-btn>
      </v-col>
    </v-row>

    <v-row class="mt-2">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-text>
            <div class="text-caption text-medium-emphasis">Total products</div>
            <div class="text-h5">{{ totalProducts }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-text>
            <div class="text-caption text-medium-emphasis">Total quantity</div>
            <div class="text-h5">{{ totalQuantity }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12">
        <v-alert v-if="error" type="error" variant="tonal" class="mb-2">{{ error }}</v-alert>
        <v-data-table
          :items="items"
          :loading="loading"
          :headers="[
            { title: 'Product', value: 'product_name' },
            { title: 'Code', value: 'product_code' },
            { title: 'Manufacturer', value: 'manufacturer' },
            { title: 'Last batch', value: 'last_batch_number' },
            { title: 'Last date', value: 'last_batch_date' },
            { title: 'Last quantity', value: 'last_batch_quantity' },
            { title: 'Offered by', value: 'offered_by_company' },
            { title: 'Total quantity', value: 'total_quantity' },
          ]"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

