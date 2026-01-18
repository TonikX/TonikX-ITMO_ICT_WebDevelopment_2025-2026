<template>
  <v-container>
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        <span>Список сотрудников</span>
        <v-btn color="green lighten-2" @click="createWorker">
          Добавить нового
        </v-btn>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="workers"
        item-key="id"
        class="elevation-1"
      >
        <template #item.is_employed="{ item }">
          <span v-if="item.is_employed">Да</span>
          <span v-else>Нет</span>
        </template>

        <template #item.actions="{ item }">
          <v-btn color="primary" small class="mr-2" @click="editWorker(item.id)">
            Редактировать
          </v-btn>
          <v-btn color="error" small @click="deleteWorker(item.id)">
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
const workers = ref([])

const headers = [
  { title: 'Имя', key: 'name' },
  { title: 'Фамилия', key: 'surname' },
  { title: 'Отчество', key: 'patronymic' },
  { title: 'Работает', key: 'is_employed' },
  { title: '', key: 'actions', sortable: false }
]

const loadWorkers = async () => {
  try {
    const res = await api.get('workers/')
    workers.value = res.data
  } catch (e) {
    console.error('Ошибка загрузки сотрудников', e)
  }
}

const createWorker = () => {
  router.push('/workers/new')
}

const editWorker = (id) => {
  router.push(`/workers/${id}/edit`)
}

const deleteWorker = async (id) => {
  const confirmDelete = confirm('Вы точно хотите удалить этого сотрудника?')
  if (!confirmDelete) return

  try {
    await api.delete(`workers/${id}/`)
    alert('Сотрудник успешно удалён')
    await loadWorkers()
  } catch (e) {
    console.error('Ошибка при удалении сотрудника', e)
    alert('Ошибка при удалении сотрудника')
  }
}

onMounted(() => {
  loadWorkers()
})
</script>
