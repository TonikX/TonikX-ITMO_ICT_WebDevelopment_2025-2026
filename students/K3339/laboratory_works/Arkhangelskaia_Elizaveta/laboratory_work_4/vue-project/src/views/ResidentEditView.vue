<template>
  <v-container>
    <v-card>
      <v-card-title>Редактировать клиента</v-card-title>

      <v-card-text>
        <v-text-field
          v-model="resident.name"
          label="Имя"
          outlined
          dense
        ></v-text-field>

        <v-text-field
          v-model="resident.surname"
          label="Фамилия"
          outlined
          dense
        ></v-text-field>

        <v-text-field
          v-model="resident.patronymic"
          label="Отчество"
          outlined
          dense
        ></v-text-field>

        <v-text-field
          v-model="resident.passport_number"
          label="Номер паспорта"
          outlined
          dense
        ></v-text-field>

        <v-text-field
          v-model="resident.city"
          label="Город"
          outlined
          dense
        ></v-text-field>


        <v-btn
          color="primary"
          class="mt-3"
          @click="updateResident"
        >
          Сохранить
        </v-btn>

        <div v-if="success" class="mt-2" style="color:green">{{ success }}</div>
        <div v-if="error" class="mt-2" style="color:red">{{ error }}</div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'

const route = useRoute()
const router = useRouter()

const resident = ref({
  name: '',
  surname: '',
  patronymic: '',
  passport_number: '',
  city: '',
  phone: ''
})

const success = ref('')
const error = ref('')

onMounted(async () => {
  const id = route.params.id
  try {
    const res = await api.get(`residents/${id}/`)
    resident.value = res.data
  } catch {
    error.value = 'Ошибка загрузки данных'
  }
})

const updateResident = async () => {
  success.value = ''
  error.value = ''
  const id = route.params.id

  try {
    await api.patch(`residents/${id}/`, resident.value)
    success.value = 'Данные клиента успешно обновлены'
  } catch {
    error.value = 'Ошибка при обновлении'
  }
}
</script>
