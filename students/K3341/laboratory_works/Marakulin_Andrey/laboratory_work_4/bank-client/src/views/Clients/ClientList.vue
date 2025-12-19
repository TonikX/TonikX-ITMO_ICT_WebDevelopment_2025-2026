<template>
  <div>
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="text-h4">Список клиентов</h1>
      <v-btn color="primary" to="/clients/create" prepend-icon="mdi-plus">Добавить</v-btn>
    </div>

    <v-card>
      <v-data-table :headers="headers" :items="clients" :loading="loading">
        <template v-slot:item.actions="{ item }">
          <v-btn icon="mdi-eye" variant="text" color="blue" :to="`/clients/${item.id}`"></v-btn>
          <v-btn icon="mdi-pencil" variant="text" color="green" :to="`/clients/${item.id}/edit`"></v-btn>
          <v-btn icon="mdi-delete" variant="text" color="red" @click="deleteClient(item.id)"></v-btn>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../../api/axios';

const clients = ref([]);
const loading = ref(true);
const headers = [
  { title: 'ID', key: 'id' },
  { title: 'ФИО', key: 'fio' },
  { title: 'Телефон', key: 'phone' },
  { title: 'Email', key: 'email' },
  { title: 'Действия', key: 'actions', sortable: false, align: 'end' },
];

const loadClients = async () => {
  try {
    const res = await api.get('/api/v1/clients/');
    clients.value = res.data;
  } finally {
    loading.value = false;
  }
};

const deleteClient = async (id) => {
  if(confirm('Удалить клиента?')) {
    await api.delete(`/api/v1/clients/${id}/`);
    clients.value = clients.value.filter(c => c.id !== id);
  }
};

onMounted(loadClients);
</script>