<template>
  <v-container>
    <v-card>
      <v-card-title>Редактировать уборку</v-card-title>

      <v-card-text>
        <v-text-field
          v-model="form.cleaning_date"
          label="Дата уборки"
          type="date"
          outlined
          dense
        />

        <v-select
          v-model="form.worker"
          :items="workers"
          item-title="fio"
          item-value="id"
          label="Сотрудник"
          outlined
          dense
        />

        <v-select
          v-model="form.room"
          :items="rooms"
          item-title="room_number"
          item-value="id"
          label="Номер комнаты"
          outlined
          dense
        />

        <v-btn
          color="success"
          class="mt-3 mr-2"
          @click="save"
        >
          Сохранить
        </v-btn>

        <v-btn
          color="grey"
          class="mt-3"
          @click="goBack"
        >
          Отмена
        </v-btn>

        <v-alert
          v-if="error"
          type="error"
          class="mt-3"
          dense
        >
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

const route = useRoute()
const router = useRouter()

const form = ref({
  cleaning_date: '',
  worker: null,
  room: null
})

const workers = ref([])
const rooms = ref([])
const error = ref('')

const loadCleaning = async () => {
  const res = await api.get(`cleaning/${route.params.id}/`)
  form.value = {
    cleaning_date: res.data.cleaning_date.slice(0, 10),
    worker: res.data.worker,
    room: res.data.room
  }
}

const loadWorkers = async () => {
  const res = await api.get('workers/')
  workers.value = res.data.map(w => ({
    id: w.id,
    fio: `${w.surname} ${w.name} ${w.patronymic}`
  }))
}

const loadRooms = async () => {
  const res = await api.get('rooms/')
  rooms.value = res.data
}

const save = async () => {
  error.value = ''
  try {
    await api.patch(`cleaning/${route.params.id}/`, {
      cleaning_date: form.value.cleaning_date,
      worker: form.value.worker,
      room: form.value.room
    })
    router.push('/cleaning')
  } catch (e) {
    console.error(e)
    error.value = 'Ошибка сохранения'
  }
}

const goBack = () => {
  router.push('/cleaning')
}

onMounted(async () => {
  try {
    await Promise.all([
      loadCleaning(),
      loadWorkers(),
      loadRooms()
    ])
  } catch (e) {
    console.error(e)
    error.value = 'Ошибка загрузки данных'
  }
})
</script>
