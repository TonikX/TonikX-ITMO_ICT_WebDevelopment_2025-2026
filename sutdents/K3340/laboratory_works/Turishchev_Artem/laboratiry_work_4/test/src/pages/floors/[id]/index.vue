<template>
  <v-container>
    <v-btn to="/floors" icon="mdi-arrow-left" class="mb-4"></v-btn>
    <FloorCard :floor="floor" @delete="handleDeleteFloor" />
    <v-btn
      color="success"
      class="mt-4"
      :to="`/rooms/new?floor=${floor.id}`"
    >
      + Добавить номер
    </v-btn>
    <h3 class="mt-6 mb-4">Сегодня убирает</h3>
    <StaffCard :staff="staff" :disableDelete="true"/>
    <h3 class="mt-6 mb-4">Номера на этаже</h3>
    <div v-if="loadingRooms">Загрузка номеров...</div>

    <div v-else-if="rooms.length === 0">
      На этом этаже пока нет номеров.
    </div>

    <div v-else>
      <RoomCard
        v-for="room in rooms"
        :key="room.id"
        :room="room"
        :floor="room.floor"
        @delete="confirmDeleteRoom(room)"
      />
    </div>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/api';
import FloorCard from '@/components/FloorCard.vue';
import RoomCard from '@/components/RoomCard.vue';
import StaffCard from '@/components/StaffCard.vue';

const route = useRoute();
const router = useRouter();
const floor = ref({});
const rooms = ref([]);
const staff = ref([]);
const loadingRooms = ref(false);
const error = ref(null);

const fetchFloor = async () => {
  loadingRooms.value = true;
  error.value = null;
  try {
    const floorRes = await api.get(`api/floor/${route.params.id}/`);
    floor.value = floorRes.data;
    rooms.value = floor.value.rooms;

    const today = new Date();
    const todayDayOfWeek = today.getDay() === 0 ? 7 : today.getDay();
    const todaySchedule = floor.value.cleaning_schedules.find(
      schedule => schedule.day_of_week === todayDayOfWeek
    );

    const staffForToday = todaySchedule?.staff;
    const staffRes = await api.get(`api/staff/${staffForToday}/`);
    staff.value = staffRes.data;
  } catch (err) {
    error.value = 'Не удалось загрузить информацию о этаже';
    console.error(err);
  } finally {
    loadingRooms.value = false;
  }
};

onMounted(async () => {
  fetchFloor();
});

const handleDeleteFloor = () => {
  if (confirm(`Удалить этаж №${floor.value.number}? Все номера на нём будут удалены!`)) {
    deleteFloor();
  }
};

const deleteFloor = async () => {
  try {
    await api.delete(`/floor/${floor.value.id}/`);
    router.push('/floors');
  } catch (err) {
    alert('Не удалось удалить этаж');
    console.error(err);
  }
};

const confirmDeleteRoom = (room) => {
  if (confirm(`Удалить номер ${room.number}?`)) {
    deleteRoom(room.id);
  }
};

const deleteRoom = async (roomId) => {
  try {
    await api.delete(`/room/${roomId}/`);
    fetchFloor();
  } catch (err) {
    alert('Не удалось удалить номер');
    console.error(err);
  }
};
</script>