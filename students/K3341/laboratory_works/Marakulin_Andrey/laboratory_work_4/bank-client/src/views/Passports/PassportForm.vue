<template>
  <v-container>
    <v-card class="pa-4 mx-auto" max-width="600">
      <v-card-title>{{ isEdit ? 'Редактирование паспорта' : 'Новый паспорт' }}</v-card-title>
      <v-form @submit.prevent="submit">

        <v-select
          v-model="form.client"
          :items="clients"
          item-title="fio"
          item-value="id"
          label="Владелец (Клиент)"
          prepend-icon="mdi-account"
          :hint="form.client ? `ID клиента: ${form.client}` : 'Выберите клиента из списка'"
          persistent-hint
          required
        ></v-select>

        <v-row class="mt-2">
          <v-col cols="6">
            <v-text-field v-model="form.series" label="Серия" required></v-text-field>
          </v-col>
          <v-col cols="6">
            <v-text-field v-model="form.number" label="Номер" required></v-text-field>
          </v-col>
        </v-row>

        <v-text-field v-model="form.fio" label="ФИО в паспорте" hint="Должно совпадать с ФИО клиента" required></v-text-field>

        <v-text-field v-model="form.date_issue" label="Дата выдачи" type="date" required></v-text-field>

        <v-textarea v-model="form.issuer" label="Кем выдан" rows="2" required></v-textarea>

        <div class="d-flex gap-2 mt-4">
          <v-btn type="submit" color="primary">Сохранить</v-btn>
          <v-btn variant="text" to="/passports">Отмена</v-btn>
        </div>
      </v-form>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../../api/axios';

const route = useRoute();
const router = useRouter();
const isEdit = computed(() => !!route.params.id);

const clients = ref([]); // Сюда загрузим список клиентов

const form = reactive({
  client: null,
  series: '',
  number: '',
  fio: '',
  date_issue: '',
  issuer: ''
});

// Автозаполнение ФИО паспорта при выборе клиента (удобство)
watch(() => form.client, (newClientId) => {
  if (!isEdit.value && newClientId) { // Только при создании
    const selectedClient = clients.value.find(c => c.id === newClientId);
    if (selectedClient) {
      form.fio = selectedClient.fio;
    }
  }
});

onMounted(async () => {
  try {
    // 1. Загружаем список клиентов для выпадающего списка
    const clientsRes = await api.get('/api/v1/clients/');
    clients.value = clientsRes.data;

    // 2. Если режим редактирования, загружаем данные паспорта
    if (isEdit.value) {
      const passportRes = await api.get(`/api/v1/passports/${route.params.id}/`);
      Object.assign(form, passportRes.data);
    }
  } catch (e) {
    console.error(e);
    alert('Ошибка загрузки данных');
  }
});

const submit = async () => {
  try {
    if (isEdit.value) {
      await api.patch(`/api/v1/passports/${route.params.id}/`, form);
    } else {
      await api.post('/api/v1/passports/', form);
    }
    router.push('/passports');
  } catch (e) {
    console.error(e);
    alert('Ошибка сохранения паспорта. Проверьте консоль.');
  }
};
</script>