<template>
  <v-container>
    <v-card>
      <v-card-title>Сотрудники</v-card-title>
      <v-card-actions>
        <v-btn to="/employees/new" color="primary">Добавить сотрудника</v-btn>
      </v-card-actions>
      <v-table>
        <thead>
          <tr>
            <th>ФИО</th>
            <th>Паспорт</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="employee in items" :key="employee.id">
            <td>{{ employee.full_name }}</td>
            <td>{{ employee.passport_series }} {{ employee.passport_number }}</td>
            <td>
              <v-btn
                size="small"
                variant="text"
                color="primary"
                :to="`/employees/${employee.id}/edit`"
              >
                Редактировать
              </v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getEmployees } from '@/api/employees'

const items = ref([])

onMounted(async () => {
  try {
    items.value = await getEmployees()
  } catch (err) {
    const msg = err.response?.data?.error || 'Ошибка загрузки списка сотрудников'
    console.error(msg)
    alert(msg)
  }
})
</script>