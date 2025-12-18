<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { fetchExpiredItems } from '../../api/trading'

const items = ref<
  Array<{
    batch_number: string
    product_code: string
    product_name: string
    broker_id: number
    broker_company: string
  }>
>([])
const loading = ref(false)
const error = ref<string | null>(null)

const loadData = async () => {
  loading.value = true
  error.value = null
  try {
    items.value = await fetchExpiredItems()
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
          <h2 class="text-h5 mb-1">Expired items</h2>
          <div class="text-body-2 text-medium-emphasis">Batches with expired goods</div>
        </div>
        <v-btn color="primary" :loading="loading" @click="loadData">Refresh</v-btn>
      </v-col>
    </v-row>

    <v-row class="mt-2">
      <v-col cols="12">
        <v-alert v-if="error" type="error" variant="tonal" class="mb-2">{{ error }}</v-alert>
        <v-data-table
          :items="items"
          :loading="loading"
          :headers="[
            { title: 'Batch', value: 'batch_number' },
            { title: 'Product code', value: 'product_code' },
            { title: 'Product name', value: 'product_name' },
            { title: 'Broker ID', value: 'broker_id' },
            { title: 'Broker company', value: 'broker_company' },
          ]"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

