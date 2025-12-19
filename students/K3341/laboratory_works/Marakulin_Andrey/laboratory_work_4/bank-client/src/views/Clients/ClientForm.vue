<template>
  <v-card class="pa-4 mx-auto" max-width="600">
    <v-card-title>{{ isEdit ? 'Редактирование клиента' : 'Новый клиент' }}</v-card-title>
    <v-form @submit.prevent="submit">
      <v-text-field v-model="form.fio" label="ФИО" required></v-text-field>
      <v-text-field v-model="form.phone" label="Телефон" required></v-text-field>
      <v-textarea v-model="form.address" label="Адрес"></v-textarea>
      <v-text-field v-model="form.email" label="Email"></v-text-field>

      <div class="d-flex gap-2 mt-4">
        <v-btn type="submit" color="primary">Сохранить</v-btn>
        <v-btn variant="text" to="/clients">Отмена</v-btn>
      </div>
    </v-form>
  </v-card>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../../api/axios';

const route = useRoute();
const router = useRouter();
const isEdit = computed(() => !!route.params.id);

const form = reactive({ fio: '', phone: '', address: '', email: '' });

onMounted(async () => {
  if (isEdit.value) {
    const res = await api.get(`/api/v1/clients/${route.params.id}/`);
    Object.assign(form, res.data);
  }
});

const submit = async () => {
  try {
    if (isEdit.value) {
      await api.patch(`/api/v1/clients/${route.params.id}/`, form);
    } else {
      await api.post('/api/v1/clients/', form);
    }
    router.push('/clients');
  } catch (e) {
    alert('Ошибка сохранения');
  }
};
</script>