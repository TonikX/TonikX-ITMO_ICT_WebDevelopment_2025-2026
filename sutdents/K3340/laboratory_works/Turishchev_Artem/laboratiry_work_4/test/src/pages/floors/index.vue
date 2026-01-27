<template>
  <v-container>
    <div class="d-flex justify-space-between align-center mb-4">
      <h2>Этажи отеля</h2>
      <v-btn color="primary" to="/floors/new">+ Добавить этаж</v-btn>
    </div>

    <v-card v-if="loading" class="pa-4">
      <v-skeleton-loader type="list-item-three-line"></v-skeleton-loader>
    </v-card>

    <v-alert v-else-if="error" type="error">{{ error }}</v-alert>

    <FloorCard
        v-for="floor in floors"
        :key="floor.id"
        :floor="floor"
        @delete="confirmDelete(floor)"
      />
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';
import FloorCard from '@/components/FloorCard.vue';

const floors = ref([]);
const loading = ref(false);
const error = ref(null);
const router = useRouter();

const fetchFloors = async () => {
  loading.value = true;
  error.value = null;
  try {
    const res = await api.get('api/floor/');
    floors.value = res.data;
  } catch (err) {
    error.value = 'Не удалось загрузить список этажей';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const confirmDelete = (floor) => {
  if (confirm(`Удалить этаж №${floor.number}? Это действие нельзя отменить.`)) {
    deleteFloor(floor.id);
  }
};

const deleteFloor = async (id) => {
  try {
    await api.delete(`api/floor/${id}/`);
    fetchFloors(); 
  } catch (err) {
    alert('Ошибка при удалении этажа');
    console.error(err);
  }
};

onMounted(() => {
  fetchFloors();
});
</script>