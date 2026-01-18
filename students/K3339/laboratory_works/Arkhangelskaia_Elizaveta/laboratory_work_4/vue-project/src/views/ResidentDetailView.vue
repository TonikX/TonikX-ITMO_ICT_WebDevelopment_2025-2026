<template>
  <v-container>
    <v-card>
      <v-card-title>
        {{ resident.surname }} {{ resident.name }} {{ resident.patronymic }}
      </v-card-title>

      <v-card-text>
        <p><strong>Номер паспорта:</strong> {{ resident.passport_number }}</p>
        <p><strong>Город:</strong> {{ resident.city }}</p>
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
const resident = ref({})

onMounted(async () => {
  const id = route.params.id
  try {
    const res = await api.get(`residents/${id}/`)
    resident.value = res.data
  } catch (e) {
    console.error('Ошибка загрузки клиента', e)
    router.push('/residents')
  }
})
</script>
