<template>
  <v-container>
    <v-container>
      <h1>Гости</h1>
      <v-btn v-if="!addingClient" @click="addingClient = true" color="primary">
        Заселить клиента
      </v-btn>
    </v-container>

    <v-container>
      <v-form @submit.prevent="addClient" v-if="addingClient">
        <v-text-field
          v-model="newClient.passport_number"
          label="Паспорт"
          required
          mask="## ## ######"
          hint="Пример: 1234 5678 9012"
          persistent-hint
        ></v-text-field>
        <v-text-field v-model="newClient.first_name" label="Имя" required></v-text-field>
        <v-text-field v-model="newClient.last_name" label="Фамилия" required></v-text-field>
        <v-text-field v-model="newClient.middle_name" label="Отчество" required></v-text-field>
        <v-text-field v-model="newClient.city_of_origin" label="Город" required></v-text-field>

        <v-text-field
          v-model="newClient.check_in_date"
          label="Дата заезда"
          type="date"
        ></v-text-field>

        <v-text-field
          v-model="newClient.check_out_date"
          label="Дата выезда"
          type="date"
        ></v-text-field>

        <v-select
          v-model="newClient.room"
          :items="availableRooms"
          item-value="id"
          item-title="number"
          label="Выберите свободную комнату"
          required
          :disabled="availableRooms.length === 0"
        ></v-select>

        <v-btn color="primary" type="submit">Добавить</v-btn>
        <v-btn @click="addingClient = false" color="secondary">Отмена</v-btn>
      </v-form>
    </v-container>

    <v-row>
      <v-col v-for="client in clients" :key="client.id" cols="12" md="4">
        <ClientCard :client="client" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import ClientCard from '@/components/ClientCard.vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const clients = ref([]);
const addingClient = ref(false);

const newClient = ref({
  passport_number: '',
  first_name: '',
  last_name: '',
  middle_name: '',
  city_of_origin: '',
  check_in_date: null,
  check_out_date: null,
  room: null,
});

const availableRooms = ref([]);

const fetchClients = async () => {
  try {
    const response = await axios.get('/api/clients/');
    clients.value = response.data;
  } catch (error) {
    console.error('Ошибка при получении списка клиентов', error);
  }
};

const addClient = async () => {
  try {
    await axios.post('/api/clients/', {
      passport_number: newClient.value.passport_number,
      first_name: newClient.value.first_name,
      last_name: newClient.value.last_name,
      middle_name: newClient.value.middle_name,
      city_of_origin: newClient.value.city_of_origin,
      check_in_date: newClient.value.check_in_date,
      check_out_date: newClient.value.check_out_date,
      room: newClient.value.room,
    });
    alert('Клиент добавлен');
    newClient.value = {
      passport_number: '',
      first_name: '',
      last_name: '',
      middle_name: '',
      city_of_origin: '',
      check_in_date: null,
      check_out_date: null,
      room: null,
    };
    fetchClients();
    availableRooms.value = [];
    router.go();
  } catch (error) {
    console.error('Ошибка при добавлении клиента', error);
    alert('Ошибка при добавлении клиента');
  }
};

const fetchAvailableRooms = async () => {
  const start = newClient.value.check_in_date;
  const end = newClient.value.check_out_date;

  if (!start || !end) return;

  try {
    const response = await axios.get('/api/rooms/free_rooms/', {
      params: { start, end },
    });
    availableRooms.value = response.data;
  } catch (error) {
    console.error('Ошибка при получении данных о комнатах:', error);
    availableRooms.value = [];
  }
};

watch(
  () => [newClient.value.check_in_date, newClient.value.check_out_date],
  ([start, end]) => {
    if (start && end) fetchAvailableRooms();
  }
);

onMounted(() => {
  fetchClients();
});
</script>