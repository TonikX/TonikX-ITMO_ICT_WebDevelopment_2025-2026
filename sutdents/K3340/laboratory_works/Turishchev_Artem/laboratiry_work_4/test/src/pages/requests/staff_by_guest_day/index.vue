<template>
  <v-container>
    <v-card class="pa-6">
      <v-card-title class="text-h5">Сотрудник, который убирал номер клиента в заданный день</v-card-title>
      
      <v-card-text>
        <v-form @submit.prevent="fetchStaff">
          <v-select
            v-model="form.guest_id"
            :items="guests"
            item-value="id"
            label="Гость"
            variant="outlined"
            required
          >
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :title="`${item.raw.last_name} ${item.raw.first_name} ${item.raw.patronymic}`"></v-list-item>
            </template>
            <template v-slot:selection="{ item }">
              {{ item.raw.last_name }} {{ item.raw.first_name }} {{ item.raw.patronymic }}
            </template>
          </v-select>

          <v-text-field
            v-model="form.date"
            label="Дата"
            type="date"
            variant="outlined"
            required
          ></v-text-field>

          <v-btn
            type="submit"
            color="primary"
            :loading="loading"
          >
            Найти сотрудника
          </v-btn>
        </v-form>

        <div v-if="staff" class="mt-4">
          <h3 class="mb-3">Результат:</h3>
          <StaffCard
            :staff="staff"
            :disable-delete="true"
          />
        </div>

        <v-alert v-else-if="!staff && !loading && submitted" type="info" class="mt-4">
          Сотрудник не найден
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
import StaffCard from '@/components/StaffCard.vue';

const form = ref({
  guest_id: null,
  date: ''
});
const guests = ref([]);
const staff = ref(null);
const loading = ref(false);
const error = ref(null);
const submitted = ref(false);

onMounted(async () => {
  try {
    const res = await api.get('api/guest/');
    guests.value = res.data;
  } catch (err) {
    error.value = 'Не удалось загрузить список гостей';
    console.error(err);
  }
});

const fetchStaff = async () => {
  if (!form.value.guest_id || !form.value.date) return;
  
  loading.value = true;
  error.value = null;
  staff.value = null;
  submitted.value = true;
  try {
    const res = await api.get('api/staff/by_guest_day/', {
      params: {
        guest_id: form.value.guest_id,
        date: form.value.date
      }
    });
    staff.value = res.data;
  } catch (err) {
    error.value = err.response?.data?.error || 'Не удалось получить данные';
    console.error(err);
  } finally {
    loading.value = false;
  }
};
</script>
