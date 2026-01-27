<template>
  <v-container>
    <v-card class="pa-6">
      <v-card-title>Добавить новый этаж</v-card-title>
      <v-form @submit.prevent="submit">
        <v-text-field
          v-model.number="form.number"
          label="Номер этажа"
          type="number"
          required
          :rules="[v => !!v || 'Обязательно']"
        ></v-text-field>

        <v-textarea
          v-model="form.description"
          label="Описание (опционально)"
          rows="3"
        ></v-textarea>

        <v-card-actions>
          <v-btn to="/floors" variant="outlined">Отмена</v-btn>
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
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';

const form = ref({
  number: null,
  description: '',
});
const loading = ref(false);
const router = useRouter();

const submit = async () => {
  if (!form.value.number) return;
  loading.value = true;
  try {
    await api.post('api/floor/', form.value);
    router.push('/floors');
  } catch (err) {
    const errors = err.response?.data;
    let msg = 'Ошибка создания этажа';
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