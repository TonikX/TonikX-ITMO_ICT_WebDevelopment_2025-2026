<template>
  <v-container>
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        <span>Список клиентов</span>
        <v-btn color="success" @click="createResident">Добавить нового клиента</v-btn>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="residents"
        item-key="id"
      >
      <template #item.fullName="{ item }">
        {{ item.surname }} {{ item.name }} {{ item.patronymic }}
      </template>

      <template #item.actions="{ item }">
        <v-btn
          color="primary"
          size="small"
          class="mr-2"
          @click="goToResident(item.id)"
        >
          Подробнее
        </v-btn>

        <v-btn
          color="secondary"
          size="small"
          class="mr-2"
          @click="editResident(item.id)"
        >
          Редактировать
        </v-btn>

        <v-btn
          color="error"
          size="small"
          @click="deleteResident(item.id)"
        >
          Удалить
        </v-btn>
      </template>

      </v-data-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()
const residents = ref([])

const headers = [
  { title: 'ФИО', key: 'fullName' },
  { title: '', key: 'actions', sortable: false }
]

const loadResidents = async () => {
  try {
    const res = await api.get('residents/')
    residents.value = res.data
  } catch (e) {
    console.error('Ошибка загрузки клиентов', e)
  }
}

onMounted(() => {
  loadResidents()
})

const goToResident = (id) => {
  router.push(`/residents/${id}`)
}

const editResident = (id) => {
  router.push(`/residents/${id}/edit`)
}

const createResident = () => {
  router.push('/residents/new')
}

const deleteResident = async (id) => {
  const confirmDelete = confirm('Вы точно хотите удалить этого клиента?')
  if (!confirmDelete) return

  try {
    await api.delete(`residents/${id}/`)
    alert('Клиент успешно удалён')
    loadResidents() // обновляем список
  } catch (e) {
    console.error(e)
    alert('Ошибка при удалении клиента')
  }
}
</script>
