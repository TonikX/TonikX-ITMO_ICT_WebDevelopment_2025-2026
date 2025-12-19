<template>
  <v-container>
    <v-card max-width="600" class="mx-auto">
      <v-card-title>Новое трудоустройство</v-card-title>
      <v-card-text>
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
          <v-text-field
            v-model="form.position"
            label="Должность *"
            :rules="[rules.required]"
            required
          />
          <v-text-field
            v-model="form.contract"
            label="Номер договора *"
            :rules="[rules.required]"
            required
          />
          <v-text-field
            v-model.number="form.salary_rub"
            label="Зарплата (руб) *"
            type="number"
            min="0"
            :rules="[rules.required, rules.min0]"
            required
          />
          <v-text-field
            v-model="form.date_start"
            label="Дата начала *"
            type="date"
            :rules="[rules.required]"
            required
          />
          
          <!-- Поля увольнения (опционально) -->
          <v-divider class="my-4" />
          <h4 class="text-h6 mb-2">При увольнении</h4>
          <v-text-field
            v-model="form.date_end"
            label="Дата увольнения"
            type="date"
            :min="form.date_start || ''"
          />
          <v-text-field
            v-model="form.termination_reason"
            label="Причина увольнения"
            :disabled="!form.date_end"
          />
          <v-text-field
            v-model="form.termination_order_num"
            label="Номер приказа об увольнении"
            :disabled="!form.date_end"
          />

          <v-card-actions class="mt-4">
            <v-btn type="submit" color="primary" :loading="loading">Создать</v-btn>
            <v-btn to="/employments">Отмена</v-btn>
          </v-card-actions>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getEmployees } from '@/api/employees'
import { createEmployment } from '@/api/employments'

const router = useRouter()
const today = new Date().toISOString().split('T')[0]

const form = ref({
  employee: null,
  position: '',
  contract: '',
  salary_rub: null,
  date_start: today,
  date_end: null,
  termination_reason: null,
  termination_order_num: null
})

const rules = {
  required: value => !!value || 'Обязательное поле',
  min0: value => value >= 0 || 'Зарплата не может быть отрицательной'
}

const employees = ref([])
const loading = ref(false)

onMounted(async () => {
  try {
    employees.value = await getEmployees()
  } catch (err) {
    alert(err.response?.data?.error || 'Ошибка загрузки сотрудников')
  }
})

const submit = async () => {
  // Проверка обязательных полей
  if (!form.value.employee || !form.value.position || !form.value.contract || !form.value.salary_rub) {
    alert('Заполните все обязательные поля')
    return
  }

  // Валидация увольнения
  if (form.value.date_end) {
    if (!form.value.termination_reason || !form.value.termination_order_num) {
      alert('При указании даты увольнения необходимо указать причину и номер приказа')
      return
    }
  }

  loading.value = true
  try {
    // Подготавливаем данные: null для пустых полей увольнения
    const payload = {
      employee: form.value.employee,
      position: form.value.position,
      contract: form.value.contract,
      salary_rub: form.value.salary_rub,
      date_start: form.value.date_start
    }

    if (form.value.date_end) {
      payload.date_end = form.value.date_end
      payload.termination_reason = form.value.termination_reason
      payload.termination_order_num = form.value.termination_order_num
    }

    await createEmployment(payload)
    router.push('/employments')
  } catch (err) {
    const errors = err.response?.data
    let msg = 'Ошибка создания трудоустройства'
    if (errors?.contract) msg = errors.contract[0]
    else if (errors?.employee) msg = errors.employee[0]
    else if (errors?.non_field_errors) msg = errors.non_field_errors[0]
    alert(msg)
  } finally {
    loading.value = false
  }
}
</script>