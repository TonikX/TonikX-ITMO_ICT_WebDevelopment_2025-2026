<template>
  <v-container>
    <v-card class="pa-6">
      <v-card-title>Изменить этаж</v-card-title>
      <v-form @submit.prevent="submit">
        <v-text-field
          v-model.number="form.number"
          label="Номер этажа"
          type="number"
          required
        ></v-text-field>

        <v-textarea
          v-model="form.description"
          label="Описание"
          rows="3"
        ></v-textarea>

        <v-card-actions>
          <v-btn to="/floors" variant="outlined">Отмена</v-btn>
          <v-spacer></v-spacer>
          <v-btn
            type="submit"
            color="primary"
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
  number: null,
  description: '',
});
const loading = ref(false);
const floorId = route.params.id;

onMounted(async () => {
  try {
    const res = await api.get(`api/floor/${floorId}/`);
    form.value = { ...res.data };
  } catch (err) {
    alert('Не удалось загрузить данные этажа');
    console.error(err);
  }
});

const submit = async () => {
  loading.value = true;
  try {
    await api.put(`api/floor/${floorId}/`, form.value);
    router.push(`/floors/${floorId}`);
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