<template>
  <v-container>
    <div class="d-flex justify-space-between align-center mb-4">
      <h2>Сотрудник</h2>
      <v-btn color="primary" to="/livingRecords/new">+ Добавить запись о проживании</v-btn>
    </div>
    <v-btn to="/staff" icon="mdi-arrow-left" class="mb-4"></v-btn>
    <StaffCard 
    v-if="staff.id"
    :staff="staff" 
    @delete="handleDeleteStaff" 
    />
    <v-btn
      color="success"
      class="mt-4"
      :to="`/cleaningSchedules/new?staff=${staff.id}`"
    >
      + Добавить Уборку
    </v-btn>

    <h3 class="mt-6 mb-4">Уборки</h3>

    <div v-if="loading">Загрузка уборок...</div>

    <div v-else-if="cleaningSchedules.length === 0">
      У данного сотрудника нет назначенных уборок
    </div>

    <div v-else>
      <CleaningScheduleCard
        v-for="cleaningSchedule in cleaningSchedules"
        :key="cleaningSchedule.id"
        :cleaningSchedule="cleaningSchedule"
        @delete="confirmDeleteCleaningSchedule(cleaningSchedule)"
      />
    </div>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/api';
import StaffCard from '@/components/StaffCard.vue';
import CleaningScheduleCard from '@/components/CleaningScheduleCard.vue';

const route = useRoute();
const router = useRouter();
const staff = ref({});
const cleaningSchedules = ref([]);
const loading = ref(false);
const error = ref(null);

const fetch = async () => {
  loading.value = true;
  error.value = null;
  try {
    const staffRes = await api.get(`api/staff/${route.params.id}/`);
    staff.value = staffRes.data;
    cleaningSchedules.value = staff.value.cleaning_schedules;
  } catch (err) {
    error.value = 'Не удалось загрузить информацию о сотруднике';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  fetch();
});

const handleDeleteStaff = () => {
  if (confirm(`Удалить сотрудника ${staff.value.number}?`)) {
    deleteStaff();
  }
};

const deleteStaff = async () => {
  try {
    await api.delete(`/staff/${staff.value.id}/`);
    router.push('/staff');
  } catch (err) {
    alert('Не удалось удалить сотрудника');
    console.error(err);
  }
};

const confirmDeleteCleaningSchedule = (cleaningSchedule) => {
  if (confirm(`Удалить уборку ${cleaningSchedule.id}?`)) {
    deleteCleaningSchedule(cleaningSchedule.id);
  }
};

const deleteCleaningSchedule = async (cleaningScheduleId) => {
  try {
    await api.delete(`/cleaning_schedule/${cleaningScheduleId}/`);
    fetch();
  } catch (err) {
    alert('Не удалось удалить уборку');
    console.error(err);
  }
};
</script>