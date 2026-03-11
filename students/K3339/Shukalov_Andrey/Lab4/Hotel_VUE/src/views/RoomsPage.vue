<template>
  <v-container>
    <v-container>
      <h1>Все номера</h1>
      <v-btn v-if="!addingRoom" @click="addingRoom = true" color="primary">Добавить номер</v-btn>
    </v-container>
    <v-container>
      <v-form @submit.prevent="addRoom" v-if="addingRoom">
        <v-text-field v-model="newRoom.number" label="Номер комнаты" type="number" required></v-text-field>
        <v-text-field v-model="newRoom.price" label="Цена" type="number" required></v-text-field>
        <v-select v-model="newRoom.room_type" :items="roomType" label="Тип номера" required></v-select>
        <v-text-field v-model="newRoom.floor" label="Этаж" type="number" required></v-text-field>
        <v-text-field v-model="newRoom.phone" label="Телефон" required></v-text-field>

        <v-btn color="primary" type="submit">Добавить</v-btn>
        <v-btn @click="addingRoom = false" color="secondary">Отмена</v-btn>
      </v-form>
    </v-container>
    <v-row>
      <v-col v-for="room in rooms" :key="room.id" cols="12" md="4">
        <RoomCard :room="room" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import RoomCard from '@/components/RoomCard.vue';

const rooms = ref([]);

const fetchRooms = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/rooms/');
    rooms.value = response.data;
  } catch (error) {
    console.error('Ошибка при получении списка комнат:', error);
  }
};

const addingRoom = ref(false);
const newRoom = ref({
  number: '',
  price: '',
  room_type: '',
  floor: '',
  phone: '',
});
const roomType = ref(['single', 'double', 'triple']);

const addRoom = async () => {
  try {
    await axios.post('http://localhost:8000/api/rooms/', newRoom.value);
    alert('Номер добавлен');
    addingRoom.value = false;
    newRoom.value = { number: '', price: '', room_type: '', floor: '', phone: '' };
    fetchRooms();
  } catch (error) {
    console.error('Ошибка при добавлении комнаты', error);
    alert('Ошибка при добавлении комнаты');
  }
};

onMounted(() => {
  fetchRooms();
});

</script>
<style scoped></style>