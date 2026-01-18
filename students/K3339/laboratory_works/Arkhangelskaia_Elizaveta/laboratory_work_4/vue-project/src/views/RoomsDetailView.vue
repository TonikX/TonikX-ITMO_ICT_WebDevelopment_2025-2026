<template>
  <v-container>
    <v-card>
      <v-card-title>Детали номера</v-card-title>

      <v-card-text>
        <v-list>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>Номер комнаты:</v-list-item-title>
              <v-list-item-subtitle>{{ room.room_number }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>Тип номера:</v-list-item-title>
              <v-list-item-subtitle>{{ room.id_room_type?.name }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>Телефон:</v-list-item-title>
              <v-list-item-subtitle>{{ room.phone_number }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>Этаж:</v-list-item-title>
              <v-list-item-subtitle>{{ room.floor }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>

        <v-btn color="primary" @click="editRoom">Редактировать</v-btn>
        <v-btn color="secondary" @click="goBack">Назад</v-btn>
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
const room = ref({})

const loadRoom = async () => {
  try {
    const res = await api.get(`rooms/${route.params.id}/`)
    room.value = res.data
  } catch (e) {
    console.error('Ошибка загрузки комнаты', e)
  }
}

onMounted(() => {
  loadRoom()
})

const editRoom = () => {
  router.push(`/rooms/${route.params.id}/edit`)
}

const goBack = () => {
  router.push('/rooms')
}
</script>
