<template>
  <v-container>
    <v-btn to="/rooms" icon="mdi-arrow-left" class="mb-4"></v-btn>
    <RoomCard
      v-if="room.id"
      :room="room"
      :floor="room.floor.id"
      @delete="handleDeleteRoom"
    />

    <v-btn
      v-if="room.id"
      color="success"
      class="mt-4"
      :to="`/livingRecords/new?room=${room.id}`"
    >
      + Добавить запись о проживании
    </v-btn>

    <h3 class="mt-6 mb-4">Сегодня убирает</h3>
    <StaffCard
      v-if="staff"
      :staff="staff"
      :disableDelete="true"
    />

    <h3 class="mt-6 mb-4">Проживания</h3>

    <div v-if="loading">Загрузка записей проживания...</div>

    <div v-else-if="livingRecords.length === 0">
      В этом номере пока нет записей о проживании.
    </div>

    <div v-else>
      <LivingRecordCard
        v-for="livingRecord in livingRecords"
        :key="livingRecord.id"
        :livingRecord="livingRecord"
        @delete="confirmDeleteLivingRecord(livingRecord)"
      />
    </div>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/api';
import RoomCard from '@/components/RoomCard.vue';
import LivingRecordCard from '@/components/LivingRecordCard.vue';
import StaffCard from '@/components/StaffCard.vue';

const route = useRoute();
const router = useRouter();
const room = ref({});
const staff = ref([]);
const livingRecords = ref([]);
const loading = ref(false);
const error = ref(null);

const fetch = async () => {
  loading.value = true;
  error.value = null;
  try {
    const roomRes = await api.get(`api/room/${route.params.id}/`);
    room.value = roomRes.data;
    livingRecords.value = room.value.living_records;

    const today = new Date();
    const todayDayOfWeek = today.getDay() === 0 ? 7 : today.getDay();
    const todaySchedule = room.value.floor.cleaning_schedules.find(
      schedule => schedule.day_of_week === todayDayOfWeek
    );
    const staffForToday = todaySchedule?.staff;
    const staffRes = await api.get(`api/staff/${staffForToday}/`);
    staff.value = staffRes.data;
  } catch (err) {
    error.value = 'Не удалось загрузить информацию о госте';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  fetch();
});

const handleDeleteRoom = () => {
  if (confirm(`Удалить Гостя ${room.value.number}?`)) {
    deleteRoom();
  }
};

const deleteRoom = async () => {
  try {
    await api.delete(`/room/${room.value.id}/`);
    router.push('/rooms');
  } catch (err) {
    alert('Не удалось гостя');
    console.error(err);
  }
};

const confirmDeleteLivingRecord = (livingRecord) => {
  if (confirm(`Удалить запись о проживании ${livingRecord.id}?`)) {
    deleteLivingRecord(livingRecord.id);
  }
};

const deleteLivingRecord = async (livingRecordId) => {
  try {
    await api.delete(`/livingRecord/${livingRecordId}/`);
    fetch();
  } catch (err) {
    alert('Не удалось удалить запись о проживании');
    console.error(err);
  }
};
</script>