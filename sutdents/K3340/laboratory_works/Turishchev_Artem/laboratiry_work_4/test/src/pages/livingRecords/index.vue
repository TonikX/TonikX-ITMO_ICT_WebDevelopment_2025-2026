<template>
  <v-container>
    <div class="d-flex justify-space-between align-center mb-4">
      <h2>Записи о проживании</h2>
      <v-btn color="primary" to="/livingRecords/new">+ Добавить запись о проживании</v-btn>
    </div>

    <v-card v-if="loading" class="pa-4">
      <v-skeleton-loader type="list-item-three-line"></v-skeleton-loader>
    </v-card>

    <v-alert v-else-if="error" type="error">{{ error }}</v-alert>

    <LivingRecordCard
        v-for="livingRecord in livingRecords"
        :key="livingRecord.id"
        :livingRecord="livingRecord"
        @delete="confirmDelete(livingRecord)"
      />
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';
import LivingRecordCard from '@/components/LivingRecordCard.vue';


const livingRecords = ref([]);
const loading = ref(false);
const error = ref(null);
const router = useRouter();

const fetchLivingRecords = async () => {
  loading.value = true;
  error.value = null;
  try {
    const res = await api.get('api/living_record/');
    livingRecords.value = res.data;
  } catch (err) {
    error.value = 'Не удалось загрузить список записей о проживании';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const confirmDelete = (livingRecord) => {
  if (confirm(`Удалить запись о проживании ${ livingRecord.id }? Это действие нельзя отменить.`)) {
    deleteLivingRecord(livingRecord.id);
  }
};

const deleteLivingRecord = async (id) => {
  try {
    await api.delete(`api/living_record/${id}/`);
    fetchLivingRecords(); 
  } catch (err) {
    alert('Ошибка при удалении записи о проживании');
    console.error(err);
  }
};

onMounted(() => {
  fetchLivingRecords();
});
</script>