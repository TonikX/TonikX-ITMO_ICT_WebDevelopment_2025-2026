<template>
  <v-container>
    <v-card>
      <v-card-title class="text-h5 primary white--text pa-4 d-flex justify-space-between align-center">
        Список Клиентов
        <v-btn color="white" dark @click="$router.push('/clients/create')">
          <v-icon left>mdi-plus</v-icon>
          Добавить Клиента
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-alert v-if="error" type="error" dense text class="my-3">{{ error }}</v-alert>

        <v-data-table
          :headers="headers"
          :items="clients"
          :loading="loading"
          loading-text="Загрузка данных..."
          class="elevation-1"
        >
          <template v-slot:item.actions="{ item }">
            <v-icon
              small
              class="mr-2"
              @click="editClient(item.id_client)"
            >
              mdi-pencil
            </v-icon>
            <v-icon
              small
              color="error"
              @click="deleteClient(item.id_client)"
            >
              mdi-delete
            </v-icon>
          </template>

          <template v-slot:no-data>
            Нет данных о клиентах.
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
const clients = ref([]);
const loading = ref(true);
const error = ref(null);

const headers = [
  { title: 'ID', value: 'id_client' },
  { title: 'ФИО', value: 'fio' },
  { title: 'Телефон', value: 'phone' },
  { title: 'Email', value: 'email' },
  { title: 'Действия', value: 'actions', sortable: false },
];

const fetchClients = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await api.get('/api/v1/clients/');
    clients.value = response.data;
  } catch (err) {
    if (err.response && err.response.status === 401) {
        error.value = 'Сессия истекла или требуется авторизация. Пожалуйста, войдите снова.';
        router.push('/login');
    } else {
        error.value = 'Ошибка при загрузке списка клиентов.';
    }
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const editClient = (id) => {
  router.push(`/clients/${id}`);
};

const deleteClient = async (id) => {
  if (confirm('Вы уверены, что хотите удалить этого клиента?')) {
    try {
      await api.delete(`/api/v1/clients/${id}/`);
      // Удаление из локального списка после успешного удаления на сервере
      clients.value = clients.value.filter(client => client.id_client !== id);
      alert('Клиент успешно удален!');
    } catch (err) {
      error.value = 'Не удалось удалить клиента.';
      console.error(err);
    }
  }
};

onMounted(() => {
  fetchClients();
});
</script>