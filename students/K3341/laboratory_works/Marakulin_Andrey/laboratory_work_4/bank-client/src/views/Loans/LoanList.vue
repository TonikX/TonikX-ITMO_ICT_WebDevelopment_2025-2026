<template>
  <v-container>
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="text-h4">Кредиты</h1>
      <v-btn color="primary" to="/credits/create" prepend-icon="mdi-plus">Выдать кредит</v-btn>
    </div>

    <v-card>
      <v-data-table :headers="headers" :items="items" :loading="loading">
        <template v-slot:item.actions="{ item }">
          <v-btn icon="mdi-eye" variant="text" color="blue" :to="`/credits/${item.id}`"></v-btn>
          <v-btn icon="mdi-pencil" variant="text" color="green" :to="`/credits/${item.id}/edit`"></v-btn>
          <v-btn icon="mdi-delete" variant="text" color="red" @click="deleteItem(item.id)"></v-btn>
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
  { title: 'Сумма', key: 'sum_credit' },
  { title: 'Выдан', key: 'date_issue' },
  { title: 'Закрытие', key: 'close_date' },
  { title: 'Действия', key: 'actions', sortable: false, align: 'end' },
];

const fetchData = async () => {
  try {
    const res = await api.get('/api/v1/loans/');
    items.value = res.data;
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};

const deleteItem = async (id) => {
  if (confirm('Удалить кредит?')) {
    await api.delete(`/api/v1/loans/${id}/`);
    items.value = items.value.filter(i => i.id !== id);
  }
};

onMounted(fetchData);
</script>