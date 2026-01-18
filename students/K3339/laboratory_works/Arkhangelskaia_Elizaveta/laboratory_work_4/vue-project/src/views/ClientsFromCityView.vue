<template>
  <v-container>
    <v-card>
      <v-card-title>
        Клиенты из города {{ city || '...' }}
      </v-card-title>

      <v-card-text>
        <v-text-field
          v-model="city"
          label="Город"
          outlined
          dense
        />

        <v-btn color="#1B5E20" class="mt-2" @click="search">
          Поиск
        </v-btn>

        <div v-if="error" class="mt-2" style="color:red">
          {{ error }}
        </div>

        <v-data-table
          v-if="clients.length"
          :headers="headers"
          :items="clients"
          class="mt-4"
        ></v-data-table>
      </v-card-text>
    </v-card>
  </v-container>
</template>
<script setup>
import { ref } from 'vue'
import api from '@/api'


const city = ref('')
const clients = ref([])
const error = ref('')

const headers = [
  { title: 'Фамилия', key: 'surname' },
  { title: 'Имя', key: 'name' },
  { title: 'Отчество', key: 'patronymic' },
  { title: 'Паспорт', key: 'passport_number' }
]

const search = async () => {
  error.value = ''
  clients.value = []

  if (!city.value) {
    error.value = 'Введите город'
    return
  }

  try {
    const res = await api.get(`req/from_city/?city=${city.value}`)
    clients.value = res.data
  } catch (e) {
    console.error(e)
    error.value = 'Ошибка получения данных'
  }
}
</script>
