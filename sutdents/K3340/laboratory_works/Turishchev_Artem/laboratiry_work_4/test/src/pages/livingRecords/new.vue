<template>
  <v-container>
    <v-card class="pa-6">
      <v-card-title>Изменить запись о проживании</v-card-title>
      <v-form @submit.prevent="submit">
        <v-select
          v-model="form.guest"
          :items="guests"
          item-title="passport_number"
          item-value="id"
          label="Гость"
          required
          :rules="[v => !!v || 'Обязательно выбрать гостя']"
        ></v-select>
        <v-select
          v-model="form.room"
          :items="rooms"
          item-title="number"
          item-value="id"
          label="Номер"
          required
          :rules="[v => !!v || 'Обязательно выбрать номер']"
        ></v-select>
        <v-text-field
          v-model="form.start_date"
          label="Дата заезда"
          type="date"
          required
          :rules="[v => !!v || 'Обязательно указать дату заезда']"
        ></v-text-field>
        <v-text-field
          v-model="form.end_date"
          label="Дата выезда (опционально)"
          type="date"
        ></v-text-field>

        <v-card-actions>
          <v-btn to="/livingRecords" variant="outlined">Отмена</v-btn>
          <v-spacer></v-spacer>
          <v-btn
            type="submit"
            color="success"
            :loading="loading"
          >
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';

const form = ref({
  guest: null,
  room: null,
  first_name: '',
  patronymic: '',
});
const loading = ref(false);
const router = useRouter();
const guests = ref([]);
const rooms = ref([]);

onMounted(async () => {
  try {
    const resGuests = await api.get(`api/guest/`);
    guests.value = resGuests.data;
    const resRooms = await api.get(`api/room/`);
    rooms.value = resRooms.data;
  } catch (err) {
    alert('Не удалось загрузить данные');
    console.error(err);
  }
});

const submit = async () => {
  loading.value = true;
  try {
    await api.post('api/living_record/', form.value);
    router.push('/livingRecords');
  } catch (err) {
    const errors = err.response?.data;
    let msg = 'Ошибка создания гостя';
    if (errors) {
      msg = Object.entries(errors)
        .map(([field, msgs]) => `${field}: ${msgs.join(', ')}`)
        .join('\n');
    }
    alert(msg);
    console.error(err);
  } finally {
    loading.value = false;
  }
};
</script>