<template>
  <v-container>
    <v-card>
      <v-card-title>{{ isEdit ? 'Редактировать сотрудника' : 'Создать сотрудника' }}</v-card-title>
      <v-card-text>
        <v-text-field 
          v-model="form.full_name" 
          label="ФИО" 
          :rules="[v => !!v || 'Обязательное поле']"
          required 
        />
        <v-text-field
          v-model="form.passport_series"
          label="Серия паспорта (4 цифры)"
          :rules="[v => !!v || 'Обязательное поле', v => /^\d{4}$/.test(v) || '4 цифры']"
          required
        />
        <v-text-field
          v-model="form.passport_number"
          label="Номер паспорта (6 цифр)"
          :rules="[v => !!v || 'Обязательное поле', v => /^\d{6}$/.test(v) || '6 цифр']"
          required
        />
      </v-card-text>
      <v-card-actions>
        <v-btn @click="save" color="primary">Сохранить</v-btn>
        <v-btn to="/employees">Отмена</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { createEmployee, updateEmployee, getEmployee } from '@/api/employees'

const route = useRoute()
const router = useRouter()
const isEdit = !!route.params.id
const form = ref({ full_name: '', passport_series: '', passport_number: '' })

onMounted(async () => {
  if (isEdit) {
    const data = await getEmployee(route.params.id)
    form.value = data
  }
})

const save = async () => {
  // Проверка на пустые поля
  if (!form.value.full_name || !form.value.passport_series || !form.value.passport_number) {
    alert('Все поля обязательны для заполнения')
    return
  }
  
  // Проверка формата паспортных данных
  if (!/^\d{4}$/.test(form.value.passport_series)) {
    alert('Серия паспорта должна содержать 4 цифры')
    return
  }
  
  if (!/^\d{6}$/.test(form.value.passport_number)) {
    alert('Номер паспорта должен содержать 6 цифр')
    return
  }

  try {
    if (isEdit) {
      await updateEmployee(route.params.id, form.value)
    } else {
      await createEmployee(form.value)
    }
    router.push('/employees')
  } catch (err) {
    console.error(err.response?.data?.error || 'Ошибка сохранения')
    alert(err.response?.data?.error || 'Ошибка сохранения')
  }
}
</script>