<template>
  <v-container v-if="deposit">
    <v-btn to="/deposits" variant="text" prepend-icon="mdi-arrow-left" class="mb-4">Назад</v-btn>

    <v-card class="mb-4 pa-4">
      <h1 class="text-h5">Договор № {{ deposit.contract_number }}</h1>
      <v-chip color="green" class="mt-2">{{ deposit.deposit_sum }} RUB</v-chip>
      <div class="mt-4">
        <p><strong>Дата открытия:</strong> {{ deposit.deposit_date }}</p>
        <p><strong>Дата возврата:</strong> {{ deposit.return_date }}</p>
      </div>
    </v-card>

    <h2 class="text-h6 mb-2">График начислений</h2>
    <v-card>
      <v-data-table
        :headers="accrualHeaders"
        :items="deposit.accruals"
        no-data-text="График пуст"
      ></v-data-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '../../api/axios';

const route = useRoute();
const deposit = ref(null);

const accrualHeaders = [
  { title: '№', key: 'number' },
  { title: 'Дата', key: 'date' },
  { title: 'Сумма начисления', key: 'sum' },
];

onMounted(async () => {
  // Сериализатор из Лабы 3 возвращает accruals внутри объекта deposit
  const res = await api.get(`/api/v1/deposits/${route.params.id}/`);
  deposit.value = res.data;
});
</script>