<template>
  <v-container>
    <v-card>
      <v-card-title>Добавить нового клиента</v-card-title>

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

        <v-btn color="success" class="mr-3" @click="addResident">
          Добавить
        </v-btn>

        <v-btn color="grey" class="mr-3" @click="cancel">
          Отмена
        </v-btn>

        <div v-if="success" class="mt-2" style="color:green">{{ success }}</div>
        <div v-if="error" class="mt-2" style="color:red">{{ error }}</div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()
const resident = ref({
  name: '',
  surname: '',
  patronymic: '',
  passport_number: '',
  city: ''
})

const success = ref('')
const error = ref('')

const addResident = async () => {
  success.value = ''
  error.value = ''
  try {
    await api.post('residents/', resident.value)
    success.value = 'Клиент успешно добавлен!'
    router.push('/residents')
  } catch (e) {
    console.error(e)
    error.value = 'Ошибка при добавлении клиента'
  }
}
const cancel = () => {
  router.push('/residents')
}
</script>
