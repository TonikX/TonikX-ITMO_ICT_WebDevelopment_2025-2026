<template>
  <v-container v-if="passport">
    <v-btn to="/passports" variant="text" prepend-icon="mdi-arrow-left" class="mb-4">Назад</v-btn>

    <v-card class="mx-auto" max-width="600">
      <v-toolbar color="primary" title="Паспорт гражданина РФ"></v-toolbar>
      <v-card-text class="text-body-1">
        <v-row class="mt-2">
          <v-col cols="4" class="font-weight-bold">Владелец (ID):</v-col>
          <v-col cols="8">
            <router-link :to="`/clients/${passport.client}`" class="text-decoration-none">
              Открыть профиль клиента #{{ passport.client }}
            </router-link>
          </v-col>

          <v-col cols="4" class="font-weight-bold">Серия и Номер:</v-col>
          <v-col cols="8" class="text-h6 text-primary">{{ passport.series }} {{ passport.number }}</v-col>

          <v-col cols="4" class="font-weight-bold">ФИО:</v-col>
          <v-col cols="8">{{ passport.fio }}</v-col>

          <v-col cols="4" class="font-weight-bold">Дата выдачи:</v-col>
          <v-col cols="8">{{ new Date(passport.date_issue).toLocaleDateString() }}</v-col>

          <v-col cols="4" class="font-weight-bold">Кем выдан:</v-col>
          <v-col cols="8">{{ passport.issuer }}</v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" :to="`/passports/${passport.id}/edit`">Редактировать</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '../../api/axios';

const route = useRoute();
const passport = ref(null);

onMounted(async () => {
  try {
    const res = await api.get(`/api/v1/passports/${route.params.id}/`);
    passport.value = res.data;
  } catch (e) {
    console.error(e);
  }
});
</script>