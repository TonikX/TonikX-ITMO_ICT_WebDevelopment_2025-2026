<template>
  <v-container>
    <v-card class="pa-6">
      <v-card-title class="text-h5">Количество свободных номеров</v-card-title>
      
      <v-card-text>
        <v-btn
          color="primary"
          @click="fetchFreeRooms"
          :loading="loading"
        >
          Получить количество
        </v-btn>

        <v-card v-if="result !== null" class="mt-4 pa-4" color="success" variant="tonal">
          <v-card-title class="text-h3">{{ result }}</v-card-title>
          <v-card-subtitle>свободных номеров</v-card-subtitle>
        </v-card>

        <v-alert v-if="error" type="error" class="mt-4">
          {{ error }}
        </v-alert>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import api from '@/api';

const result = ref(null);
const loading = ref(false);
const error = ref(null);

const fetchFreeRooms = async () => {
  loading.value = true;
  error.value = null;
  result.value = null;
  try {
    const res = await api.get('api/room/count_not_occupied/');
    result.value = res.data;
  } catch (err) {
    error.value = 'Не удалось получить данные';
    console.error(err);
  } finally {
    loading.value = false;
  }
};
</script>
