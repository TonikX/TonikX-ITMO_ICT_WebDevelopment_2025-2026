<template>
  <v-container>
    <v-card>
      <v-card-title>Добавить нового сотрудника</v-card-title>

      <v-card-text>
        <!-- Имя -->
        <v-text-field
          v-model="worker.name"
          label="Имя"
          outlined
          dense
        ></v-text-field>

        <!-- Фамилия -->
        <v-text-field
          v-model="worker.surname"
          label="Фамилия"
          outlined
          dense
        ></v-text-field>

        <!-- Отчество -->
        <v-text-field
          v-model="worker.patronymic"
          label="Отчество"
          outlined
          dense
        ></v-text-field>

        <!-- Статус занятости -->
        <v-switch
          v-model="worker.is_employed"
          label="Работает"
          inset
        ></v-switch>

        <!-- Кнопки -->
        <v-btn color="green lighten-2" class="mt-3 mr-2" @click="createWorker">
          Добавить
        </v-btn>

        <v-btn color="grey lighten-1" class="mt-3" @click="goBack">
          Отмена
        </v-btn>

        <!-- Сообщения -->
        <v-alert v-if="success" type="success" dense class="mt-3" color="green lighten-2">
          {{ success }}
        </v-alert>

        <v-alert v-if="error" type="error" dense class="mt-3">
          {{ error }}
        </v-alert>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()

const worker = ref({
  name: '',
  surname: '',
  patronymic: '',
  is_employed: true
})

const success = ref('')
const error = ref('')

const createWorker = async () => {
  success.value = ''
  error.value = ''

  try {
    await api.post('workers/', worker.value)
    success.value = 'Сотрудник успешно добавлен!'
    setTimeout(() => {
      router.push('/workers')
    }, 1500)
  } catch (e) {
    console.error(e)
    error.value = 'Ошибка при добавлении сотрудника'
  }
}

const goBack = () => {
  router.push('/workers')
}
</script>
