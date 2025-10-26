<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">Сотрудники</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="6">
        <v-card color="primary" dark>
          <v-card-title>
            <v-icon left>mdi-account-group</v-icon>
            Общее количество сотрудников
          </v-card-title>
          <v-card-text>
            <div v-if="loading" class="text-center py-4">
              <v-progress-circular indeterminate color="white"></v-progress-circular>
            </div>
            <div v-else class="text-h2">{{ employeesCount }}</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>
            <v-icon left>mdi-information</v-icon>
            Информация
          </v-card-title>
          <v-card-text>
            <p>Здесь отображается общее количество сотрудников авиакомпании.</p>
            <p>Данные обновляются автоматически при загрузке страницы.</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { dataAPI } from '@/services/api'

const employeesCount = ref(0)
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await dataAPI.getEmployeesCount()
    employeesCount.value = response.data.employees_count
  } catch (error) {
    console.error('Error loading employees count:', error)
  } finally {
    loading.value = false
  }
})
</script>