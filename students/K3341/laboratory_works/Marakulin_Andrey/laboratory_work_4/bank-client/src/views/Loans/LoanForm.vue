<template>
  <v-container>
    <v-card class="pa-4 mx-auto" max-width="800">
      <v-card-title>{{ isEdit ? 'Редактирование кредита' : 'Выдача кредита' }}</v-card-title>
      <v-form @submit.prevent="submit">
        <v-row>
          <v-col cols="12">
            <v-select
              v-model="form.processed_by"
              :items="positions"
              item-title="desc"
              item-value="id"
              label="Кем оформлен (Сотрудник)"
              required
            ></v-select>
          </v-col>

          <v-col cols="12">
            <v-select
              v-model="form.passport"
              :items="passports"
              item-title="selectTitle"
              item-value="id"
              label="Паспорт клиента"
              required
            ></v-select>
          </v-col>

          <v-col cols="12" md="6">
            <v-select
              v-model="form.loan_type"
              :items="loanTypes"
              item-title="name"
              item-value="id"
              label="Тип кредита"
              required
            ></v-select>
          </v-col>
          <v-col cols="12" md="6">
            <v-select
              v-model="form.currency"
              :items="currencies"
              item-title="code"
              item-value="id"
              label="Валюта"
              required
            ></v-select>
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field v-model="form.contract_number" label="Номер договора" required></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="form.sum_credit" label="Сумма кредита" type="number" required></v-text-field>
          </v-col>

          <v-col cols="12" md="4">
            <v-text-field v-model="form.monthly_payment" label="Ежемес. платеж" type="number" required></v-text-field>
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field v-model="form.payout_count" label="Кол-во выплат" type="number" required></v-text-field>
          </v-col>

          <v-col cols="12" md="4">
             <v-text-field v-model="form.trusted_person" label="Доверенное лицо"></v-text-field>
          </v-col>

          <v-col cols="12" md="4">
            <v-text-field v-model="form.date_issue" label="Дата выдачи" type="date" required></v-text-field>
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field v-model="form.close_date" label="Дата закрытия (план)" type="date" required></v-text-field>
          </v-col>
           <v-col cols="12" md="4">
            <v-text-field v-model="form.fact_close_date" label="Фактич. закрытие" type="date"></v-text-field>
          </v-col>

          <v-col cols="12">
            <v-textarea v-model="form.contract_data" label="Данные договора (текст)" rows="2"></v-textarea>
          </v-col>
          <v-col cols="12">
            <v-textarea v-model="form.loan_data" label="Доп. данные кредита" rows="2"></v-textarea>
          </v-col>
        </v-row>

        <div class="d-flex gap-2 mt-4">
          <v-btn type="submit" color="primary">Сохранить</v-btn>
          <v-btn variant="text" to="/credits">Отмена</v-btn>
        </div>
      </v-form>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../../api/axios';

const route = useRoute();
const router = useRouter();
const isEdit = computed(() => !!route.params.id);

const passports = ref([]);
const loanTypes = ref([]);
const currencies = ref([]);
const positions = ref([]);

const form = reactive({
  passport: null,
  loan_type: null,
  currency: null,
  processed_by: null,
  contract_number: '',
  sum_credit: '',
  monthly_payment: '',
  payout_count: 12,
  trusted_person: '',
  date_issue: '',
  close_date: '',
  fact_close_date: null,
  contract_data: 'Типовой договор...',
  loan_data: ''
});

onMounted(async () => {
  try {
    const [passReq, typeReq, currReq, posReq] = await Promise.all([
      api.get('/api/v1/passports/'),
      api.get('/api/v1/loan-types/'),
      api.get('/api/v1/currencies/'),
      api.get('/api/v1/occupied-positions/')
    ]);

    passports.value = passReq.data.map(p => ({
      ...p,
      selectTitle: `${p.series} ${p.number} (${p.fio})`
    }));
    loanTypes.value = typeReq.data;
    currencies.value = currReq.data;


    positions.value = posReq.data.map(pos => ({
      id: pos.id,
      desc: `Должность #${pos.id} (Сотрудник ${pos.employee})`
    }));

    if (isEdit.value) {
      const res = await api.get(`/api/v1/loans/${route.params.id}/`);
      Object.assign(form, res.data);
    }
  } catch (e) {
    console.error(e);
  }
});

const submit = async () => {
  try {
    if (isEdit.value) {
      await api.patch(`/api/v1/loans/${route.params.id}/`, form);
    } else {
      await api.post('/api/v1/loans/', form);
    }
    router.push('/credits');
  } catch (e) {
    console.error(e);
    if (e.response && e.response.data) {
        alert('Ошибка: ' + JSON.stringify(e.response.data));
    } else {
        alert('Ошибка сохранения кредита');
    }
  }
};
</script>