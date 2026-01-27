<template>
  <v-container>
    <div class="d-flex justify-space-between align-center mb-4">
      <h2>календарь уборок</h2>
      <v-btn color="primary" to="/cleaningSchedules/new">+ Добавить уборку</v-btn>
    </div>

    <v-card v-if="loading" class="pa-4">
      <v-skeleton-loader type="list-item-three-line"></v-skeleton-loader>
    </v-card>

    <v-alert v-else-if="error" type="error">{{ error }}</v-alert>

    <CleaningScheduleCard
        v-for="cleaningSchedule in cleaningSchedules"
        :key="cleaningSchedule.id"
        :cleaningSchedule="cleaningSchedule"
        @delete="confirmDelete(cleaningSchedule)"
      />
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';
import CleaningScheduleCard from '@/components/CleaningScheduleCard.vue';


const cleaningSchedules = ref([]);
const loading = ref(false);
const error = ref(null);
const router = useRouter();

const fetchCleaningSchedules = async () => {
  loading.value = true;
  error.value = null;
  try {
    const res = await api.get('api/cleaning_schedule/');
    cleaningSchedules.value = res.data;
  } catch (err) {
    error.value = 'Не удалось загрузить календарь уборок';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const confirmDelete = (cleaningSchedule) => {
  if (confirm(`Удалить уборку ${ cleaningSchedule.id }? Это действие нельзя отменить.`)) {
    deleteCleaningSchedule(cleaningSchedule.id);
  }
};

const deleteCleaningSchedule = async (id) => {
  try {
    await api.delete(`api/cleaning_schedule/${id}/`);
    fetchCleaningSchedules(); 
  } catch (err) {
    alert('Ошибка при удалении уборки');
    console.error(err);
  }
};

onMounted(() => {
  fetchCleaningSchedules();
});
</script>