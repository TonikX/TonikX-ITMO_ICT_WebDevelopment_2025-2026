<template>
  <v-container>
    <div class="d-flex justify-space-between align-center mb-4">
      <h2>записи уборок</h2>
      <v-btn color="primary" to="/cleaningRecords/new">+ Добавить запись об уборку</v-btn>
    </div>

    <v-card v-if="loading" class="pa-4">
      <v-skeleton-loader type="list-item-three-line"></v-skeleton-loader>
    </v-card>

    <v-alert v-else-if="error" type="error">{{ error }}</v-alert>

    <CleaningRecordCard
        v-for="cleaningRecord in cleaningRecords"
        :key="cleaningRecord.id"
        :cleaningRecord="cleaningRecord"
        @delete="confirmDelete(cleaningRecord)"
      />
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';
import CleaningRecordCard from '@/components/CleaningRecordCard.vue';


const cleaningRecords = ref([]);
const loading = ref(false);
const error = ref(null);
const router = useRouter();

const fetchCleaningRecords = async () => {
  loading.value = true;
  error.value = null;
  try {
    const res = await api.get('api/cleaning_record/');
    cleaningRecords.value = res.data;
  } catch (err) {
    error.value = 'Не удалось загрузить записи уборок';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const confirmDelete = (cleaningRecord) => {
  if (confirm(`Удалить запись об уборке ${ cleaningRecord.id }? Это действие нельзя отменить.`)) {
    deleteCleaningRecord(cleaningRecord.id);
  }
};

const deleteCleaningRecord = async (id) => {
  try {
    await api.delete(`api/cleaning_record/${id}/`);
    fetchCleaningRecords(); 
  } catch (err) {
    alert('Ошибка при удалении записи об уборке');
    console.error(err);
  }
};

onMounted(() => {
  fetchCleaningRecords();
});
</script>