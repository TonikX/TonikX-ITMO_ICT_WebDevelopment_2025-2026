<template>
  <v-container>
    <v-card class="pa-6">
      <v-card-title>Добавить нового гостя</v-card-title>
      <v-form @submit.prevent="submit">
        <v-text-field
          v-model="form.passport_number"
          label="Номер паспорта"
          required
          :rules="[v => !!v || 'Обязательное поле']"
        ></v-text-field>

        <v-text-field
          v-model="form.last_name"
          label="Фамилия"
          required
          :rules="[v => !!v || 'Обязательное поле']"
        ></v-text-field>

        <v-text-field
          v-model="form.first_name"
          label="Имя"
          required
          :rules="[v => !!v || 'Обязательное поле']"
        ></v-text-field>

        <v-text-field
          v-model="form.patronymic"
          label="Отчество (опционально)"
        ></v-text-field>

        <v-text-field
          v-model="form.city"
          label="Город"
          required
          :rules="[v => !!v || 'Обязательное поле']"
        ></v-text-field>

        <v-card-actions>
          <v-btn to="/guests" variant="outlined">Отмена</v-btn>
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
  passport_number: '',
  last_name: '',
  first_name: '',
  patronymic: '',
  city: ''
});
const loading = ref(false);
const router = useRouter();

const submit = async () => {
  loading.value = true;
  try {
    await api.post('api/guest/', form.value);
    router.push('/guests');
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