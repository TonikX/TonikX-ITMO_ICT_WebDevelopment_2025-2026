<template>
  <div class="patients-container">
    <v-card class="patients-card" elevation="2">
      <!-- Заголовок -->
      <v-card-title class="card-header">
        <span class="title-text">Пациенты</span>
        <v-spacer />
        <v-btn color="primary" @click="openAddDialog" class="add-btn" large>
          <v-icon left>mdi-plus</v-icon>
          Добавить пациента
        </v-btn>
      </v-card-title>

      <!-- Таблица -->
      <v-card-text class="table-container">
        <v-data-table
          :headers="headers"
          :items="patients"
          item-key="id"
          class="elevation-1 patients-table"
          :loading="loading"
          loading-text="Загрузка данных..."
          :items-per-page="10"
          :footer-props="{ showFirstLastPage: false }"
        >
          <!-- Колонка даты рождения -->
          <template v-slot:item.birth_date="{ item }">
            {{ formatDate(item.birth_date) }}
          </template>

          <!-- Действия -->
          <template v-slot:item.actions="{ item }">
            <div style="display: flex; gap: 8px;">
              <v-btn color="primary" @click="openEditDialog(item)" small icon>
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn color="error" @click="deletePatient(item.id)" small icon>
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </div>
          </template>

          <!-- Нет данных -->
          <template v-slot:no-data>
            <div class="text-center py-6">
              <v-icon size="64" color="grey lighten-1">mdi-account-group</v-icon>
              <div class="text-h6 grey--text mt-4">Нет данных о пациентах</div>
              <v-btn color="primary" @click="openAddDialog" class="mt-4">
                Добавить первого пациента
              </v-btn>
            </div>
          </template>

          <!-- Кастомная пагинация -->
          <template v-slot:footer="{ props }">
            <div class="custom-footer">
              <div class="footer-left">
                <span>Записей на странице:</span>
                <v-select
                  :items="[5, 10, 20, 50]"
                  v-model="props.itemsPerPage"
                  dense
                  hide-details
                  class="page-select"
                />
              </div>

              <div class="footer-center">
                {{ props.pageStart }}-{{ props.pageStop }} из {{ props.itemsLength }}
              </div>

              <div class="footer-right">
                <v-btn icon small :disabled="props.page === 1" @click="props.previousPage">
                  <v-icon>mdi-chevron-left</v-icon>
                </v-btn>

                <span class="page-number">{{ props.page }}</span>

                <v-btn
                  icon
                  small
                  :disabled="props.pageStop >= props.itemsLength"
                  @click="props.nextPage"
                >
                  <v-icon>mdi-chevron-right</v-icon>
                </v-btn>
              </div>
            </div>
          </template>
        </v-data-table>
      </v-card-text>

      <!-- Футер -->
      <v-card-actions class="card-footer">
        <div class="patient-count">
          Всего пациентов: <strong>{{ patients.length }}</strong>
        </div>
        <v-spacer />
        <v-btn text color="grey" @click="loadPatients">
          <v-icon left>mdi-refresh</v-icon>
          Обновить
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- Диалог добавления/редактирования -->
    <v-dialog v-model="dialog" max-width="600" persistent>
      <v-card class="dialog-card">
        <v-card-title class="dialog-header">
          <span class="dialog-title">{{ isEditing ? 'Редактирование пациента' : 'Новый пациент' }}</span>
          <v-spacer />
          <v-btn icon @click="closeDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="dialog-content">
          <v-row>
            <v-col cols="12" md="4">
              <v-text-field
                label="Фамилия *"
                v-model="currentPatient.last_name"
                outlined dense
                required
                :rules="[v => !!v || 'Обязательное поле']"
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                label="Имя *"
                v-model="currentPatient.first_name"
                outlined dense
                required
                :rules="[v => !!v || 'Обязательное поле']"
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                label="Отчество"
                v-model="currentPatient.middle_name"
                outlined dense
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                label="Дата рождения"
                v-model="currentPatient.birth_date"
                type="date"
                outlined dense
                prepend-icon="mdi-calendar"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                label="Телефон"
                v-model="currentPatient.phone"
                outlined dense
                prepend-icon="mdi-phone"
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12">
              <v-textarea
                label="Адрес"
                v-model="currentPatient.address"
                outlined dense
                rows="2"
                prepend-icon="mdi-home"
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12">
              <v-text-field
                label="Паспортные данные"
                v-model="currentPatient.passport_data"
                outlined dense
                prepend-icon="mdi-card-account-details"
              />
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-actions class="dialog-actions">
          <v-spacer />
          <v-btn text @click="closeDialog" class="cancel-btn">Отмена</v-btn>
          <v-btn color="primary" @click="savePatient" :disabled="!isFormValid" :loading="saving" class="save-btn">
            {{ isEditing ? 'Сохранить изменения' : 'Сохранить пациента' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import api from "../api/axios";

export default {
  data() {
    return {
      dialog: false,
      loading: false,
      saving: false,
      isEditing: false,
      patients: [],
      headers: [
        { text: "ID", value: "id", width: "80px" },
        { text: "Фамилия", value: "last_name" },
        { text: "Имя", value: "first_name" },
        { text: "Отчество", value: "middle_name" },
        { text: "Дата рождения", value: "birth_date" },
        { text: "Телефон", value: "phone" },
        { text: "Действия", value: "actions", sortable: false, width: "120px" },
      ],
      currentPatient: {
        id: null,
        last_name: "",
        first_name: "",
        middle_name: "",
        birth_date: "",
        phone: "",
        address: "",
        passport_data: "",
      },
    };
  },
  computed: {
    isFormValid() {
      return this.currentPatient.last_name && this.currentPatient.first_name;
    },
  },
  async mounted() {
    await this.loadPatients();
  },
  methods: {
    async loadPatients() {
      this.loading = true;
      try {
        this.patients = (await api.get("/api/patients/")).data;
      } catch (error) {
        console.error(error);
        alert("Ошибка загрузки пациентов");
      } finally {
        this.loading = false;
      }
    },
    openAddDialog() {
      this.isEditing = false;
      this.resetForm();
      this.dialog = true;
    },
    openEditDialog(patient) {
      this.isEditing = true;
      this.currentPatient = { ...patient };
      if (this.currentPatient.birth_date) {
        this.currentPatient.birth_date = this.formatDateForInput(this.currentPatient.birth_date);
      }
      this.dialog = true;
    },
    async savePatient() {
      if (!this.isFormValid) return;
      this.saving = true;
      try {
        if (this.isEditing) {
          await api.put(`/api/patients/${this.currentPatient.id}/`, this.currentPatient);
          alert("Данные пациента обновлены");
        } else {
          await api.post("/api/patients/", this.currentPatient);
          alert("Пациент успешно добавлен");
        }
        this.closeDialog();
        await this.loadPatients();
      } catch (error) {
        console.error(error);
        alert(`Ошибка: ${error.response?.data?.message || error.message}`);
      } finally {
        this.saving = false;
      }
    },
    async deletePatient(id) {
      if (!confirm("Вы уверены, что хотите удалить этого пациента?")) return;
      try {
        await api.delete(`/api/patients/${id}/`);
        await this.loadPatients();
        alert("Пациент удален");
      } catch (error) {
        console.error(error);
        alert("Ошибка при удалении пациента");
      }
    },
    closeDialog() {
      this.dialog = false;
      this.resetForm();
    },
    resetForm() {
      this.currentPatient = {
        id: null,
        last_name: "",
        first_name: "",
        middle_name: "",
        birth_date: "",
        phone: "",
        address: "",
        passport_data: "",
      };
    },
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('ru-RU');
    },
    formatDateForInput(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toISOString().split('T')[0];
    },
  },
};
</script>

<style scoped>
.patients-container {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.patients-card {
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

.add-btn {
  border-radius: 8px;
  text-transform: none;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.2);
}

.table-container {
  padding: 0 !important;
}

.patients-table {
  border: none;
}

.patients-table >>> .v-data-table-header {
  background-color: #f8f9fa;
}

.patients-table >>> th {
  font-weight: 600 !important;
  color: #2c3e50 !important;
  background-color: #f8f9fa !important;
}

/* Кастомная пагинация */
.custom-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-top: 1px solid #e0e0e0;
  background-color: #f8f9fa;
}

.footer-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.footer-center {
  font-size: 14px;
  color: #666;
}

.footer-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-select {
  width: 70px;
}

.page-number {
  min-width: 20px;
  text-align: center;
  font-weight: 500;
}

.card-footer {
  background: #f8f9fa;
  padding: 16px 24px;
  border-top: 1px solid #e0e0e0;
}

.patient-count {
  font-size: 14px;
  color: #666;
}

/* Диалог стили */
.dialog-card {
  border-radius: 12px;
}

.dialog-header {
  background: linear-gradient(135deg, #1976d2 0%, #0d47a1 100%);
  color: white !important;
  padding: 20px 24px !important;
}

.dialog-title {
  font-size: 20px;
  font-weight: 500;
}

.dialog-content {
  padding: 24px !important;
}

.dialog-actions {
  padding: 16px 24px !important;
  border-top: 1px solid #e0e0e0;
}

.cancel-btn {
  text-transform: none;
  font-weight: 500;
}

.save-btn {
  text-transform: none;
  font-weight: 500;
  border-radius: 6px;
  padding: 8px 24px !important;
}

/* Адаптивность */
@media (max-width: 960px) {
  .patients-container {
    padding: 16px;
  }

  .title-text {
    font-size: 24px;
  }

  .add-btn {
    font-size: 14px;
    padding: 8px 16px !important;
  }

  .custom-footer {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .footer-left,
  .footer-center,
  .footer-right {
    justify-content: center;
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
}
</style>