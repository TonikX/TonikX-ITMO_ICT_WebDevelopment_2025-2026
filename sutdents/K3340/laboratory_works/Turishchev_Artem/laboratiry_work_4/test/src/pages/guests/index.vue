<template>
  <v-container>
    <div class="d-flex justify-space-between align-center mb-4">
      <h2>Гости отеля</h2>
      <v-btn color="primary" to="/guests/new">+ Добавить гостя</v-btn>
    </div>

    <v-card v-if="loading" class="pa-4">
      <v-skeleton-loader type="list-item-three-line"></v-skeleton-loader>
    </v-card>

    <v-alert v-else-if="error" type="error">{{ error }}</v-alert>

    <GuestCard
        v-for="guest in guests"
        :key="guest.id"
        :guest="guest"
        @delete="confirmDelete(guest)"
      />
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';
import GuestCard from '@/components/GuestCard.vue';


const guests = ref([]);
const loading = ref(false);
const error = ref(null);
const router = useRouter();

const fetchGuests = async () => {
  loading.value = true;
  error.value = null;
  try {
    const res = await api.get('api/guest/');
    guests.value = res.data;
  } catch (err) {
    error.value = 'Не удалось загрузить список Гостей';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const confirmDelete = (guest) => {
  if (confirm(`Удалить гостя ${ guest.last_name } ${guest.first_name } ${ guest.patronymic }? Это действие нельзя отменить.`)) {
    deleteGuest(guest.id);
  }
};

const deleteGuest = async (id) => {
  try {
    await api.delete(`api/guest/${id}/`);
    fetchGuests(); 
  } catch (err) {
    alert('Ошибка при гостя');
    console.error(err);
  }
};

onMounted(() => {
  fetchGuests();
});
</script>