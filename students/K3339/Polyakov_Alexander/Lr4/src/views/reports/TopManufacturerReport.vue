<script setup lang="ts">
import { ref } from 'vue'
import { fetchTopManufacturer } from '../../api/trading'
import type { TopManufacturerRow } from '../../types/reports'

const start = ref<string | null>(null)
const end = ref<string | null>(null)
const loading = ref(false)
const result = ref<TopManufacturerRow | null>(null)
const error = ref<string | null>(null)

const loadData = async () => {
  loading.value = true
  error.value = null
  try {
    const data = await fetchTopManufacturer({ start: start.value || undefined, end: end.value || undefined })
    result.value = (data as TopManufacturerRow) || null
  } catch (e) {
    error.value = 'Failed to load'
    console.error(e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-container class="py-6">
    <v-row>
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title class="text-h6">Top manufacturer by revenue</v-card-title>
          <v-card-text>
            <v-row dense>
              <v-col cols="12" md="4">
                <v-text-field v-model="start" label="Start date" type="date" density="comfortable" />
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field v-model="end" label="End date" type="date" density="comfortable" />
              </v-col>
              <v-col cols="12" md="4" class="d-flex align-end">
                <v-btn color="primary" :loading="loading" @click="loadData">Refresh</v-btn>
              </v-col>
            </v-row>
            <v-alert v-if="error" type="error" variant="tonal" class="mt-2">{{ error }}</v-alert>

            <div v-if="result" class="mt-4">
              <div class="text-h6">{{ result.product__manufacturer__name }}</div>
              <div class="text-body-2 text-medium-emphasis">Revenue: {{ result.revenue }}</div>
            </div>
            <div v-else class="mt-4 text-medium-emphasis">No data yet. Run the report.</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

