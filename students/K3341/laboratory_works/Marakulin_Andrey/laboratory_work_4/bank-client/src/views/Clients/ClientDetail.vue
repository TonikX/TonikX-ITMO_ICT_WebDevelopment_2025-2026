<template>
  <div v-if="client">
    <v-btn to="/clients" variant="text" prepend-icon="mdi-arrow-left" class="mb-4">Назад</v-btn>

    <v-card class="pa-4 mb-4">
      <h1 class="text-h4 mb-2">{{ client.fio }}</h1>
      <p><strong>Телефон:</strong> {{ client.phone }}</p>
      <p><strong>Адрес:</strong> {{ client.address }}</p>
    </v-card>

    <h2 class="text-h5 mb-2">Паспортные данные</h2>
    <v-row>
      <v-col v-for="passport in client.passports" :key="passport.id" cols="12" md="6">
        <v-card variant="outlined">
          <v-card-title>Паспорт РФ</v-card-title>
          <v-card-text>
            Серия/Номер: {{ passport.series }} {{ passport.number }}<br>
            Выдан: {{ passport.date_issue }}<br>
            Кем: {{ passport.issuer }}
          </v-card-text>
        </v-card>
      </v-col>
      <v-col v-if="!client.passports?.length">
        <v-alert type="info" variant="tonal">Нет данных о паспорте</v-alert>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '../../api/axios';

const route = useRoute();
const client = ref(null);

onMounted(async () => {
  // Загружаем клиента. В Lab 3 мы настроили, чтобы он отдавал паспорта внутри поля 'passports'
  const res = await api.get(`/api/v1/clients/${route.params.id}/`);
  client.value = res.data;
});
</script>