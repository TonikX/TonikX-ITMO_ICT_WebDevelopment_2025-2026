<template>
  <v-container fluid class="mt-4 px-4 px-md-8">
    <v-row>
      <v-col cols="12">
        <v-card class="glass-card pa-6" elevation="10" rounded="xl">
          <div class="d-flex flex-column flex-sm-row align-start align-sm-center justify-space-between mb-6 gap-4">
            <div class="d-flex align-center">
              <div class="icon-box mr-4">
                <v-icon icon="mdi-ticket" color="white" size="28"></v-icon>
              </div>
              <div>
                <h1 class="text-h5 font-weight-bold text-white mb-1">Создание билета</h1>
                <p class="text-caption text-grey-lighten-1 mb-0">Оформление нового авиабилета</p>
              </div>
            </div>
          </div>

          <v-form @submit.prevent="createTicket" class="ticket-form">
            <v-row>
              <!-- Flight Selection -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="ticketData.flight_id"
                  label="ID рейса"
                  variant="solo-filled"
                  bg-color="rgba(255,255,255,0.05)"
                  prepend-inner-icon="mdi-airplane"
                  hide-details
                  rounded="lg"
                  type="number"
                  required
                ></v-text-field>
              </v-col>

              <!-- Seat Number -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="ticketData.seat_number"
                  label="Номер места"
                  variant="solo-filled"
                  bg-color="rgba(255,255,255,0.05)"
                  prepend-inner-icon="mdi-seat-passenger"
                  hide-details
                  rounded="lg"
                  required
                ></v-text-field>
              </v-col>

              <!-- Sale Channel -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="ticketData.sale_channel"
                  label="Канал продажи"
                  variant="solo-filled"
                  bg-color="rgba(255,255,255,0.05)"
                  prepend-inner-icon="mdi-store"
                  hide-details
                  rounded="lg"
                  required
                ></v-text-field>
              </v-col>

              <!-- Additional Fee -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="ticketData.additional_fee"
                  label="Дополнительная плата"
                  variant="solo-filled"
                  bg-color="rgba(255,255,255,0.05)"
                  prepend-inner-icon="mdi-currency-usd"
                  hide-details
                  rounded="lg"
                  type="number"
                  step="0.01"
                ></v-text-field>
              </v-col>

              <!-- Passenger Information -->
              <v-col cols="12">
                <h3 class="text-h6 font-weight-bold text-white mb-4">Информация о пассажире</h3>
              </v-col>

              <!-- Full Name -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="ticketData.passenger_data.full_name"
                  label="ФИО пассажира"
                  variant="solo-filled"
                  bg-color="rgba(255,255,255,0.05)"
                  prepend-inner-icon="mdi-account"
                  hide-details
                  rounded="lg"
                  required
                ></v-text-field>
              </v-col>

              <!-- Birth Date -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="ticketData.passenger_data.birth_date"
                  label="Дата рождения"
                  variant="solo-filled"
                  bg-color="rgba(255,255,255,0.05)"
                  prepend-inner-icon="mdi-calendar"
                  hide-details
                  rounded="lg"
                  type="date"
                  required
                ></v-text-field>
              </v-col>

              <!-- Passport Serial -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="ticketData.passenger_data.passport_serial"
                  label="Серия паспорта"
                  variant="solo-filled"
                  bg-color="rgba(255,255,255,0.05)"
                  prepend-inner-icon="mdi-card-account-details"
                  hide-details
                  rounded="lg"
                  required
                ></v-text-field>
              </v-col>

              <!-- Passport Number -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="ticketData.passenger_data.passport_number"
                  label="Номер паспорта"
                  variant="solo-filled"
                  bg-color="rgba(255,255,255,0.05)"
                  prepend-inner-icon="mdi-identifier"
                  hide-details
                  rounded="lg"
                  required
                ></v-text-field>
              </v-col>

              <!-- Passport Region -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="ticketData.passenger_data.passport_region"
                  label="Кем выдан"
                  variant="solo-filled"
                  bg-color="rgba(255,255,255,0.05)"
                  prepend-inner-icon="mdi-office-building"
                  hide-details
                  rounded="lg"
                  required
                ></v-text-field>
              </v-col>

              <!-- Phone Number -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="ticketData.passenger_data.phone_number"
                  label="Номер телефона"
                  variant="solo-filled"
                  bg-color="rgba(255,255,255,0.05)"
                  prepend-inner-icon="mdi-phone"
                  hide-details
                  rounded="lg"
                  required
                ></v-text-field>
              </v-col>

              <!-- Email -->
              <v-col cols="12">
                <v-text-field
                  v-model="ticketData.passenger_data.email"
                  label="Email"
                  variant="solo-filled"
                  bg-color="rgba(255,255,255,0.05)"
                  prepend-inner-icon="mdi-email"
                  hide-details
                  rounded="lg"
                  type="email"
                  required
                ></v-text-field>
              </v-col>

              <!-- Submit Button -->
              <v-col cols="12" class="d-flex justify-center mt-4">
                <v-btn
                  type="submit"
                  color="primary"
                  size="x-large"
                  rounded="pill"
                  :loading="loading"
                  :disabled="loading"
                  class="px-8"
                >
                  <v-icon start>mdi-ticket-plus</v-icon>
                  Создать билет
                </v-btn>
              </v-col>
            </v-row>
          </v-form>

          <!-- Success Message -->
          <v-alert
            v-if="successMessage"
            type="success"
            variant="tonal"
            icon="mdi-check-circle"
            class="glass-alert mt-6"
            border="start"
          >
            {{ successMessage }}
          </v-alert>

          <!-- Error Message -->
          <v-alert
            v-if="errorMessage"
            type="error"
            variant="tonal"
            icon="mdi-alert-circle"
            class="glass-alert mt-6"
            border="start"
          >
            {{ errorMessage }}
          </v-alert>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '../api';

const loading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');
const route = useRoute();

const ticketData = ref({
  flight_id: '',
  seat_number: '',
  sale_channel: '',
  additional_fee: 0,
  passenger_data: {
    full_name: '',
    birth_date: '',
    passport_serial: '',
    passport_number: '',
    passport_region: '',
    phone_number: '',
    email: ''
  }
});

onMounted(() => {
  // Pre-fill form with query parameters if available
  if (route.query.flightId) {
    ticketData.value.flight_id = route.query.flightId;
  }
  if (route.query.seatNumber) {
    ticketData.value.seat_number = route.query.seatNumber;
  }
});

const createTicket = async () => {
  loading.value = true;
  successMessage.value = '';
  errorMessage.value = '';
  
  try {
    const response = await api.post('/air/tickets/create/', ticketData.value);
    successMessage.value = `Билет успешно создан! ID: ${response.data.id}`;
    
    // Reset form
    ticketData.value = {
      flight_id: '',
      seat_number: '',
      sale_channel: '',
      additional_fee: 0,
      passenger_data: {
        full_name: '',
        birth_date: '',
        passport_serial: '',
        passport_number: '',
        passport_region: '',
        phone_number: '',
        email: ''
      }
    };
  } catch (error) {
    errorMessage.value = error.response?.data?.error || 'Ошибка при создании билета';
    console.error(error);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.glass-card {
  background: rgba(30, 41, 59, 0.7) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.icon-box {
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.glass-alert {
  border-color: rgba(255, 255, 255, 0.2) !important;
}

.gap-4 {
  gap: 1rem;
}

.ticket-form {
  margin-top: 20px;
}
</style>