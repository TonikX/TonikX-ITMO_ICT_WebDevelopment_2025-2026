<template>
  <v-container>
    <v-card>
      <v-card-title>Текущие закрепления клеток за сотрудниками</v-card-title>
      <v-card-text>
        <v-select
          v-model="filters.employee_id"
          :items="activeEmployeeOptions"
          item-title="full_name"
          item-value="id"
          label="Фильтр по сотруднику"
          clearable
          hide-details
          style="max-width: 400px"
        />
      </v-card-text>

      <v-table class="mt-2">
        <thead>
          <tr>
            <th>Сотрудник</th>
            <th>Паспорт</th>
            <th>Клетка</th>
            <th>Дата закрепления</th>
            <th>Действия</th> <!-- Новая колонка -->
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ item.employee_details.full_name }}</td>
            <td>{{ item.employee_details.passport_series }} {{ item.employee_details.passport_number }}</td>
            <td>
              Цех {{ item.cage_details.workshop_number }},
              ряд {{ item.cage_details.row_number }},
              клетка {{ item.cage_details.in_row_number }}
            </td>
            <td>{{ formatDate(item.date_start) }}</td>
            <td>
              <!-- Кнопка "Открепить" -->
              <v-btn
                size="small"
                color="warning"
                variant="tonal"
                @click="detachEmployee(item.id)"
              >
                Открепить
              </v-btn>
            </td>
          </tr>
          <tr v-if="items.length === 0">
            <td colspan="5" class="text-center">Нет текущих закреплений</td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { getEmployeeCages, updateEmployeeCage } from '@/api/employeeCages'
import { getEmployments } from '@/api/employments'

const items = ref([])
const filters = ref({ employee_id: null })
const activeEmployeeOptions = ref([])

// Загружаем текущие закрепления
const loadAssignments = async () => {
  try {
    const params = { active: 'true' }
    if (filters.value.employee_id) {
      params.employee_id = filters.value.employee_id
    }
    items.value = await getEmployeeCages(params)
  } catch (err) {
    const msg = err.response?.data?.error || 'Ошибка загрузки закреплений'
    console.error(msg)
    alert(msg)
  }
}

// Загружаем только активных сотрудников
const loadActiveEmployees = async () => {
  try {
    const activeEmployments = await getEmployments({ active: 'true' })
    const employees = activeEmployments.map(emp => emp.employee_details)
    const uniqueEmployees = employees.filter((emp, index, self) =>
      index === self.findIndex(e => e.id === emp.id)
    )
    activeEmployeeOptions.value = uniqueEmployees
  } catch (err) {
    const msg = err.response?.data?.error || 'Ошибка загрузки списка сотрудников'
    console.error(msg)
    alert(msg)
  }
}

// Открепление сотрудника
const detachEmployee = async (id) => {
  if (!confirm('Вы уверены, что хотите открепить сотрудника от клетки?')) return

  try {
    const today = new Date().toISOString().split('T')[0]
    await updateEmployeeCage(id, { date_end: today })
    // Обновляем список
    await loadAssignments()
  } catch (err) {
    const msg = err.response?.data?.error || 'Ошибка открепления'
    console.error(msg)
    alert(msg)
  }
}

onMounted(async () => {
  await Promise.all([
    loadActiveEmployees(),
    loadAssignments()
  ])
})

watch(() => filters.value.employee_id, loadAssignments)

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('ru-RU')
}
</script>