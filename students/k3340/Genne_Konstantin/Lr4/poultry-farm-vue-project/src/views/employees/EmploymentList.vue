<template>
  <v-container>
    <v-card>
      <v-card-title>Трудоустройство сотрудников</v-card-title>
      <v-card-actions>
        <v-btn to="/employments/new" color="primary">Новое трудоустройство</v-btn>
      </v-card-actions>

      <v-expansion-panels flat>
        <v-expansion-panel 
          v-for="(group, employeeId) in groupedEmployments" 
          :key="employeeId"
        >
          <v-expansion-panel-title>
            <div class="d-flex align-center">
              <v-avatar size="36" class="mr-3" color="primary" variant="tonal">
                <span class="text-h6">{{ employeeId }}</span>
              </v-avatar>
              <div>
                <div class="font-weight-medium">{{ group.employee.full_name }}</div>
                <div class="text-caption text-medium-emphasis">
                  {{ group.employments.filter(e => !e.date_end).length }} активных договоров
                </div>
              </div>
            </div>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <v-table density="compact">
              <thead>
                <tr>
                  <th>Должность</th>
                  <th>Номер договора</th>
                  <th>Зарплата</th>
                  <th>Дата начала</th>
                  <th>Дата окончания</th>
                  <th>Статус</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="emp in group.employments" :key="emp.id">
                  <td>{{ emp.position }}</td>
                  <td>{{ emp.contract }}</td>
                  <td>{{ emp.salary_rub }} ₽</td>
                  <td>{{ formatDate(emp.date_start) }}</td>
                  <td>{{ emp.date_end ? formatDate(emp.date_end) : '—' }}</td>
                  <td>
                    <v-chip 
                      :color="emp.date_end ? 'error' : 'success'" 
                      size="small"
                      variant="tonal"
                    >
                      {{ emp.date_end ? 'Уволен' : 'Работает' }}
                    </v-chip>
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getEmployments } from '@/api/employments'

const employments = ref([])

onMounted(async () => {
  try {
    employments.value = await getEmployments()
  } catch (err) {
    alert(err.response?.data?.error || 'Ошибка загрузки трудоустройства')
  }
})

// Группировка по сотрудникам
const groupedEmployments = computed(() => {
  const groups = {}
  employments.value.forEach(emp => {
    const id = emp.employee
    if (!groups[id]) {
      groups[id] = {
        employee: emp.employee_details,
        employments: []
      }
    }
    groups[id].employments.push(emp)
  })
  return groups
})

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('ru-RU')
}
</script>