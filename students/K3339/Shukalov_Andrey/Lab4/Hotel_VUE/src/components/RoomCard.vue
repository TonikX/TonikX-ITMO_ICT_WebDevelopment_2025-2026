<template>
  <v-card class="mb-3" max-width="400px">
    <v-card-title>Номер {{ room.number }}</v-card-title>
    <v-card-subtitle>Тип: {{ room.room_type }} | Этаж: {{ room.floor }}</v-card-subtitle>
    <v-card-text>
      <p>Цена: {{ room.price }}</p>
      <p>Телефон: {{ room.phone }}</p>
      <p :style="{ color: room.free ? 'green' : 'red' }">
        {{ room.free ? 'Свободна' : 'Занята' }}
      </p>
    </v-card-text>
    <v-card-actions>
      <v-btn v-if="room.free" @click="deleteRoom(room.id)" color="red" small>Удалить</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { useRouter } from 'vue-router';
import axios from 'axios';

const props = defineProps({
  room: Object,
});

const router = useRouter();

const deleteRoom = async (id) => {
  try {
    await axios.delete(`http://localhost:8000/api/rooms/${id}/`);
    router.go(); // обновляем список после удаления
  } catch (error) {
    console.error('Ошибка при удалении комнаты:', error);
  }
};
</script>

<style scoped></style>