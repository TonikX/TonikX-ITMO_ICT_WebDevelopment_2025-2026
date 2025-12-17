<template>
  <v-container>
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="text-h4">Вклады</h1>
      <v-btn color="primary" to="/deposits/create" prepend-icon="mdi-plus">Оформить вклад</v-btn>
    </div>

    <v-card>
      <v-data-table :headers="headers" :items="items" :loading="loading">
        <template v-slot:item.actions="{ item }">
          <v-btn icon="mdi-eye" variant="text" color="blue" :to="`/deposits/${item.id}`"></v-btn>
          <v-btn icon="mdi-pencil" variant="text" color="green" :to="`/deposits/${item.id}/edit`"></v-btn>
          <v-btn icon="mdi-delete" variant="text" color="red" @click="deleteItem(item.id)"></v-btn>
        </template>

        <template v-slot:item.deposit_date="{ item }">
          {{ new Date(item.deposit_date).toLocaleDateString() }}
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
  { title: 'Номер договора', key: 'contract_number' },
  { title: 'Сумма', key: 'deposit_sum' },
  { title: 'Дата открытия', key: 'deposit_date' },
  { title: 'Дата возврата', key: 'return_date' },
  { title: 'Действия', key: 'actions', sortable: false, align: 'end' },
];

const fetchData = async () => {
  try {
    const res = await api.get('/api/v1/deposits/');
    items.value = res.data;
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};

const deleteItem = async (id) => {
  if (confirm('Удалить вклад?')) {
    await api.delete(`/api/v1/deposits/${id}/`);
    items.value = items.value.filter(i => i.id !== id);
  }
};

onMounted(fetchData);
</script>