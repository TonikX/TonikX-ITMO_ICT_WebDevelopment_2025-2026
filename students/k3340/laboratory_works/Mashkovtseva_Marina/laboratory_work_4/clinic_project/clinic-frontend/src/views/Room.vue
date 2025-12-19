<template>
  <div class="rooms-container">
    <div class="header-section">
      <h2 class="section-title">Кабинеты</h2>
      <p class="section-subtitle">Список кабинетов клиники</p>
    </div>

    <div class="content-grid">
      <!-- Форма добавления/редактирования кабинета -->
      <div class="card form-card">
        <h3 class="card-title">
          {{ isEditing ? 'Редактировать кабинет' : 'Добавить новый кабинет' }}
        </h3>

        <form @submit.prevent="isEditing ? updateRoom() : createRoom()" class="room-form">
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">
                <span class="label-text">Номер кабинета</span>
                <span class="required-mark">*</span>
              </label>
              <input
                v-model="currentRoom.room_number"
                class="form-input"
                placeholder="Например: 101"
                required
                maxlength="20"
              >
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-text">Начало работы</span>
                <span class="required-mark">*</span>
              </label>
              <input
                type="time"
                v-model="currentRoom.work_time_start"
                class="form-input"
                required
              >
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-text">Окончание работы</span>
                <span class="required-mark">*</span>
              </label>
              <input
                type="time"
                v-model="currentRoom.work_time_end"
                class="form-input"
                required
              >
            </div>

            <div class="form-group">
              <label class="form-label">Ответственное лицо</label>
              <input
                v-model="currentRoom.responsible_person"
                class="form-input"
                placeholder="ФИО ответственного"
                maxlength="100"
              >
            </div>

            <div class="form-group">
              <label class="form-label">Внутренний телефон</label>
              <input
                v-model="currentRoom.internal_phone"
                class="form-input"
                placeholder="Например: 123"
                maxlength="20"
              >
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
              {{ isEditing ? 'Сохранить изменения' : 'Добавить кабинет' }}
            </button>
          </div>
        </form>
      </div>

      <!-- Список кабинетов -->
      <div class="card list-card">
        <div class="card-header">
          <h3 class="card-title">Список кабинетов</h3>
          <span class="badge">{{ rooms.length }}</span>
        </div>

        <div v-if="rooms.length === 0" class="empty-state">
          <div class="empty-icon">🚪</div>
          <p>Нет кабинетов</p>
        </div>

        <div v-else class="rooms-list">
          <div
            v-for="room in rooms"
            :key="room.id"
            class="room-card"
          >
            <div class="visit-header">
              <div class="patient-info">
                <div class="patient-name">
                  Кабинет {{ room.room_number }}
                </div>
                <div class="visit-time">
                  {{ formatTime(room.work_time_start) }} - {{ formatTime(room.work_time_end) }}
                </div>
              </div>
              <div class="doctor-actions">
                <button
                  class="btn-edit"
                  @click="startEdit(room)"
                  title="Редактировать"
                >
                  ✏️
                </button>
                <button
                  class="btn-delete"
                  @click="deleteRoom(room.id)"
                  title="Удалить"
                >
                  🗑️
                </button>
              </div>
            </div>

            <div class="visit-details">
              <div v-if="room.responsible_person" class="detail-row">
                <span class="detail-label">Ответственный:</span>
                <span class="detail-value">{{ room.responsible_person }}</span>
              </div>

              <div v-if="room.internal_phone" class="detail-row">
                <span class="detail-label">Внутренний телефон:</span>
                <span class="detail-value">{{ room.internal_phone }}</span>
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
      rooms: [],
      isEditing: false,
      currentRoom: {
        id: null,
        room_number: "",
        work_time_start: "09:00",
        work_time_end: "18:00",
        responsible_person: "",
        internal_phone: ""
      }
    };
  },
  async mounted() {
    await this.loadRooms();
  },
  methods: {
    async loadRooms() {
      try {
        const response = await api.get("/api/rooms/");
        this.rooms = response.data;
      } catch (error) {
        console.error("Ошибка загрузки кабинетов:", error);
      }
    },

    formatTime(timeStr) {
      if (!timeStr) return "";
      return timeStr.substring(0, 5);
    },

    startEdit(room) {
      this.isEditing = true;
      this.currentRoom = {
        id: room.id,
        room_number: room.room_number,
        work_time_start: room.work_time_start.substring(0, 5),
        work_time_end: room.work_time_end.substring(0, 5),
        responsible_person: room.responsible_person || "",
        internal_phone: room.internal_phone || ""
      };
    },

    cancelEdit() {
      this.isEditing = false;
      this.currentRoom = {
        id: null,
        room_number: "",
        work_time_start: "09:00",
        work_time_end: "18:00",
        responsible_person: "",
        internal_phone: ""
      };
    },

    async createRoom() {
      try {
        const payload = {
          ...this.currentRoom,
          work_time_start: this.currentRoom.work_time_start + ":00",
          work_time_end: this.currentRoom.work_time_end + ":00",
          responsible_person: this.currentRoom.responsible_person || null,
          internal_phone: this.currentRoom.internal_phone || null
        };

        delete payload.id;

        await api.post("/api/rooms/", payload);
        await this.loadRooms();
        this.cancelEdit();
        alert('Кабинет успешно добавлен!');
      } catch (error) {
        console.error("Ошибка создания кабинета:", error);
        alert("Произошла ошибка при создании кабинета");
      }
    },

    async updateRoom() {
      try {
        const payload = {
          ...this.currentRoom,
          work_time_start: this.currentRoom.work_time_start + ":00",
          work_time_end: this.currentRoom.work_time_end + ":00",
          responsible_person: this.currentRoom.responsible_person || null,
          internal_phone: this.currentRoom.internal_phone || null
        };

        await api.put(`/api/rooms/${this.currentRoom.id}/`, payload);
        await this.loadRooms();
        this.cancelEdit();
        alert('Изменения сохранены!');
      } catch (error) {
        console.error("Ошибка обновления кабинета:", error);
        alert("Произошла ошибка при обновлении кабинета");
      }
    },

    async deleteRoom(id) {
      if (!confirm('Вы уверены, что хотите удалить этот кабинет?')) {
        return;
      }

      try {
        await api.delete(`/api/rooms/${id}/`);
        await this.loadRooms();
        alert('Кабинет успешно удален!');
      } catch (error) {
        console.error("Ошибка удаления кабинета:", error);
        alert("Произошла ошибка при удалении кабинета");
      }
    }
  }
};
</script>

<style scoped>
.rooms-container {
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

.room-form {
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

.form-input {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s;
  background: white;
}

.form-input:focus {
  outline: none;
  border-color: #2196f3;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
}

input[type="time"] {
  font-family: inherit;
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

.rooms-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.room-card {
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
  font-size: 16px;
}

.visit-time {
  background: #e8f5e9;
  color: #2e7d32;
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