<template>
  <div class="page">
    <h1>Отчёты библиотеки</h1>
    <p class="subtitle">
      Статистика по читателям и залам. Доступно только для администратора.
    </p>

    <!-- статистика по образованию -->
    <section class="card">
      <h2>Распределение читателей по образованию</h2>

      <button class="secondary-btn" @click="loadEducation" :disabled="loadingEdu">
        <span v-if="loadingEdu">Обновляем…</span>
        <span v-else>Обновить</span>
      </button>

      <p v-if="errorEdu" class="status status-error">
        {{ errorEdu }}
      </p>

      <table v-if="eduStats" class="table">
        <thead>
          <tr>
            <th>Уровень образования</th>
            <th>Количество</th>
            <th>% от общего числа</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, level) in eduStats.by_education" :key="level">
            <td>{{ level }}</td>
            <td>{{ item.count }}</td>
            <td>{{ item.percent }} %</td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- новые читатели по залам за месяц -->
    <section class="card">
      <h2>Новые читатели по залам за месяц</h2>

      <form class="filter-row" @submit.prevent="loadMonthly">
        <label>
          Год
          <input
            v-model.number="year"
            type="number"
            class="input"
            min="2000"
            max="2100"
          />
        </label>
        <label>
          Месяц
          <input
            v-model.number="month"
            type="number"
            class="input"
            min="1"
            max="12"
          />
        </label>
        <button class="secondary-btn" type="submit" :disabled="loadingMonthly">
          <span v-if="loadingMonthly">Обновляем…</span>
          <span v-else>Показать</span>
        </button>
      </form>

      <p v-if="errorMonthly" class="status status-error">
        {{ errorMonthly }}
      </p>

      <table v-if="monthly && monthly.new_readers" class="table">
        <thead>
          <tr>
            <th>Зал</th>
            <th>Новых читателей</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="h in monthly.new_readers.by_hall" :key="h.hall_id">
            <td>{{ h.hall_name }}</td>
            <td>{{ h.count }}</td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import apiClient from '@/api/client'

const eduStats = ref(null)
const loadingEdu = ref(false)
const errorEdu = ref(null)

const monthly = ref(null)
const loadingMonthly = ref(false)
const errorMonthly = ref(null)

const now = new Date()
const year = ref(now.getFullYear())
const month = ref(now.getMonth() + 1)

const loadEducation = async () => {
  loadingEdu.value = true
  errorEdu.value = null
  try {
    const resp = await apiClient.get('readers/education-stats/')
    eduStats.value = resp.data
  } catch (e) {
    console.error(e)
    errorEdu.value = 'Не удалось загрузить статистику.'
  } finally {
    loadingEdu.value = false
  }
}

const loadMonthly = async () => {
  loadingMonthly.value = true
  errorMonthly.value = null
  try {
    const resp = await apiClient.get('reports/monthly/', {
      params: { year: year.value, month: month.value },
    })
    monthly.value = resp.data
  } catch (e) {
    console.error(e)
    errorMonthly.value = 'Не удалось загрузить отчёт.'
  } finally {
    loadingMonthly.value = false
  }
}

loadEducation()
loadMonthly()
</script>

<style scoped>
.page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 16px 48px;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

h1 {
  font-size: 26px;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 24px;
}

.card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
  border: 1px solid #e2e8f0;
  padding: 20px 18px;
  margin-bottom: 18px;
}

.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
  margin-top: 12px;
}

.table th,
.table td {
  padding: 8px 10px;
  border-bottom: 1px solid #e2e8f0;
  text-align: left;
}

.status {
  margin-top: 8px;
  padding: 8px 10px;
  border-radius: 12px;
  font-size: 13px;
}

.status-error {
  background: #fef2f2;
  color: #b91c1c;
}

.filter-row {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-top: 8px;
  flex-wrap: wrap;
}

.filter-row label {
  font-size: 13px;
  color: #475569;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.input {
  padding: 6px 10px;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
}

.secondary-btn {
  border-radius: 999px;
  border: 1px solid #6366f1;
  background: #fff;
  color: #4f46e5;
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
}
</style>
