<template>
  <v-container>
    <v-card class="mx-auto" max-width="900">
      <v-card-title class="text-h5 pa-4" :class="isCreating ? 'success white--text' : 'primary white--text'">
        {{ isCreating ? 'Открытие Нового Вклада' : `Детали Вклада №${depositId}` }}
      </v-card-title>

      <v-card-text>
        <v-alert v-if="error" type="error" dense text class="my-3">{{ error }}</v-alert>
        <v-progress-linear v-if="loading" indeterminate color="primary"></v-progress-linear>

        <v-form v-if="!loading" @submit.prevent="saveDeposit">

          <h3 class="my-4">Основные данные:</h3>
          <v-row>
            <v-col cols="12" md="6">
              <v-select
                v-model="deposit.client"
                :items="clients"
                item-title="fio"
                item-value="id_client"
                label="Клиент (ID)"
                :disabled="!isCreating"
                required
              ></v-select>
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                v-model="deposit.deposit_type"
                :items="depositTypes"
                item-title="name"
                item-value="id_deposit_type"
                label="Тип Вклада"
                required
              ></v-select>
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model="deposit.deposit_amount"
                label="Сумма вклада"
                type="number"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="deposit.deposit_date"
                label="Дата вклада (YYYY-MM-DD)"
                type="date"
                required
              ></v-text-field>
            </v-col>

            <v-col cols="12" md="4">
              <v-select
                v-model="deposit.currency"
                :items="currencies"
                item-title="name"
                item-value="code"
                label="Валюта"
                required
              ></v-select>
            </v-col>

            <v-col cols="12" md="8">
              <v-select
                v-model="deposit.employee_position"
                :items="employeePositions"
                item-title="title"
                item-value="id_employee_position"
                label="Сотрудник (Занимаемая должность)"
                clearable
              ></v-select>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <div v-if="!isCreating && deposit.schedule && deposit.schedule.length">
            <h3 class="my-4 primary--text">График Начислений</h3>
            <v-data-table
                :headers="scheduleHeaders"
                :items="deposit.schedule"
                class="elevation-2"
                density="compact"
            >
                <template v-slot:item.charge_amount="{ item }">
                    {{ item.charge_amount }} {{ deposit.currency.code }}
                </template>
            </v-data-table>
          </div>
          <div v-else-if="!isCreating" class="text-caption grey--text">
            График начислений не сформирован.
          </div>

          <v-card-actions class="pa-0 pt-4">
            <v-btn color="grey" @click="$router.push('/deposits')">Назад к списку</v-btn>
            <v-spacer></v-spacer>
            <v-btn
              type="submit"
              :color="isCreating ? 'success' : 'primary'"
              :loading="isSaving"
            >
              {{ isCreating ? 'Открыть Вклад' : 'Сохранить Изменения' }}
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../api';

const route = useRoute();
const router = useRouter();

const depositId = computed(() => route.params.id);
const isCreating = computed(() => !depositId.value);

// --- Вспомогательные данные для Selects ---
const clients = ref([]);
const depositTypes = ref([]);
const currencies = ref([]);
const employeePositions = ref([]);

// --- Основное состояние ---
const deposit = ref({
  client: null,
  deposit_type: null,
  currency: null,
  employee_position: null,
  deposit_amount: 0,
  deposit_date: new Date().toISOString().substr(0, 10), // Сегодняшняя дата по умолчанию
  // Дополнительные поля, которые приходят с GET-запросом:
  contract_data: '',
  contract_number: '',
  return_date: '',
  return_amount: 0,
  schedule: [],
});

const loading = ref(true);
const isSaving = ref(false);
const error = ref(null);

const scheduleHeaders = [
  { title: '№', value: 'number' },
  { title: 'Дата начисления', value: 'charge_date' },
  { title: 'Сумма', value: 'charge_amount' },
];


// --- 1. Загрузка вспомогательных списков ---
const fetchSelectData = async () => {
    try {
        const [clientsRes, typesRes, currencyRes, positionsRes] = await Promise.all([
            api.get('/api/v1/clients/'),
            api.get('/api/v1/deposittypes/'),
            api.get('/api/v1/currencies/'),
            api.get('/api/v1/employeepositions/'),
        ]);
        clients.value = clientsRes.data;
        depositTypes.value = typesRes.data;
        currencies.value = currencyRes.data;
        employeePositions.value = positionsRes.data;
    } catch (err) {
        error.value = 'Не удалось загрузить вспомогательные данные для формы.';
        console.error("Fetch Select Data Error:", err);
    }
};

// --- 2. Загрузка данных Вклада (для редактирования/просмотра) ---
const fetchDeposit = async () => {
  error.value = null;
  try {
    const response = await api.get(`/api/v1/deposits/${depositId.value}/`);

    // Преобразование полученных данных для формы
    deposit.value = {
        ...response.data,
        // Извлекаем только ID/Code для v-model, так как DRF присылает объекты
        client: response.data.client, // client - это ID
        deposit_type: response.data.deposit_type.id_deposit_type,
        currency: response.data.currency.code,
        employee_position: response.data.employee_position ? response.data.employee_position.id_employee_position : null,
    };

  } catch (err) {
    error.value = 'Ошибка при загрузке данных вклада.';
    console.error(err);
  }
};

// --- 3. Сохранение/Создание Вклада ---
const saveDeposit = async () => {
  isSaving.value = true;
  error.value = null;

  // Создание чистого payload для отправки (только ID внешних ключей)
  const payload = {
    ...deposit.value,
    client: deposit.value.client, // ID клиента
    deposit_type: deposit.value.deposit_type, // ID типа
    currency: deposit.value.currency, // Код валюты
    employee_position: deposit.value.employee_position || null, // ID должности
    // Убираем вложенные объекты, чтобы не мешать DRF
    schedule: undefined,
    client_info: undefined,
  };

  try {
    let response;

    if (isCreating.value) {
      // POST запрос для создания
      response = await api.post('/api/v1/deposits/', payload);
      alert('Вклад успешно открыт!');
      router.push(`/deposits/${response.data.id_deposit}`);

    } else {
      // PUT запрос для редактирования (отправляем только изменяемые поля)
      response = await api.put(`/api/v1/deposits/${depositId.value}/`, payload);
      alert('Данные вклада успешно обновлены!');
      await fetchDeposit(); // Перезагружаем данные
    }
  } catch (err) {
    if (err.response && err.response.data) {
        const errors = Object.values(err.response.data).flat().join('; ');
        error.value = `Ошибка валидации: ${errors}`;
    } else {
        error.value = isCreating.value ? 'Ошибка открытия вклада.' : 'Ошибка сохранения вклада.';
    }
    console.error(err);
  } finally {
    isSaving.value = false;
  }
};

onMounted(async () => {
  await fetchSelectData();
  if (!isCreating.value) {
    await fetchDeposit();
  }
  loading.value = false; // Завершаем загрузку после всех асинхронных операций
});
</script>