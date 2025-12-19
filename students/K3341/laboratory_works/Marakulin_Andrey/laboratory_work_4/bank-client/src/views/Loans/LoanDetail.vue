<template>
  <v-container v-if="loan">
    <v-btn to="/credits" variant="text" prepend-icon="mdi-arrow-left" class="mb-4">Назад</v-btn>

    <v-card class="mb-4 pa-4">
      <h1 class="text-h5">Кредитный договор № {{ loan.contract_number }}</h1>
      <v-chip color="red" class="mt-2">{{ loan.sum_credit }} RUB</v-chip>
      <div class="mt-4">
        <p><strong>Дата выдачи:</strong> {{ loan.date_issue }}</p>
        <p><strong>Ежемесячный платеж:</strong> {{ loan.monthly_payment }}</p>
      </div>
    </v-card>

    <h2 class="text-h6 mb-2">График платежей</h2>
    <v-card>
      <v-data-table
        :headers="payoutHeaders"
        :items="loan.payouts"
        no-data-text="График не сформирован"
      ></v-data-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '../../api/axios';

const route = useRoute();
const loan = ref(null);

const payoutHeaders = [
  { title: 'Дата выплаты', key: 'date_payout' },
  { title: 'Сумма платежа', key: 'sum_payout' },
  { title: 'Проценты', key: 'sum_interest' },
  { title: 'Остаток долга', key: 'remainder' },
];

onMounted(async () => {
  // Сериализатор из Лабы 3 возвращает график в поле 'payouts'
  const res = await api.get(`/api/v1/loans/${route.params.id}/`);
  loan.value = res.data;
});
</script>