<template>
  <v-container>
    <v-card class="pa-6">
      <v-card-title class="text-h5">Гости за период по номеру</v-card-title>
      
      <v-card-text>
        <v-form @submit.prevent="fetchGuests">
          <v-select
            v-model="form.room_id"
            :items="rooms"
            item-title="number"
            item-value="id"
            label="Номер"
            variant="outlined"
            required
          ></v-select>

          <v-text-field
            v-model="form.start_date"
            label="Дата начала"
            type="date"
            variant="outlined"
            required
          ></v-text-field>

          <v-text-field
            v-model="form.end_date"
            label="Дата окончания"
            type="date"
            variant="outlined"
            required
          ></v-text-field>

          <v-btn
            type="submit"
            color="primary"
            :loading="loading"
          >
            Найти гостей
          </v-btn>
        </v-form>

        <div v-if="guests.length > 0" class="mt-4">
          <h3 class="mb-3">Результаты ({{ guests.length }} гостей):</h3>
          <GuestCard
            v-for="guest in guests"
            :key="guest.id"
            :guest="guest"
            :disable-delete="true"
          />
        </div>

        <v-alert v-else-if="guests.length === 0 && !loading && submitted" type="info" class="mt-4">
          Гости не найдены
        </v-alert>

        <v-alert v-if="error" type="error" class="mt-4">
          {{ error }}
        </v-alert>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';
import GuestCard from '@/components/GuestCard.vue';

const form = ref({
  room_id: null,
  start_date: '',
  end_date: ''
});
const rooms = ref([]);
const guests = ref([]);
const loading = ref(false);
const error = ref(null);
const submitted = ref(false);

onMounted(async () => {
  try {
    const res = await api.get('api/room/');
    rooms.value = res.data;
  } catch (err) {
    error.value = 'Не удалось загрузить список номеров';
    console.error(err);
  }
});

const fetchGuests = async () => {
  if (!form.value.room_id || !form.value.start_date || !form.value.end_date) return;
  
  loading.value = true;
  error.value = null;
  guests.value = [];
  submitted.value = true;
  try {
    const res = await api.get('api/guest/by_room_period/', {
      params: {
        room_id: form.value.room_id,
        start_date: form.value.start_date,
        end_date: form.value.end_date
      }
    });
    guests.value = res.data;
  } catch (err) {
    error.value = 'Не удалось получить данные';
    console.error(err);
  } finally {
    loading.value = false;
  }
};
</script>
