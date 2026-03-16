<script setup lang="ts">
import { ref } from 'vue'
import { librarianApi } from '../shared/api/library'

const month = ref(new Date().getMonth() + 1)
const year = ref(new Date().getFullYear())
const report = ref<Awaited<ReturnType<typeof librarianApi.monthlyReport>> | null>(null)
const loadingReport = ref(false)
const reportError = ref('')
const unregisterResult = ref<string | null>(null)
const unregisterLoading = ref(false)

async function loadReport() {
  reportError.value = ''
  report.value = null
  loadingReport.value = true
  try {
    report.value = await librarianApi.monthlyReport(month.value, year.value)
  } catch (e) {
    reportError.value = e instanceof Error ? e.message : 'Ошибка загрузки отчёта'
  } finally {
    loadingReport.value = false
  }
}

async function unregisterOld() {
  unregisterResult.value = null
  unregisterLoading.value = true
  try {
    const res = await librarianApi.unregisterOldReaders()
    unregisterResult.value = res.message
  } catch (e) {
    unregisterResult.value = e instanceof Error ? e.message : 'Ошибка'
  } finally {
    unregisterLoading.value = false
  }
}
</script>

<template>
  <div>
    <h1 class="text-h4 mb-4">Операции библиотекаря</h1>

    <v-card class="mb-4">
      <v-card-title>Исключить старых читателей</v-card-title>
      <v-card-text>
        Исключить читателей, записавшихся более года назад и не прошедших перерегистрацию.
        <v-btn class="mt-2" color="primary" :loading="unregisterLoading" @click="unregisterOld">
          Выполнить
        </v-btn>
        <v-alert v-if="unregisterResult" type="info" density="compact" class="mt-2">
          {{ unregisterResult }}
        </v-alert>
      </v-card-text>
    </v-card>

    <v-card>
      <v-card-title>Месячный отчёт</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="auto">
            <v-text-field v-model.number="month" type="number" label="Месяц" min="1" max="12" density="compact" />
          </v-col>
          <v-col cols="auto">
            <v-text-field v-model.number="year" type="number" label="Год" density="compact" />
          </v-col>
          <v-col cols="auto" align-self="center">
            <v-btn color="primary" :loading="loadingReport" @click="loadReport">
              Загрузить отчёт
            </v-btn>
          </v-col>
        </v-row>
        <v-alert v-if="reportError" type="error" density="compact">{{ reportError }}</v-alert>
        <v-progress-linear v-if="loadingReport" indeterminate />
        <template v-else-if="report">
          <p class="mt-2">
            <strong>Всего записавшихся за месяц:</strong> {{ report.total_new_readers }}
          </p>
          <v-table density="compact" class="mt-2">
            <thead>
              <tr>
                <th>Дата</th>
                <th>Книг</th>
                <th>Читателей</th>
                <th>Новых за день</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="d in report.daily_stats" :key="d.date">
                <td>{{ d.date }}</td>
                <td>{{ d.books_count }}</td>
                <td>{{ d.readers_count }}</td>
                <td>{{ d.new_readers_count }}</td>
              </tr>
            </tbody>
          </v-table>
        </template>
      </v-card-text>
    </v-card>
  </div>
</template>
