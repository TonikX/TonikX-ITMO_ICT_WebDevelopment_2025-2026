<template>
  <v-card>
    <v-card-title primary-title>
      <div>
        <div class="headline">{{ client.first_name }} {{ client.last_name }}</div>
      </div>
    </v-card-title>
    <v-card-text v-if="client.room !== null">
      <p>Проживает</p>
    </v-card-text>
    <v-card-text v-else-if="client.room === null">
      <p>Выселен</p>
    </v-card-text>
    <v-card-actions>
      <v-btn v-if="client.room !== null" @click="checkout(client.id)" color="red" small>Выселить</v-btn>
      <v-spacer></v-spacer>
      <v-btn icon @click="show = !show">
        <i class="material-icons">{{ show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</i>
      </v-btn>
    </v-card-actions>
    <v-slide-y-transition>
      <v-card-text v-show="show" v-if="client.room !== null">
        <p>Паспорт: {{ client.passport_number }}</p>
        <p>Город: {{ client.city_of_origin }}</p>
        <p>Дата заезда: {{ client.check_in_date }}</p>
        <p>Дата выезда: {{ client.check_out_date }}</p>
        <p>Номер: {{ client.room }}</p>
      </v-card-text>
      <v-card-text v-else v-show="show">
        <p>Паспорт: {{ client.passport_number }}</p>
        <p>Город: {{ client.city_of_origin }}</p>
        <p>Дата заезда: {{ client.check_in_date }}</p>
        <p>Дата выселения: {{ client.check_out_date }}</p>
        <p>Проживал в номере: {{ client.room_number }}</p>
      </v-card-text>
    </v-slide-y-transition>
  </v-card>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const props = defineProps({
  client: Object,
});

const router = useRouter();

const checkout = async (clientId) => {
  try {
    await axios.post(`/api/clients/${clientId}/checkout/`);
    alert('Клиент выселен');
    router.go();
  } catch (error) {
    console.error('Ошибка при выселении клиента:', error);
    alert('Ошибка при выселении клиента');
  }
};

const show = ref(false);
</script>
