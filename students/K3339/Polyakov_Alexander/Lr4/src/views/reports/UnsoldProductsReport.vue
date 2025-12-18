<script setup lang="ts">
import { ref } from 'vue'
import { fetchUnsoldProducts } from '../../api/trading'

const companyId = ref('')
const companyName = ref('')
const loading = ref(false)
const items = ref<Array<{ id: number; code: string; name: string }>>([])
const error = ref<string | null>(null)

const loadData = async () => {
  if (!companyId.value && !companyName.value) {
    error.value = 'Enter company id or name'
    return
  }
  loading.value = true
  error.value = null
  try {
    items.value = await fetchUnsoldProducts({
      company_id: companyId.value || undefined,
      company_name: companyName.value || undefined,
    })
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
          <v-card-title class="text-h6">Products never sold by broker company</v-card-title>
          <v-card-text>
            <v-row dense>
              <v-col cols="12" md="4">
                <v-text-field v-model="companyId" label="Company ID" type="number" density="comfortable" />
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field v-model="companyName" label="Company name" density="comfortable" />
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
            { title: 'Code', value: 'code' },
            { title: 'Name', value: 'name' },
          ]"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

