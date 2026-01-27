<template>
  <v-container>
    <v-btn to="/livingRecords" icon="mdi-arrow-left" class="mb-4"></v-btn>
    <LivingRecordCard 
      v-if="livingRecord.id"
      :livingRecord="livingRecord"
      @delete="handleDeleteLivingRecord" 
    />

    <h3 class="mt-6 mb-4">Гость</h3>
    <GuestCard 
      v-if="guest.id"
      :guest="guest" 
      :disableDelete="true"
    />

    <h3 class="mt-6 mb-4">Номер</h3>
    <RoomCard
      v-if="room.id"
      :room="room"
      :floor="room.floor"
      :disableDelete="true"
    />
    
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/api';
import LivingRecordCard from '@/components/LivingRecordCard.vue';
import GuestCard from '@/components/GuestCard.vue';
import RoomCard from '@/components/RoomCard.vue';

const route = useRoute();
const router = useRouter();
const livingRecord = ref({});
const room = ref([]);
const guest = ref([]);
const loading = ref(false);
const error = ref(null);
console.log('1')
const fetch = async () => {
  loading.value = true;
  error.value = null;
  try {
    console.log('1');
    const livingRecordRes = await api.get(`api/living_record/${route.params.id}/`);
    console.log(livingRecordRes.data);
    livingRecord.value = livingRecordRes.data;
    room.value = livingRecord.value.room;
    guest.value = livingRecord.value.guest;
    console.log(guest.value);
  } catch (err) {
    error.value = 'Не удалось загрузить информацию о записи проживания';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  fetch();
});

const handleDeleteLivingRecord = () => {
  if (confirm(`Удалить запись о проживании ${livingRecord.value.number}?`)) {
    deleteLivingRecord();
  }
};

const deleteLivingRecord = async () => {
  try {
    await api.delete(`/living_record/${livingRecord.value.id}/`);
    router.push('/livingRecords');
  } catch (err) {
    alert('Не удалось удалить запись о проживании');
    console.error(err);
  }
};
</script>