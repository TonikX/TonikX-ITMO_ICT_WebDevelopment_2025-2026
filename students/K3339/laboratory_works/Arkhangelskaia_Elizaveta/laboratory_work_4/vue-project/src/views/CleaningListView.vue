<template>
  <v-container>
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        <span>Уборки</span>

        <v-btn color="success" @click="goToNewCleaning">
          Добавить новую
        </v-btn>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="cleanings"
        item-key="id"
      >
        <template #item.cleaning_date="{ item }">
          {{ formatDate(item.cleaning_date) }}
        </template>

        <template #item.worker="{ item }">
          {{ item.worker_fio }}
        </template>

        <template #item.room="{ item }">
          {{ item.room_number }}
        </template>

        <template #item.actions="{ item }">
          <v-btn
            color="primary"
            size="small"
            class="mr-2"
            @click="editCleaning(item.id)"
          >
            Редактировать
          </v-btn>

          <v-btn
            color="error"
            size="small"
            @click="deleteCleaning(item.id)"
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
const cleanings = ref([])

const headers = [
  { title: 'Дата уборки', key: 'cleaning_date' },
  { title: 'Сотрудник', key: 'worker' },
  { title: 'Номер комнаты', key: 'room' },
  { title: '', key: 'actions', sortable: false }
]

const formatDate = (dateStr) => {
  return new Date(dateStr).toISOString().slice(0, 10)
}

const loadCleanings = async () => {
  try {
    const res = await api.get('cleaning/')
    const rawCleanings = res.data

    const enriched = await Promise.all(
      rawCleanings.map(async (c) => {
        const [workerRes, roomRes] = await Promise.all([
          api.get(`workers/${c.worker}/`),
          api.get(`rooms/${c.room}/`)
        ])

        return {
          ...c,
          worker_fio: `${workerRes.data.surname} ${workerRes.data.name} ${workerRes.data.patronymic}`,
          room_number: roomRes.data.room_number
        }
      })
    )

    cleanings.value = enriched
  } catch (e) {
    console.error('Ошибка загрузки уборок', e)
  }
}

const editCleaning = (id) => {
  router.push(`/cleaning/${id}/edit`)
}

const deleteCleaning = async (id) => {
  const confirmDelete = confirm('Удалить эту запись об уборке?')
  if (!confirmDelete) return

  try {
    await api.delete(`cleaning/${id}/`)
    loadCleanings()
  } catch (e) {
    console.error(e)
    alert('Ошибка при удалении')
  }
}

onMounted(() => {
  loadCleanings()
})


const goToNewCleaning = () => {
  router.push('/cleaning/new')
}
</script>
