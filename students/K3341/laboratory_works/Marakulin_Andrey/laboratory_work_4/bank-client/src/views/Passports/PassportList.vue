<template>
  <v-container>
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="text-h4">Паспорта</h1>
      <v-btn color="primary" to="/passports/create" prepend-icon="mdi-plus">Добавить паспорт</v-btn>
    </div>

    <v-card>
      <v-data-table :headers="headers" :items="items" :loading="loading">
        <template v-slot:item.actions="{ item }">
          <v-btn icon="mdi-eye" variant="text" color="blue" :to="`/passports/${item.id}`" title="Просмотр"></v-btn>
          <v-btn icon="mdi-pencil" variant="text" color="green" :to="`/passports/${item.id}/edit`" title="Редактировать"></v-btn>
          <v-btn icon="mdi-delete" variant="text" color="red" @click="deleteItem(item.id)" title="Удалить"></v-btn>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../../api/axios';

const items = ref([]);
const loading = ref(true);

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Серия', key: 'series' },
  { title: 'Номер', key: 'number' },
  { title: 'ФИО (в паспорте)', key: 'fio' },
  { title: 'Клиент ID', key: 'client' }, // Можно выводить ID, так как бэкенд отдает ID
  { title: 'Действия', key: 'actions', sortable: false, align: 'end' },
];

const fetchData = async () => {
  try {
    const res = await api.get('/api/v1/passports/');
    items.value = res.data;
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};

const deleteItem = async (id) => {
  if (confirm('Удалить паспорт?')) {
    await api.delete(`/api/v1/passports/${id}/`);
    items.value = items.value.filter(i => i.id !== id);
  }
};

onMounted(fetchData);
</script>