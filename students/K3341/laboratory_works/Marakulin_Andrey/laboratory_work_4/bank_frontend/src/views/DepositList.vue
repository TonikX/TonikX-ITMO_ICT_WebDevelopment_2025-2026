<template>
  <v-container>
    <v-card>
      <v-card-title class="text-h5 primary white--text pa-4 d-flex justify-space-between align-center">
        Список Вкладов
        <v-btn color="white" dark @click="$router.push('/deposits/create')">
          <v-icon left>mdi-plus</v-icon>
          Открыть Вклад
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-alert v-if="error" type="error" dense text class="my-3">{{ error }}</v-alert>

        <v-data-table
          :headers="headers"
          :items="deposits"
          :loading="loading"
          loading-text="Загрузка данных..."
          class="elevation-1"
        >
          <template v-slot:item.deposit_amount="{ item }">
            {{ item.deposit_amount }} {{ item.currency.code }}
          </template>

          <template v-slot:item.client_fio="{ item }">
             {{ item.client_info ? item.client_info.fio : 'Неизвестен' }}
          </template>

          <template v-slot:item.actions="{ item }">
            <v-icon
              small
              class="mr-2"
              @click="viewDeposit(item.id_deposit)"
            >
              mdi-eye
            </v-icon>
            <v-icon
              small
              color="error"
              @click="deleteDeposit(item.id_deposit)"
            >
              mdi-delete
            </v-icon>
          </template>

          <template v-slot:no-data>
            Нет открытых вкладов.
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

const router = useRouter();
const deposits = ref([]);
const loading = ref(true);
const error = ref(null);

const headers = [
  { title: 'ID Вклада', value: 'id_deposit' },
  { title: 'Клиент', value: 'client_fio' },
  { title: 'Тип Вклада', value: 'deposit_type.name' },
  { title: 'Сумма', value: 'deposit_amount' },
  { title: 'Дата Открытия', value: 'deposit_date' },
  { title: 'Действия', value: 'actions', sortable: false },
];

const fetchDeposits = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await api.get('/api/v1/deposits/');
    deposits.value = response.data;
  } catch (err) {
    if (err.response && err.response.status === 401) {
        error.value = 'Сессия истекла. Войдите снова.';
        router.push('/login');
    } else {
        error.value = 'Ошибка при загрузке списка вкладов.';
    }
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const viewDeposit = (id) => {
  router.push(`/deposits/${id}`);
};

const deleteDeposit = async (id) => {
  if (confirm('Вы уверены, что хотите закрыть и удалить этот вклад?')) {
    try {
      await api.delete(`/api/v1/deposits/${id}/`);
      deposits.value = deposits.value.filter(deposit => deposit.id_deposit !== id);
      alert('Вклад успешно удален!');
    } catch (err) {
      error.value = 'Не удалось удалить вклад.';
      console.error(err);
    }
  }
};

onMounted(() => {
  fetchDeposits();
});
</script>@