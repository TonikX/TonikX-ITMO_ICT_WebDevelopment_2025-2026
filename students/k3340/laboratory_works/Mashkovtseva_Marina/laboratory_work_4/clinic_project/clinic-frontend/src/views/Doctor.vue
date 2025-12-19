<template>
  <div class="doctors-container">
    <div class="header-section">
      <h2 class="section-title">Врачи</h2>
      <p class="section-subtitle">Список врачей клиники</p>
    </div>

    <div class="content-grid">
      <!-- Форма добавления/редактирования врача -->
      <div class="card form-card">
        <h3 class="card-title">
          {{ isEditing ? 'Редактировать врача' : 'Добавить нового врача' }}
        </h3>

        <form @submit.prevent="isEditing ? updateDoctor() : createDoctor()" class="doctor-form">
          <div class="form-grid">
            <!-- ФИО -->
            <div class="form-group">
              <label class="form-label">
                <span class="label-text">Фамилия</span>
                <span class="required-mark">*</span>
              </label>
              <input
                v-model="currentDoctor.last_name"
                class="form-input"
                placeholder="Введите фамилию"
                required
                maxlength="100"
              >
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-text">Имя</span>
                <span class="required-mark">*</span>
              </label>
              <input
                v-model="currentDoctor.first_name"
                class="form-input"
                placeholder="Введите имя"
                required
                maxlength="100"
              >
            </div>

            <div class="form-group">
              <label class="form-label">Отчество</label>
              <input
                v-model="currentDoctor.middle_name"
                class="form-input"
                placeholder="Введите отчество"
                maxlength="100"
              >
            </div>

            <!-- Специальность и образование -->
            <div class="form-group">
              <label class="form-label">
                <span class="label-text">Специальность</span>
                <span class="required-mark">*</span>
              </label>
              <input
                v-model="currentDoctor.specialty"
                class="form-input"
                placeholder="Например: Терапевт"
                required
                maxlength="100"
              >
            </div>

            <div class="form-group">
              <label class="form-label">Образование</label>
              <input
                v-model="currentDoctor.education"
                class="form-input"
                placeholder="Учебное заведение"
                maxlength="255"
              >
            </div>

            <!-- Пол и дата рождения -->
            <div class="form-group">
              <label class="form-label">Пол</label>
              <select
                v-model="currentDoctor.gender"
                class="form-select"
              >
                <option value="" disabled>Выберите пол</option>
                <option value="male">Мужской</option>
                <option value="female">Женский</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Дата рождения</label>
              <input
                type="date"
                v-model="currentDoctor.birth_date"
                class="form-input"
              >
            </div>

            <!-- Даты работы -->
            <div class="form-group">
              <label class="form-label">
                <span class="label-text">Дата начала работы</span>
                <span class="required-mark">*</span>
              </label>
              <input
                type="date"
                v-model="currentDoctor.work_start_date"
                class="form-input"
                required
              >
            </div>

            <div class="form-group">
              <label class="form-label">Дата окончания работы</label>
              <input
                type="date"
                v-model="currentDoctor.work_end_date"
                class="form-input"
              >
            </div>

            <!-- Договорная информация -->
            <div class="form-group full-width">
              <label class="form-label">Информация о договоре</label>
              <textarea
                v-model="currentDoctor.contract_info"
                class="form-textarea"
                placeholder="Информация о трудовом договоре"
                rows="3"
              ></textarea>
            </div>
          </div>

          <div class="form-actions">
            <button
              v-if="isEditing"
              type="button"
              class="btn btn-secondary"
              @click="cancelEdit"
            >
              Отмена
            </button>
            <button type="submit" class="btn btn-primary">
              <span class="btn-icon">{{ isEditing ? '✓' : '+' }}</span>
              {{ isEditing ? 'Сохранить изменения' : 'Добавить врача' }}
            </button>
          </div>
        </form>
      </div>

      <!-- Список врачей -->
      <div class="card list-card">
        <div class="card-header">
          <h3 class="card-title">Список врачей</h3>
          <span class="badge">{{ doctors.length }}</span>
        </div>

        <div v-if="doctors.length === 0" class="empty-state">
          <div class="empty-icon">👨‍⚕️</div>
          <p>Нет врачей</p>
        </div>

        <div v-else class="doctors-list">
          <div
            v-for="doctor in doctors"
            :key="doctor.id"
            class="doctor-card"
          >
            <div class="visit-header">
              <div class="patient-info">
                <div class="patient-name">
                  {{ doctor.last_name }} {{ doctor.first_name }}
                  <span v-if="doctor.middle_name">{{ doctor.middle_name }}</span>
                </div>
                <div class="visit-price">{{ doctor.specialty }}</div>
              </div>
              <div class="doctor-actions">
                <button
                  class="btn-edit"
                  @click="startEdit(doctor)"
                  title="Редактировать"
                >
                  ✏️
                </button>
                <button
                  class="btn-delete"
                  @click="deleteDoctor(doctor.id)"
                  title="Удалить"
                >
                  🗑️
                </button>
              </div>
            </div>

            <div class="visit-details">
              <div class="detail-row">
                <span class="detail-label">Начало работы:</span>
                <span class="detail-value">{{ formatDate(doctor.work_start_date) }}</span>
              </div>

              <div v-if="doctor.work_end_date" class="detail-row">
                <span class="detail-label">Окончание:</span>
                <span class="detail-value">{{ formatDate(doctor.work_end_date) }}</span>
              </div>

              <div v-if="doctor.gender" class="detail-row">
                <span class="detail-label">Пол:</span>
                <span class="detail-value">{{ doctor.gender === 'male' ? 'Мужской' : 'Женский' }}</span>
              </div>

              <div v-if="doctor.education" class="detail-row">
                <span class="detail-label">Образование:</span>
                <span class="detail-value">{{ doctor.education }}</span>
              </div>

              <div v-if="doctor.birth_date" class="detail-row">
                <span class="detail-label">Дата рождения:</span>
                <span class="detail-value">{{ formatDate(doctor.birth_date) }}</span>
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
      doctors: [],
      isEditing: false,
      currentDoctor: {
        id: null,
        last_name: "",
        first_name: "",
        middle_name: "",
        specialty: "",
        education: "",
        gender: "",
        birth_date: "",
        work_start_date: "",
        work_end_date: "",
        contract_info: ""
      }
    };
  },
  async mounted() {
    await this.loadDoctors();
  },
  methods: {
    async loadDoctors() {
      try {
        const response = await api.get("/api/doctors/");
        this.doctors = response.data;
      } catch (error) {
        console.error("Ошибка загрузки врачей:", error);
      }
    },

    formatDate(dateStr) {
      if (!dateStr) return "";
      const date = new Date(dateStr);
      return date.toLocaleDateString('ru-RU');
    },

    startEdit(doctor) {
      this.isEditing = true;
      this.currentDoctor = {
        id: doctor.id,
        last_name: doctor.last_name,
        first_name: doctor.first_name,
        middle_name: doctor.middle_name || "",
        specialty: doctor.specialty,
        education: doctor.education || "",
        gender: doctor.gender || "",
        birth_date: doctor.birth_date ? doctor.birth_date.substring(0, 10) : "",
        work_start_date: doctor.work_start_date.substring(0, 10),
        work_end_date: doctor.work_end_date ? doctor.work_end_date.substring(0, 10) : "",
        contract_info: doctor.contract_info || ""
      };
    },

    cancelEdit() {
      this.isEditing = false;
      this.currentDoctor = {
        id: null,
        last_name: "",
        first_name: "",
        middle_name: "",
        specialty: "",
        education: "",
        gender: "",
        birth_date: "",
        work_start_date: "",
        work_end_date: "",
        contract_info: ""
      };
    },

    async createDoctor() {
      try {
        const payload = {
          ...this.currentDoctor,
          birth_date: this.currentDoctor.birth_date || null,
          work_end_date: this.currentDoctor.work_end_date || null,
          middle_name: this.currentDoctor.middle_name || null,
          education: this.currentDoctor.education || null,
          gender: this.currentDoctor.gender || null,
          contract_info: this.currentDoctor.contract_info || null
        };

        delete payload.id;

        await api.post("/api/doctors/", payload);
        await this.loadDoctors();
        this.cancelEdit();
        alert('Врач успешно добавлен!');
      } catch (error) {
        console.error("Ошибка создания врача:", error);
        alert("Произошла ошибка при создании врача");
      }
    },

    async updateDoctor() {
      try {
        const payload = {
          ...this.currentDoctor,
          birth_date: this.currentDoctor.birth_date || null,
          work_end_date: this.currentDoctor.work_end_date || null,
          middle_name: this.currentDoctor.middle_name || null,
          education: this.currentDoctor.education || null,
          gender: this.currentDoctor.gender || null,
          contract_info: this.currentDoctor.contract_info || null
        };

        await api.put(`/api/doctors/${this.currentDoctor.id}/`, payload);
        await this.loadDoctors();
        this.cancelEdit();
        alert('Изменения сохранены!');
      } catch (error) {
        console.error("Ошибка обновления врача:", error);
        alert("Произошла ошибка при обновлении врача");
      }
    },

    async deleteDoctor(id) {
      if (!confirm('Вы уверены, что хотите удалить этого врача?')) {
        return;
      }

      try {
        await api.delete(`/api/doctors/${id}/`);
        await this.loadDoctors();
        alert('Врач успешно удален!');
      } catch (error) {
        console.error("Ошибка удаления врача:", error);
        alert("Произошла ошибка при удалении врача");
      }
    }
  }
};
</script>

<style scoped>
.doctors-container {
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
}

.badge {
  background: #e3f2fd;
  color: #1976d2;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.doctor-form {
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

.form-input,
.form-select,
.form-textarea {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s;
  background: white;
  font-family: inherit;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
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

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid #eee;
  padding-top: 20px;
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

.btn-secondary {
  background: #f5f5f5;
  color: #666;
  border: 1px solid #ddd;
}

.btn-secondary:hover {
  background: #e0e0e0;
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

.doctors-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.doctor-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e9ecef;
}

.visit-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e9ecef;
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
  background: #e3f2fd;
  color: #1976d2;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
}

.doctor-actions {
  display: flex;
  gap: 8px;
}

.btn-edit,
.btn-delete {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  padding: 2px 6px;
  border-radius: 4px;
  transition: all 0.2s;
}

.btn-edit:hover {
  background: #e3f2fd;
}

.btn-delete:hover {
  background: #ffebee;
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
  min-width: 140px;
  flex-shrink: 0;
}

.detail-value {
  font-size: 14px;
  color: #333;
  flex-grow: 1;
}
</style>