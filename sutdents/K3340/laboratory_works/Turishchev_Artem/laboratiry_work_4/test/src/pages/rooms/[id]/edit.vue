<template>
  <v-container>
    <v-card class="pa-6">
      <v-card-title>Изменить номер</v-card-title>
      <v-form @submit.prevent="submit">
        <v-text-field
          v-model="form.number"
          label="Номер комнаты"
          required
          :rules="[v => !!v || 'Обязательное поле']"
        ></v-text-field>
        <v-select
          v-model="form.room_type"
          :items="roomTypeOptions"
          label="Тип номера"
          required
          :rules="[v => !!v || 'Обязательное поле']"
        ></v-select>
        <v-text-field
          v-model.number="form.price"
          label="Стоимость за день (₽)"
          type="number"
          step="0.01"
          min="0"
          required
          :rules="[v => v != null && v >= 0 || 'Укажите корректную стоимость']"
        ></v-text-field>
        <v-text-field
          v-model="form.phone"
          label="Телефон в номере"
          required
          :rules="[v => !!v || 'Обязательное поле']"
        ></v-text-field>
        <v-text-field
          v-model.number="form.floor"
          label="Этаж"
          type="number"
          required
          :rules="[v => !!v || 'Выберите этаж']"
        ></v-text-field>

        <v-card-actions>
          <v-btn to="/rooms" variant="outlined">Отмена</v-btn>
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
import { useRoute, useRouter } from 'vue-router';
import api from '@/api';

const route = useRoute();
const router = useRouter();
const form = ref({
  number: '',
  room_type: '',
  price: null,
  phone: '',
  floor: null,
});
const roomTypeOptions = [
        { value: 'single', title: 'Одноместный' },
        { value: 'double', title: 'Двухместный' },
        { value: 'triple', title: 'Трехместный' },
      ]
const loading = ref(false);
const roomId = route.params.id;

onMounted(async () => {
  try {
    const res = await api.get(`api/room/${roomId}/`);
    form.value = { ...res.data };
    form.value.floor = res.data.floor.id;
  } catch (err) {
    alert('Не удалось загрузить данные гостя');
    console.error(err);
  }
});

const submit = async () => {
  loading.value = true;
  try {
    await api.put(`api/room/${roomId}/`, form.value);
    router.push(`/rooms/${roomId}`);
  } catch (err) {
    const errors = err.response?.data;
    let msg = 'Ошибка обновления';
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