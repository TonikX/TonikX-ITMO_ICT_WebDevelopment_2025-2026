<template>
  <v-container>
    <div class="d-flex justify-space-between align-center mb-4">
      <h2>Комнаты отеля</h2>
      <v-btn color="primary" to="/rooms/new">+ Добавить комнату</v-btn>
    </div>

    <v-card v-if="loading" class="pa-4">
      <v-skeleton-loader type="list-item-three-line"></v-skeleton-loader>
    </v-card>

    <v-alert v-else-if="error" type="error">{{ error }}</v-alert>

    <RoomCard
        v-for="room in rooms"
        :key="room.id"
        :room="room"
        :floor="room.floor"
        @delete="confirmDelete(room)"
      />
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';
import RoomCard from '@/components/RoomCard.vue';


const rooms = ref([]);
const loading = ref(false);
const error = ref(null);
const router = useRouter();

const fetchRooms = async () => {
  loading.value = true;
  error.value = null;
  try {
    const res = await api.get('api/room/');
    rooms.value = res.data;
  } catch (err) {
    error.value = 'Не удалось загрузить список номеров';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const confirmDelete = (room) => {
  if (confirm(`Удалить гостя ${ room.number }? Это действие нельзя отменить.`)) {
    deleteRoom(room.id);
  }
};

const deleteRoom = async (id) => {
  try {
    await api.delete(`api/room/${id}/`);
    fetchRooms(); 
  } catch (err) {
    alert('Ошибка при удалении номера');
    console.error(err);
  }
};

onMounted(() => {
  fetchRooms();
});
</script>