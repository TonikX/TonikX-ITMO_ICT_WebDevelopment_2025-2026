<template>
  <div class="payments-container">
    <v-card class="payments-card" elevation="2">
      <v-card-title class="card-header">
        <span class="title-text">Платежи</span>
        <v-spacer />
        <v-btn
          color="primary"
          @click="refreshData"
          class="refresh-btn"
          small
        >
          <v-icon left>mdi-refresh</v-icon>
          Обновить
        </v-btn>
      </v-card-title>

      <v-card-text>
        <!-- Форма создания платежа -->
        <div class="payment-form-section">
          <h3 class="section-title">
            <v-icon color="primary" class="mr-2">mdi-cash-plus</v-icon>
            Новый платеж
          </h3>

          <v-form @submit.prevent="createPayment" class="payment-form">
            <v-row>
              <v-col cols="12" md="6">
                <div class="custom-select-wrapper">
                  <label class="select-label">
                    <v-icon small class="mr-2">mdi-calendar-text</v-icon>
                    Выберите визит *
                  </label>
                  <select
                    v-model="newPayment.visit_id"
                    @change="updateAmount"
                    required
                    class="custom-select"
                    :disabled="loading"
                  >
                    <option disabled :value="null">Выберите визит</option>
                    <option
                      v-for="visit in visits"
                      :key="visit.id"
                      :value="visit.id"
                      :disabled="visit.is_paid"
                    >
                      {{ visit.record.patient.last_name }}
                      {{ visit.record.patient.first_name }}
                      — {{ formatDate(visit.visit_datetime) }}
                      — {{ visit.price }} ₽
                      {{ visit.is_paid ? '(Оплачено)' : '(Не оплачено)' }}
                    </option>
                  </select>
                  <v-icon class="dropdown-icon">mdi-chevron-down</v-icon>
                </div>
              </v-col>

              <v-col cols="12" md="6">
                <div class="custom-select-wrapper">
                  <label class="select-label">
                    <v-icon small class="mr-2">mdi-credit-card-outline</v-icon>
                    Способ оплаты *
                  </label>
                  <select
                    v-model="newPayment.payment_method"
                    required
                    class="custom-select"
                    :disabled="!newPayment.visit_id || isVisitPaid || loading"
                  >
                    <option disabled :value="null">Выберите способ оплаты</option>
                    <option value="cash">Наличные</option>
                    <option value="card">Карта</option>
                  </select>
                  <v-icon class="dropdown-icon">mdi-chevron-down</v-icon>
                </div>
              </v-col>
            </v-row>

            <!-- Информация о выбранном визите -->
            <v-card v-if="newPayment.visit_id" class="selected-visit-info mt-4" elevation="1">
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="6">
                    <div class="info-item">
                      <v-icon small color="primary" class="mr-2">mdi-account</v-icon>
                      <span class="label">Пациент:</span>
                      <strong>{{ selectedVisit?.record?.patient?.last_name }} {{ selectedVisit?.record?.patient?.first_name }}</strong>
                    </div>
                    <div class="info-item">
                      <v-icon small color="primary" class="mr-2">mdi-calendar-clock</v-icon>
                      <span class="label">Дата визита:</span>
                      {{ formatDate(selectedVisit?.visit_datetime) }}
                    </div>
                  </v-col>
                  <v-col cols="12" md="6">
                    <div class="info-item">
                      <v-icon small color="primary" class="mr-2">mdi-cash</v-icon>
                      <span class="label">Стоимость:</span>
                      <strong class="price">{{ selectedVisitPrice }} ₽</strong>
                    </div>
                    <div class="info-item">
                      <v-icon small color="primary" class="mr-2">mdi-check-circle</v-icon>
                      <span class="label">Статус:</span>
                      <span :class="['status-text', isVisitPaid ? 'paid' : 'unpaid']">
                        {{ isVisitPaid ? 'Оплачено' : 'Не оплачено' }}
                      </span>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>

            <v-alert
              v-if="isVisitPaid && newPayment.visit_id"
              type="error"
              dense
              class="mt-4"
            >
              <v-icon small left>mdi-alert-circle</v-icon>
              Этот визит уже оплачен!
            </v-alert>

            <v-btn
              color="primary"
              large
              @click="createPayment"
              :disabled="!isFormValid || isVisitPaid || loading"
              :loading="processing"
              class="submit-btn mt-4"
              block
            >
              <v-icon left>mdi-cash-check</v-icon>
              {{ isVisitPaid ? 'Визит уже оплачен' : 'Оплатить' }}
            </v-btn>
          </v-form>
        </div>

        <v-divider class="my-6"/>

        <!-- История платежей -->
        <div class="payments-history-section">
          <h3 class="section-title">
            <v-icon color="primary" class="mr-2">mdi-history</v-icon>
            История платежей
          </h3>

          <div class="payments-list" v-if="payments.length">
            <v-card
              v-for="payment in payments"
              :key="payment.id"
              class="payment-item mb-3"
              elevation="1"
            >
              <v-card-text>
                <v-row align="center">
                  <v-col cols="2" class="text-center">
                    <div class="payment-id">#{{ payment.id }}</div>
                  </v-col>
                  <v-col cols="4">
                    <div class="patient-info">
                      <v-icon small color="primary" class="mr-2">mdi-account</v-icon>
                      {{ payment.visit.record.patient.last_name }}
                      {{ payment.visit.record.patient.first_name }}
                    </div>
                    <div class="visit-date">
                      <v-icon small color="grey" class="mr-2">mdi-calendar</v-icon>
                      {{ formatDate(payment.visit.visit_datetime) }}
                    </div>
                  </v-col>
                  <v-col cols="2" class="text-right">
                    <div class="amount">{{ payment.amount }} ₽</div>
                  </v-col>
                  <v-col cols="2">
                    <v-chip small :color="getMethodColor(payment.payment_method)" dark>
                      <v-icon small left>{{ getMethodIcon(payment.payment_method) }}</v-icon>
                      {{ payment.payment_method === 'cash' ? 'Наличные' : 'Карта' }}
                    </v-chip>
                  </v-col>
                  <v-col cols="2">
                    <div class="payment-date">
                      <v-icon small color="grey" class="mr-2">mdi-clock-outline</v-icon>
                      {{ formatDate(payment.created_at) }}
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </div>

          <div v-else class="text-center py-6 empty-state">
            <v-icon size="64" color="grey lighten-1">mdi-cash-remove</v-icon>
            <div class="text-h6 grey--text mt-4">Нет данных о платежах</div>
            <div class="text-body-1 grey--text mt-2">Оплатите первый визит, чтобы увидеть историю</div>
          </div>

          <!-- Статистика -->
          <div class="payment-stats mt-6">
            <v-card elevation="1">
              <v-card-text class="stats-content">
                <v-row>
                  <v-col cols="12" sm="6" md="3">
                    <div class="stat-item">
                      <div class="stat-label">Всего платежей</div>
                      <div class="stat-value">{{ payments.length }}</div>
                    </div>
                  </v-col>
                  <v-col cols="12" sm="6" md="3">
                    <div class="stat-item">
                      <div class="stat-label">Общая сумма</div>
                      <div class="stat-value total-amount">{{ totalAmount }} ₽</div>
                    </div>
                  </v-col>
                  <v-col cols="12" sm="6" md="3">
                    <div class="stat-item">
                      <div class="stat-label">Наличными</div>
                      <div class="stat-value cash-amount">{{ cashAmount }} ₽</div>
                    </div>
                  </v-col>
                  <v-col cols="12" sm="6" md="3">
                    <div class="stat-item">
                      <div class="stat-label">Картой</div>
                      <div class="stat-value card-amount">{{ cardAmount }} ₽</div>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </div>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import api from "../api/axios";

export default {
  data() {
    return {
      visits: [],
      payments: [],
      loading: false,
      processing: false,
      newPayment: {
        visit_id: null,
        amount: "",
        payment_method: null,
      },
    };
  },
  computed: {
    selectedVisit() {
      if (!this.newPayment.visit_id) return null;
      return this.visits.find(v => v.id === this.newPayment.visit_id);
    },
    selectedVisitPrice() {
      if (!this.newPayment.visit_id) return 0;
      const visit = this.visits.find(v => v.id === this.newPayment.visit_id);
      return visit ? visit.price : 0;
    },
    isVisitPaid() {
      if (!this.newPayment.visit_id) return false;
      const visit = this.visits.find(v => v.id === this.newPayment.visit_id);
      return visit ? visit.is_paid : false;
    },
    isFormValid() {
      return this.newPayment.visit_id && this.newPayment.payment_method;
    },
    totalAmount() {
      return this.payments.reduce((sum, p) => sum + parseFloat(p.amount || 0), 0).toFixed(2);
    },
    cashAmount() {
      return this.payments
        .filter(p => p.payment_method === 'cash')
        .reduce((sum, p) => sum + parseFloat(p.amount || 0), 0)
        .toFixed(2);
    },
    cardAmount() {
      return this.payments
        .filter(p => p.payment_method === 'card')
        .reduce((sum, p) => sum + parseFloat(p.amount || 0), 0)
        .toFixed(2);
    }
  },
  async mounted() {
    await this.loadAllData();
  },
  methods: {
    async loadAllData() {
      this.loading = true;
      try {
        await Promise.all([
          this.loadVisits(),
          this.loadPayments()
        ]);
      } catch (error) {
        console.error('Ошибка загрузки данных:', error);
        alert('Ошибка загрузки данных');
      } finally {
        this.loading = false;
      }
    },

    async loadVisits() {
      const response = await api.get("/api/visits/");
      this.visits = response.data;
    },

    async loadPayments() {
      const response = await api.get("/api/payments/");
      this.payments = response.data;
    },

    async refreshData() {
      await this.loadAllData();
    },

    updateAmount() {
      this.newPayment.amount = this.selectedVisitPrice;
    },

    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    getMethodColor(method) {
      return method === 'cash' ? 'green' : 'blue';
    },

    getMethodIcon(method) {
      return method === 'cash' ? 'mdi-cash' : 'mdi-credit-card';
    },

    async createPayment() {
      if (this.isVisitPaid) {
        alert('Этот визит уже оплачен!');
        return;
      }

      this.processing = true;

      try {
        await api.post("/api/payments/", this.newPayment);
        await this.loadPayments();
        await this.loadVisits();

        this.newPayment = {
          visit_id: null,
          amount: "",
          payment_method: null,
        };

        alert('Платеж успешно создан!');
      } catch (error) {
        console.error('Ошибка при создании платежа:', error);
        alert('Ошибка при создании платежа: ' + (error.response?.data?.message || error.message));
      } finally {
        this.processing = false;
      }
    },
  },
};
</script>

<style scoped>
.payments-container {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.payments-card {
  border-radius: 12px;
  overflow: hidden;
}

.card-header {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 24px !important;
  border-bottom: 1px solid #e0e0e0;
}

.title-text {
  font-size: 28px;
  font-weight: 600;
  color: #2c3e50;
}

.refresh-btn {
  border-radius: 6px;
  text-transform: none;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
}

.payment-form-section {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 24px;
}

.custom-select-wrapper {
  position: relative;
}

.select-label {
  display: block;
  font-size: 12px;
  font-weight: 500;
  color: #666;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
}

.custom-select {
  width: 100%;
  padding: 12px 16px;
  padding-right: 40px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  background: white;
  appearance: none;
  transition: border-color 0.2s;
  height: 48px;
}

.custom-select:focus {
  outline: none;
  border-color: #1976d2;
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.1);
}

.custom-select:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
  opacity: 0.6;
}

.dropdown-icon {
  position: absolute;
  right: 12px;
  top: 38px;
  pointer-events: none;
  color: #666;
}

.selected-visit-info {
  border-left: 4px solid #1976d2;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.info-item .label {
  min-width: 100px;
  color: #666;
  margin-right: 8px;
}

.info-item .price {
  color: #1976d2;
  font-size: 18px;
}

.status-text {
  font-weight: 500;
}

.status-text.paid {
  color: #2e7d32;
}

.status-text.unpaid {
  color: #c62828;
}

.submit-btn {
  border-radius: 6px;
  text-transform: none;
  font-weight: 500;
}

.payments-history-section {
  margin-top: 24px;
}

.payment-item {
  border-radius: 8px;
  overflow: hidden;
  transition: box-shadow 0.2s;
}

.payment-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.payment-id {
  font-size: 14px;
  font-weight: 600;
  color: #666;
  background: #f5f5f5;
  padding: 4px 8px;
  border-radius: 4px;
  display: inline-block;
}

.patient-info {
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
}

.visit-date, .payment-date {
  font-size: 12px;
  color: #666;
  display: flex;
  align-items: center;
}

.amount {
  font-size: 18px;
  font-weight: 600;
  color: #1976d2;
}

.empty-state {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 40px 20px;
}

.payment-stats {
  margin-top: 24px;
}

.stats-content {
  padding: 16px !important;
}

.stat-item {
  text-align: center;
}

.stat-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
}

.stat-value.total-amount {
  color: #1976d2;
}

.stat-value.cash-amount {
  color: #2e7d32;
}

.stat-value.card-amount {
  color: #2196f3;
}

/* Адаптивность */
@media (max-width: 960px) {
  .payments-container {
    padding: 16px;
  }

  .title-text {
    font-size: 24px;
  }
}

@media (max-width: 600px) {
  .card-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start !important;
  }

  .title-text {
    font-size: 22px;
  }

  .v-spacer {
    display: none;
  }

  .payment-form-section {
    padding: 16px;
  }

  .payment-item .v-card-text {
    padding: 12px !important;
  }
}

option:disabled {
  color: #999;
  background-color: #f5f5f5;
}
</style>