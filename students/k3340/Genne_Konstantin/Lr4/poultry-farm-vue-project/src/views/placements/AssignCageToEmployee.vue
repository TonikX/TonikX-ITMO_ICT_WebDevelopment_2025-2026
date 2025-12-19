<template>
  <v-container>
    <v-card>
      <v-card-title>Закрепить клетку за сотрудником</v-card-title>
      <v-form @submit.prevent="submit">
        <v-select
          v-model.number="form.employee"
          :items="employees"
          item-title="full_name"
          item-value="id"
          label="Сотрудник *"
          :rules="[rules.required]"
          required
        />
        <v-select
          v-model.number="form.cage"
          :items="cages"
          item-title="label"
          item-value="id"
          label="Клетка *"
          :rules="[rules.required]"
          required
        />
        <v-text-field
          v-model="form.date_start"
          label="Дата закрепления *"
          type="date"
          :rules="[rules.required]"
          required
        />
        <v-card-actions class="mt-4">
          <v-btn type="submit" color="primary">Закрепить</v-btn>
          <v-btn to="/">Отмена</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getEmployments } from '@/api/employments'
import { getCages } from '@/api/cages'
import { createEmployeeCage } from '@/api/employeeCages'

const router = useRouter()
const today = new Date().toISOString().split('T')[0]

const form = ref({
  employee: null,
  cage: null,
  date_start: today
})

const rules = {
  required: value => !!value || 'Обязательное поле'
}

const employees = ref([])
const cages = ref([])

onMounted(async () => {
  try {
    // Только работающие сотрудники
    const employments = await getEmployments({ active: 'true' })
    const uniqueEmployees = employments
      .map(emp => emp.employee_details)
      .filter((emp, index, self) => 
        index === self.findIndex(e => e.id === emp.id)
      )
    employees.value = uniqueEmployees

    // Все клетки
    const cagesRaw = await getCages()
    cages.value = cagesRaw.map(c => ({
      id: c.id,
      label: `Цех ${c.workshop_number}, ряд ${c.row_number}, клетка ${c.in_row_number}`
    }))
  } catch (err) {
    const msg = err.response?.data?.error || 'Ошибка загрузки данных'
    console.error(msg)
    alert(msg)
  }
})

const submit = async () => {
  // Проверка обязательных полей
  if (!form.value.employee || !form.value.cage || !form.value.date_start) {
    alert('Заполните все обязательные поля')
    return
  }

  try {
    await createEmployeeCage({
      employee: form.value.employee,
      cage: form.value.cage,
      date_start: form.value.date_start
      // date_end не передаётся → будет null в БД
    })
    router.push('/')
  } catch (err) {
    const msg = err.response?.data?.error || 
                err.response?.data?.employee?.[0] ||
                err.response?.data?.cage?.[0] ||
                'Ошибка закрепления'
    alert(msg)
  }
}
</script>