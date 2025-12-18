<script setup lang="ts">
import { ref } from 'vue'
import { fetchBrokerSalaries } from '../../api/trading'
import type { BrokerSalaryRow } from '../../types/reports'

const companyId = ref('')
const companyName = ref('')
const start = ref('')
const end = ref('')
const loading = ref(false)
const items = ref<BrokerSalaryRow[]>([])
const error = ref<string | null>(null)

const loadData = async () => {
  if (!companyId.value && !companyName.value) {
    error.value = 'Enter company id or name'
    return
  }
  loading.value = true
  error.value = null
  try {
    items.value = await fetchBrokerSalaries({
      company_id: companyId.value || undefined,
      company_name: companyName.value || undefined,
      start: start.value || undefined,
      end: end.value || undefined,
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
      <v-col cols="12">
        <v-card>
          <v-card-title class="text-h6">Broker salaries</v-card-title>
          <v-card-text>
            <v-row dense>
              <v-col cols="12" md="3">
                <v-text-field v-model="companyId" label="Company ID" type="number" density="comfortable" />
              </v-col>
              <v-col cols="12" md="3">
                <v-text-field v-model="companyName" label="Company name" density="comfortable" />
              </v-col>
              <v-col cols="12" md="3">
                <v-text-field v-model="start" label="Start date" type="date" density="comfortable" />
              </v-col>
              <v-col cols="12" md="3">
                <v-text-field v-model="end" label="End date" type="date" density="comfortable" />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" class="d-flex justify-end">
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
            { title: 'Broker ID', value: 'broker_id' },
            { title: 'Company', value: 'company' },
            { title: 'Turnover', value: 'turnover' },
            { title: 'Commission', value: 'commission' },
            { title: 'Monthly fee', value: 'monthly_fee' },
            { title: 'Salary', value: 'salary' },
          ]"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

