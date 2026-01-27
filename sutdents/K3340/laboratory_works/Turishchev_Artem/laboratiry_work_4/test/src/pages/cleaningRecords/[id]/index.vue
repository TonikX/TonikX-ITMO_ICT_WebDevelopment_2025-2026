<template>
  <v-container>
    <v-btn to="/cleaningRecords" icon="mdi-arrow-left" class="mb-4"></v-btn>
    <CleaningRecordCard 
      v-if="cleaningRecord.id"
      :cleaningRecord="cleaningRecord"
      @delete="handleDeleteCleaningRecord" 
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
import CleaningRecordCard from '@/components/CleaningRecordCard.vue';
import StaffCard from '@/components/StaffCard.vue';
import FloorCard from '@/components/FloorCard.vue';

const route = useRoute();
const router = useRouter();
const cleaningRecord = ref({});
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
    const cleaningRecordRes = await api.get(`api/cleaning_record/${route.params.id}/`);
    console.log(cleaningRecordRes.data);
    cleaningRecord.value = cleaningRecordRes.data;
    floor.value = cleaningRecord.value.floor;
    staff.value = cleaningRecord.value.staff;
    console.log(staff.value);
  } catch (err) {
    error.value = 'Не удалось загрузить информацию о записи уборки';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  fetch();
});

const handleDeleteCleaningRecord = () => {
  if (confirm(`Удалить запись об уборке ${cleaningRecord.value.number}?`)) {
    deleteCleaningRecord();
  }
};

const deleteCleaningRecord = async () => {
  try {
    await api.delete(`/cleaning_record/${cleaningRecord.value.id}/`);
    router.push('/cleaningRecords');
  } catch (err) {
    alert('Не удалось удалить запись об уборке');
    console.error(err);
  }
};
</script>