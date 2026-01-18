<template>
  <v-container>
    <v-card>
      <v-card-title>Редактировать сотрудника</v-card-title>

      <v-card-text>
        <v-text-field
          v-model="worker.name"
          label="Имя"
          outlined
          dense
        ></v-text-field>

        <v-text-field
          v-model="worker.surname"
          label="Фамилия"
          outlined
          dense
        ></v-text-field>

        <v-text-field
          v-model="worker.patronymic"
          label="Отчество"
          outlined
          dense
        ></v-text-field>

        <v-switch
          v-model="worker.is_employed"
          label="Работает"
          inset
        ></v-switch>
        <v-btn color="green lighten-2" class="mt-3 mr-2" @click="updateWorker">
          Сохранить изменения
        </v-btn>

        <v-divider class="my-4"></v-divider>

        <h3>График уборок</h3>

        <v-data-table
          :headers="cleaningHeaders"
          :items="cleanings"
          item-key="id"
          class="elevation-1 mb-3"
        >
          <template #item.week_day="{ item }">
            <v-select
              v-model="item.week_day"
              :items="weekDays"
              label="День недели"
              dense
            ></v-select>
          </template>

          <template #item.floor="{ item }">
            <v-text-field v-model="item.floor" type="number" dense></v-text-field>
          </template>

          <template #item.actions="{ item }">
            <v-btn color="green lighten-2" small class="mr-2" @click="updateCleaning(item)">Сохранить</v-btn>
            <v-btn color="red" small @click="deleteCleaning(item.id)">Удалить</v-btn>
          </template>
        </v-data-table>

        <v-btn color="green lighten-2" @click="addCleaningRow">Добавить запись</v-btn>

        <v-divider class="my-4"></v-divider>



        <v-btn color="grey lighten-1" class="mt-3" @click="goBack">
          К списку сотрудников
        </v-btn>

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
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()
const route = useRoute()

const worker = ref({
  name: '',
  surname: '',
  patronymic: '',
  is_employed: true
})

const success = ref('')
const error = ref('')

const cleanings = ref([])
const weekDays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
const cleaningHeaders = [
  { title: 'День недели', key: 'week_day' },
  { title: 'Этаж', key: 'floor' },
  { title: '', key: 'actions', sortable: false }
]

const loadWorker = async () => {
  try {
    const res = await api.get(`workers/${route.params.id}/`)
    worker.value = res.data
  } catch (e) {
    console.error('Ошибка загрузки сотрудника', e)
    error.value = 'Ошибка загрузки данных сотрудника'
  }
}

const loadCleanings = async () => {
  try {
    const res = await api.get(`cleaning_info/?id_worker=${route.params.id}`)
    cleanings.value = res.data
  } catch (e) {
    console.error('Ошибка загрузки уборок', e)
  }
}

const updateWorker = async () => {
  success.value = ''
  error.value = ''

  try {
    await api.patch(`workers/${route.params.id}/`, worker.value)
    success.value = 'Сотрудник успешно обновлён'
  } catch (e) {
    console.error(e)
    error.value = 'Ошибка при обновлении сотрудника'
  }
}

const deleteCleaning = async (id) => {
  try {
    await api.delete(`cleaning_info/${id}/`)
    cleanings.value = cleanings.value.filter(c => c.id !== id)
  } catch (e) {
    console.error(e)
    alert('Ошибка при удалении уборки')
  }
}

const updateCleaning = async (item) => {
  try {
    await api.patch(`cleaning_info/${item.id}/`, {
      week_day: item.week_day,
      floor: item.floor,
      id_worker: route.params.id
    })
    alert('Уборка обновлена')
  } catch (e) {
    console.error(e)
    alert('Ошибка при обновлении уборки')
  }
}

const addCleaningRow = async () => {
  try {
    const res = await api.post('cleaning_info/', {
      week_day: 'mon',
      floor: 1,
      id_worker: route.params.id
    })
    cleanings.value.push(res.data)
  } catch (e) {
    console.error('Ошибка при создании новой уборки', e)
    alert('Не удалось добавить новую запись уборки')
  }
}

const goBack = () => {
  router.push('/workers')
}

onMounted(async () => {
  await Promise.all([loadWorker(), loadCleanings()])
})
</script>
