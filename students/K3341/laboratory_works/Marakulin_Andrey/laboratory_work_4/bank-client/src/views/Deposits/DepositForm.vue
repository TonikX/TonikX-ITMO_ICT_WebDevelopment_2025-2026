<template>
  <v-container>
    <v-card class="pa-4 mx-auto" max-width="800">
      <v-card-title>{{ isEdit ? 'Редактирование вклада' : 'Оформление вклада' }}</v-card-title>
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
              label="Выберите паспорт клиента"
              required
            ></v-select>
          </v-col>

          <v-col cols="12" md="6">
            <v-select
              v-model="form.deposit_type"
              :items="depositTypes"
              item-title="name"
              item-value="id"
              label="Тип вклада"
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
            <v-text-field v-model="form.deposit_sum" label="Сумма вклада" type="number" required></v-text-field>
          </v-col>

          <v-col cols="12" md="6">
             <v-text-field v-model="form.return_sum" label="Сумма к возврату (план)" type="number"></v-text-field>
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field v-model="form.deposit_date" label="Дата открытия" type="date" required></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="form.return_date" label="Дата возврата" type="date" required></v-text-field>
          </v-col>

          <v-col cols="12">
            <v-textarea v-model="form.contract_data" label="Данные договора (текст)" rows="2"></v-textarea>
          </v-col>
          <v-col cols="12">
            <v-textarea v-model="form.deposit_data" label="Доп. данные вклада" rows="2"></v-textarea>
          </v-col>
        </v-row>

        <div class="d-flex gap-2 mt-4">
          <v-btn type="submit" color="primary">Сохранить</v-btn>
          <v-btn variant="text" to="/deposits">Отмена</v-btn>
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
const depositTypes = ref([]);
const currencies = ref([]);
const positions = ref([]);

const form = reactive({
  passport: null,
  deposit_type: null,
  currency: null,
  processed_by: null,
  contract_number: '',
  deposit_sum: '',
  return_sum: '',
  deposit_date: '',
  return_date: '',
  contract_data: 'Типовой договор...',
  deposit_data: ''
});

onMounted(async () => {
  try {
    const [passReq, typeReq, currReq, posReq] = await Promise.all([
      api.get('/api/v1/passports/'),
      api.get('/api/v1/deposit-types/'),
      api.get('/api/v1/currencies/'),
      api.get('/api/v1/occupied-positions/')
    ]);

    passports.value = passReq.data.map(p => ({
      ...p,
      selectTitle: `${p.series} ${p.number} (${p.fio})`
    }));
    depositTypes.value = typeReq.data;
    currencies.value = currReq.data;


    positions.value = posReq.data.map(pos => ({
      id: pos.id,
      desc: `Должность #${pos.id} (Сотрудник ${pos.employee})`
    }));

    if (isEdit.value) {
      const res = await api.get(`/api/v1/deposits/${route.params.id}/`);
      Object.assign(form, res.data);
    }
  } catch (e) {
    console.error(e);
  }
});

const submit = async () => {
  try {
    if (isEdit.value) {
      await api.patch(`/api/v1/deposits/${route.params.id}/`, form);
    } else {
      await api.post('/api/v1/deposits/', form);
    }
    router.push('/deposits');
  } catch (e) {
    console.error(e);
    if (e.response && e.response.data) {
        alert('Ошибка: ' + JSON.stringify(e.response.data));
    } else {
        alert('Ошибка сохранения');
    }
  }
};
</script>