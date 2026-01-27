<template>
  <v-container>
    <v-btn to="/cleaningSchedules" icon="mdi-arrow-left" class="mb-4"></v-btn>
    <CleaningScheduleCard 
      v-if="cleaningSchedule.id"
      :cleaningSchedule="cleaningSchedule"
      @delete="handleDeleteCleaningSchedule" 
    />

    <h3 class="mt-6 mb-4">Сотрудник</h3>
    <StaffCard 
      v-if="staff.id"
      :staff="staff" 
      :disableDelete="true"
    />

    <h3 class="mt-6 mb-4">Этаж</h3>
    <FloorCard
      v-if="floor.id"
      :floor="floor"
      :disableDelete="true"
    />
    
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/api';
import CleaningScheduleCard from '@/components/CleaningScheduleCard.vue';
import StaffCard from '@/components/StaffCard.vue';
import FloorCard from '@/components/FloorCard.vue';

const route = useRoute();
const router = useRouter();
const cleaningSchedule = ref({});
const floor = ref([]);
const staff = ref([]);
const loading = ref(false);
const error = ref(null);
console.log('1')
const fetch = async () => {
  loading.value = true;
  error.value = null;
  try {
    console.log('1');
    const cleaningScheduleRes = await api.get(`api/cleaning_schedule/${route.params.id}/`);
    console.log(cleaningScheduleRes.data);
    cleaningSchedule.value = cleaningScheduleRes.data;
    floor.value = cleaningSchedule.value.floor;
    staff.value = cleaningSchedule.value.staff;
    console.log(staff.value);
  } catch (err) {
    error.value = 'Не удалось загрузить информацию об уборке';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  fetch();
});

const handleDeleteCleaningSchedule = () => {
  if (confirm(`Удалить уборку ${cleaningSchedule.value.number}?`)) {
    deleteCleaningSchedule();
  }
};

const deleteCleaningSchedule = async () => {
  try {
    await api.delete(`/cleaning_schedule/${cleaningSchedule.value.id}/`);
    router.push('/cleaningSchedules');
  } catch (err) {
    alert('Не удалось удалить уборку');
    console.error(err);
  }
};
</script>