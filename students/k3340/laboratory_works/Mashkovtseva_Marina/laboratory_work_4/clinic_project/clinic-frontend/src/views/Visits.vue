<template>
  <div class="visits-container">
    <div class="header-section">
      <h2 class="section-title">Управление визитами</h2>
      <p class="section-subtitle">Добавление и просмотр записей о визитах пациентов</p>
    </div>

    <div class="content-grid">
      <!-- Форма добавления визита -->
      <div class="card form-card">
        <h3 class="card-title">Добавить новый визит</h3>

        <form @submit.prevent="createVisit" class="visit-form">
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">
                <span class="label-text">Пациент</span>
                <span class="required-mark">*</span>
              </label>
              <select
                v-model="newVisit.record_id"
                class="form-select"
                required
              >
                <option value="" disabled>Выберите пациента</option>
                <option
                  v-for="patient in patients"
                  :key="patient.id"
                  :value="patient.medical_record_id"
                >
                  {{ patient.last_name }} {{ patient.first_name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-text">Врач</span>
                <span class="required-mark">*</span>
              </label>
              <select
                v-model="newVisit.doctor"
                class="form-select"
                required
              >
                <option value="" disabled>Выберите врача</option>
                <option
                  v-for="doctor in doctors"
                  :key="doctor.id"
                  :value="doctor.id"
                >
                  {{ doctor.last_name }} ({{ doctor.specialty }})
                </option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Кабинет</label>
              <select
                v-model="newVisit.room"
                class="form-select"
              >
                <option value="">Не выбран</option>
                <option
                  v-for="room in rooms"
                  :key="room.id"
                  :value="room.id"
                >
                  Кабинет {{ room.room_number }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-text">Дата и время</span>
                <span class="required-mark">*</span>
              </label>
              <input
                type="datetime-local"
                v-model="newVisit.visit_datetime"
                class="form-input"
                required
              >
            </div>

            <div class="form-group full-width">
              <label class="form-label">Диагноз</label>
              <input
                v-model="newVisit.diagnosis"
                class="form-input"
                placeholder="Введите диагноз"
              >
            </div>

            <div class="form-group full-width">
              <label class="form-label">Состояние пациента</label>
              <input
                v-model="newVisit.patient_condition"
                class="form-input"
                placeholder="Опишите состояние пациента"
              >
            </div>

            <div class="form-group full-width">
              <label class="form-label">Рекомендации</label>
              <input
                v-model="newVisit.recommendations"
                class="form-input"
                placeholder="Введите рекомендации"
              >
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-text">Стоимость (₽)</span>
                <span class="required-mark">*</span>
              </label>
              <input
                v-model="newVisit.price"
                type="number"
                class="form-input"
                placeholder="0"
                min="0"
                required
              >
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn btn-primary">
              <span class="btn-icon">+</span>
              Добавить визит
            </button>
          </div>
        </form>
      </div>

      <!-- Список визитов -->
      <div class="card list-card">
        <div class="card-header">
          <h3 class="card-title">Записи о визитах</h3>
          <div class="header-stats">
            <span class="badge">{{ visits.length }}</span>
            <div class="stats-info">
              <span class="stat-item paid-stat">
                <span class="stat-dot paid"></span>
                Оплачено: {{ paidVisitsCount }}
              </span>
              <span class="stat-item unpaid-stat">
                <span class="stat-dot unpaid"></span>
                Не оплачено: {{ unpaidVisitsCount }}
              </span>
            </div>
          </div>
        </div>

        <div v-if="visits.length === 0" class="empty-state">
          <div class="empty-icon">📋</div>
          <p>Нет записей о визитах</p>
        </div>

        <div v-else class="visits-list">
          <div
            v-for="visit in visits"
            :key="visit.id"
            :class="['visit-card', visit.is_paid ? 'paid' : 'unpaid']"
          >
            <!-- Бейдж статуса оплаты -->
            <div :class="['payment-status', visit.is_paid ? 'paid' : 'unpaid']">
              <span class="status-icon">
                {{ visit.is_paid ? '✓' : '●' }}
              </span>
              <span class="status-text">
                {{ visit.is_paid ? 'Оплачено' : 'Не оплачено' }}
              </span>
            </div>

            <div class="visit-header">
              <div class="patient-info">
                <div class="patient-name">
                  {{ visit.record.patient.last_name }}
                  {{ visit.record.patient.first_name }}
                </div>
                <div class="visit-price">{{ visit.price }} ₽</div>
              </div>
              <div class="visit-time">
                {{ formatDate(visit.visit_datetime) }}
              </div>
            </div>

            <div class="visit-details">
              <div class="detail-row">
                <span class="detail-label">Врач:</span>
                <span class="detail-value">
                  {{ visit.doctor_detail.last_name }}
                  ({{ visit.doctor_detail.specialty }})
                </span>
              </div>

              <div class="detail-row">
                <span class="detail-label">Кабинет:</span>
                <span class="detail-value">
                  {{ visit.room_detail ? `Кабинет ${visit.room_detail.room_number}` : "—" }}
                </span>
              </div>

              <div v-if="visit.diagnosis" class="detail-row">
                <span class="detail-label">Диагноз:</span>
                <span class="detail-value">{{ visit.diagnosis }}</span>
              </div>

              <div v-if="visit.patient_condition" class="detail-row">
                <span class="detail-label">Состояние:</span>
                <span class="detail-value">{{ visit.patient_condition }}</span>
              </div>

              <div v-if="visit.recommendations" class="detail-row">
                <span class="detail-label">Рекомендации:</span>
                <span class="detail-value">{{ visit.recommendations }}</span>
              </div>

              <!-- Дата оплаты, если визит оплачен -->
              <div v-if="visit.payment_date" class="detail-row">
                <span class="detail-label">Дата оплаты:</span>
                <span class="detail-value payment-date">
                  {{ formatDate(visit.payment_date) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../api/axios";

export default {
  data() {
    return {
      patients: [],
      doctors: [],
      rooms: [],
      visits: [],
      newVisit: {
        record_id: "",
        doctor: "",
        room: "",
        visit_datetime: "",
        diagnosis: "",
        patient_condition: "",
        recommendations: "",
        price: "",
      },
    };
  },
  computed: {
    paidVisitsCount() {
      return this.visits.filter(v => v.is_paid).length;
    },
    unpaidVisitsCount() {
      return this.visits.filter(v => !v.is_paid).length;
    }
  },
  async mounted() {
    try {
      [this.patients, this.doctors, this.rooms, this.visits] = await Promise.all([
        api.get("/api/patients/").then(r => r.data),
        api.get("/api/doctors/").then(r => r.data),
        api.get("/api/rooms/").then(r => r.data),
        api.get("/api/visits/").then(r => r.data),
      ]);
    } catch (error) {
      console.error("Ошибка загрузки данных:", error);
    }
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return "";
      return dateStr
          .replace("T", " ")
          .replace(":00Z", "")
          .replace(/-/g, ".");
    },

    async createVisit() {
      try {
        const payload = {
          record_id: Number(this.newVisit.record_id),
          doctor: Number(this.newVisit.doctor),
          room: this.newVisit.room ? Number(this.newVisit.room) : null,
          visit_datetime: this.newVisit.visit_datetime + ":00",
          diagnosis: this.newVisit.diagnosis || null,
          patient_condition: this.newVisit.patient_condition || null,
          recommendations: this.newVisit.recommendations || null,
          price: Number(this.newVisit.price),
        };

        await api.post("/api/visits/", payload);

        // Обновляем список визитов
        this.visits = (await api.get("/api/visits/")).data;

        // Сбрасываем форму
        this.newVisit = {
          record_id: "",
          doctor: "",
          room: "",
          visit_datetime: "",
          diagnosis: "",
          patient_condition: "",
          recommendations: "",
          price: "",
        };

      } catch (error) {
        console.error("Ошибка создания визита:", error);
        alert("Произошла ошибка при создании визита");
      }
    }
  },
};
</script>

<style scoped>
.visits-container {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.header-section {
  margin-bottom: 32px;
}

.section-title {
  font-size: 28px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.section-subtitle {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 24px;
}

.form-card {
  height: fit-content;
}

.list-card {
  max-height: 800px;
  overflow-y: auto;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 20px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}

.header-stats {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stats-info {
  display: flex;
  gap: 12px;
  font-size: 13px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #666;
}

.stat-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.stat-dot.paid {
  background-color: #4caf50;
}

.stat-dot.unpaid {
  background-color: #ff9800;
}

.paid-stat .stat-dot {
  background-color: #4caf50;
}

.unpaid-stat .stat-dot {
  background-color: #ff9800;
}

.badge {
  background: #e3f2fd;
  color: #1976d2;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.visit-form {
  margin-top: 8px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-label {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.label-text {
  margin-right: 4px;
}

.required-mark {
  color: #f44336;
}

.form-select,
.form-input {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s;
  background: white;
}

.form-select:focus,
.form-input:focus {
  outline: none;
  border-color: #2196f3;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
}

.form-select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23666' d='M6 8.825L1.175 4 2.238 2.938 6 6.7l3.763-3.763L10.825 4z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 36px;
}

.form-actions {
  border-top: 1px solid #eee;
  padding-top: 20px;
  text-align: right;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.btn-primary {
  background: #2196f3;
  color: white;
}

.btn-primary:hover {
  background: #1976d2;
}

.btn-icon {
  margin-right: 8px;
  font-size: 16px;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.visits-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.visit-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e9ecef;
  position: relative;
  overflow: hidden;
}

/* Левая полоса статуса */
.visit-card.paid {
  border-left: 4px solid #4caf50;
}

.visit-card.unpaid {
  border-left: 4px solid #ff9800;
}

/* Бейдж статуса оплаты */
.payment-status {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

.payment-status.paid {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.payment-status.unpaid {
  background-color: #fff3e0;
  color: #ef6c00;
}

.status-icon {
  font-size: 10px;
}

.visit-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e9ecef;
  padding-right: 80px; /* Место для бейджа */
}

.patient-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.patient-name {
  font-weight: 600;
  color: #1a1a1a;
}

.visit-price {
  background: #e8f5e9;
  color: #2e7d32;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
}

.visit-time {
  font-size: 13px;
  color: #666;
  white-space: nowrap;
}

.visit-details {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.detail-row {
  display: flex;
  align-items: flex-start;
}

.detail-label {
  font-size: 13px;
  color: #666;
  min-width: 120px;
  flex-shrink: 0;
}

.detail-value {
  font-size: 14px;
  color: #333;
  flex-grow: 1;
}

.payment-date {
  color: #4caf50;
  font-weight: 500;
}

/* Адаптивность */
@media (max-width: 768px) {
  .header-stats {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .stats-info {
    flex-direction: column;
    gap: 4px;
  }

  .visit-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    padding-right: 0;
  }

  .payment-status {
    position: static;
    margin-bottom: 8px;
    align-self: flex-start;
  }
}
</style>