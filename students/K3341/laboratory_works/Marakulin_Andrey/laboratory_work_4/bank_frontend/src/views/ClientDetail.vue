<template>
  <v-container>
    <v-card class="mx-auto" max-width="800">
      <v-card-title class="text-h5 pa-4" :class="isCreating ? 'success white--text' : 'primary white--text'">
        {{ isCreating ? 'Создание Нового Клиента' : 'Детали/Редактирование Клиента' }}
      </v-card-title>

      <v-card-text>
        <v-alert v-if="error" type="error" dense text class="my-3">{{ error }}</v-alert>
        <v-progress-linear v-if="loading" indeterminate color="primary"></v-progress-linear>

        <v-form v-if="!loading" @submit.prevent="saveClient">
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field v-model="client.fio" label="ФИО" required></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="client.phone" label="Телефон" required></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="client.email" label="Email" type="email" required></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="client.address" label="Адрес" required></v-text-field>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <div v-if="!isCreating && client.passports && client.passports.length">
            <h3 class="mb-3">Паспортные данные:</h3>
            <div v-for="passport in client.passports" :key="passport.id_passport">
              <v-card outlined class="mb-3 pa-3">
                <p><strong>Серия/Номер:</strong> {{ passport.series }} {{ passport.number }}</p>
                <p><strong>ФИО в паспорте:</strong> {{ passport.fio_on_passport }}</p>
                <p><strong>Кем выдан:</strong> {{ passport.issued_by }}</p>
                <p><strong>Дата выдачи:</strong> {{ passport.issue_date }}</p>
              </v-card>
            </div>
          </div>
          <div v-else-if="!isCreating" class="text-caption grey--text mb-4">
            Паспортные данные отсутствуют.
          </div>

          <v-divider class="my-4"></v-divider>

          <div v-if="!isCreating && client.deposits && client.deposits.length">
            <h3 class="mb-3 primary--text">Вклады клиента:</h3>
            <v-list dense class="elevation-1">
              <v-list-item v-for="deposit in client.deposits" :key="deposit.id_deposit">
                <v-list-item-content>
                  <v-list-item-title>
                    Вклад №{{ deposit.id_deposit }} (Тип: {{ deposit.deposit_type }})
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    Сумма: {{ deposit.deposit_amount }} / Дата открытия: {{ deposit.deposit_date }}
                  </v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-action>
                  <v-btn icon small @click="$router.push(`/deposits/${deposit.id_deposit}`)">
                    <v-icon>mdi-eye</v-icon>
                  </v-btn>
                </v-list-item-action>
              </v-list-item>
            </v-list>
          </div>
          <div v-else-if="!isCreating" class="text-caption grey--text">
            Нет активных вкладов.
          </div>

          <v-divider class="my-4"></v-divider>

          <div v-if="!isCreating && client.credits && client.credits.length">
            <h3 class="mb-3 primary--text">Кредиты клиента:</h3>
            <v-list dense class="elevation-1">
              <v-list-item v-for="credit in client.credits" :key="credit.id_credit">
                <v-list-item-content>
                  <v-list-item-title>
                    Кредит №{{ credit.id_credit }} (Тип: {{ credit.credit_type }})
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    Сумма: {{ credit.credit_amount }} / Дата выдачи: {{ credit.credit_date }}
                  </v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-action>
                  <v-btn icon small @click="$router.push(`/credits/${credit.id_credit}`)">
                    <v-icon>mdi-eye</v-icon>
                  </v-btn>
                </v-list-item-action>
              </v-list-item>
            </v-list>
          </div>
          <div v-else-if="!isCreating" class="text-caption grey--text">
            Нет активных кредитов.
          </div>


          <v-card-actions class="pa-0 pt-4">
            <v-btn color="grey" @click="$router.push('/clients')">Назад к списку</v-btn>
            <v-spacer></v-spacer>
            <v-btn
              type="submit"
              :color="isCreating ? 'success' : 'primary'"
              :loading="isSaving"
            >
              {{ isCreating ? 'Создать Клиента' : 'Сохранить Изменения' }}
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

const clientId = computed(() => route.params.id);
const isCreating = computed(() => !clientId.value);

const client = ref({
  fio: '',
  address: '',
  phone: '',
  email: '',
  passports: [],
  deposits: [], // Добавлено для инициализации
  credits: [],  // Добавлено для инициализации
});

const loading = ref(!isCreating.value);
const isSaving = ref(false);
const error = ref(null);

// --- Функции Загрузки Данных ---
const fetchClient = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await api.get(`/api/v1/clients/${clientId.value}/`);
    client.value = response.data;
  } catch (err) {
    error.value = 'Ошибка при загрузке данных клиента.';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

// --- Функции Сохранения/Создания (Оставлены без изменений) ---
const saveClient = async () => {
  isSaving.value = true;
  error.value = null;

  try {
    let response;

    if (isCreating.value) {
      // POST запрос для создания
      response = await api.post('/api/v1/clients/', client.value);
      alert('Клиент успешно создан!');
      router.push(`/clients/${response.data.id_client}`);

    } else {
      // PUT запрос для редактирования
      response = await api.put(`/api/v1/clients/${clientId.value}/`, {
          fio: client.value.fio,
          address: client.value.address,
          phone: client.value.phone,
          email: client.value.email,
          // Отправляем только основные поля
      });
      alert('Данные клиента успешно обновлены!');
      await fetchClient();
    }
  } catch (err) {
    if (err.response && err.response.data) {
        const errors = Object.values(err.response.data).flat().join('; ');
        error.value = `Ошибка валидации: ${errors}`;
    } else {
        error.value = isCreating.value ? 'Ошибка создания клиента.' : 'Ошибка сохранения клиента.';
    }
    console.error(err);
  } finally {
    isSaving.value = false;
  }
};

onMounted(() => {
  if (!isCreating.value) {
    fetchClient();
  }
});
</script>