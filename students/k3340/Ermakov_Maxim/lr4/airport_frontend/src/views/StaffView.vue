<template>
  <div class="page">
    <h1>Сотрудники (экипаж)</h1>

    <p v-if="loading">Загружаем сотрудников...</p>
    <p v-if="error" class="error">{{ error }}</p>

    <v-table v-if="items.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>ФИО</th>
          <th>Компания (id)</th>
          <th>Роль</th>
          <th>Стаж (лет)</th>
          <th>Активен</th>
          <th>Допуск</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="m in items" :key="m.id">
          <td>{{ m.id }}</td>
          <td>{{ m.full_name }}</td>
          <td>{{ m.company }}</td>
          <td>{{ m.role }}</td>
          <td>{{ m.experience_years }}</td>
          <td>{{ m.is_active ? "Да" : "Нет" }}</td>
          <td>{{ m.is_allowed ? "Допущен" : "Не допущен" }}</td>
          <td>
            <v-btn size="small" class="mr-1" @click="selectMember(m)">
              Редактировать
            </v-btn>
            <v-btn size="small" color="error" @click="deleteMember(m)">
              Удалить
            </v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>

    <p v-else-if="!loading && !error">
      Сотрудники не найдены.
    </p>

    <!-- v-dialog: редактирование сотрудника -->
    <v-dialog v-model="showEditModal" max-width="480">
      <v-card>
        <v-card-title class="d-flex justify-space-between align-center">
          <span>Редактирование сотрудника #{{ selected?.id }}</span>
          <v-btn icon="mdi-close" variant="text" @click="cancelEdit" />
        </v-card-title>

        <v-card-subtitle v-if="selected">
          <strong>{{ selected.full_name }}</strong>
        </v-card-subtitle>

        <v-card-text>
          <v-form @submit.prevent="saveMember">
            <v-text-field
              v-model="editRole"
              label="Роль"
              variant="outlined"
              density="comfortable"
              class="mb-3"
            />

            <v-text-field
              v-model.number="editExperienceYears"
              label="Стаж (лет)"
              type="number"
              min="0"
              variant="outlined"
              density="comfortable"
              class="mb-3"
            />

            <v-checkbox
              v-model="editIsActive"
              label="Активен"
              hide-details
              class="mb-1"
            />

            <v-checkbox
              v-model="editIsAllowed"
              label="Допущен к рейсам"
              hide-details
            />

            <div v-if="editError" class="error mt-2">
              {{ editError }}
            </div>
            <div v-if="editSuccess" class="success mt-2">
              Данные успешно сохранены.
            </div>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="cancelEdit">Отменить</v-btn>
          <v-btn
            color="primary"
            :loading="saving"
            @click="saveMember"
          >
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../api/api";

const loading = ref(false);
const error = ref("");
const items = ref([]);

// Состояние редактирования
const showEditModal = ref(false);
const selected = ref(null);
const editRole = ref("");
const editExperienceYears = ref(0);
const editIsActive = ref(true);
const editIsAllowed = ref(true);
const saving = ref(false);
const editError = ref("");
const editSuccess = ref(false);

const loadStaff = async () => {
  loading.value = true;
  error.value = "";
  try {
    const resp = await api.get("/api/crew-members/");
    items.value = resp.data;
  } catch (e) {
    console.error(e);
    error.value = "Ошибка при загрузке списка сотрудников.";
  } finally {
    loading.value = false;
  }
};

const selectMember = (member) => {
  selected.value = { ...member };
  editRole.value = member.role;
  editExperienceYears.value = member.experience_years ?? 0;
  editIsActive.value = member.is_active;
  editIsAllowed.value = member.is_allowed;
  editError.value = "";
  editSuccess.value = false;
  showEditModal.value = true;
};

const cancelEdit = () => {
  showEditModal.value = false;
  selected.value = null;
  editRole.value = "";
  editExperienceYears.value = 0;
  editIsActive.value = true;
  editIsAllowed.value = true;
  editError.value = "";
  editSuccess.value = false;
};

const saveMember = async () => {
  if (!selected.value) return;
  saving.value = true;
  editError.value = "";
  editSuccess.value = false;

  try {
    const payload = {
      role: editRole.value,
      experience_years: editExperienceYears.value,
      is_active: editIsActive.value,
      is_allowed: editIsAllowed.value,
    };

    await api.patch(`/api/crew-members/${selected.value.id}/`, payload);

    editSuccess.value = true;
    await loadStaff();
  } catch (e) {
    console.error(e);
    editError.value = "Ошибка при сохранении изменений.";
  } finally {
    saving.value = false;
  }
};

const deleteMember = async (member) => {
  const ok = window.confirm(
    `Точно удалить сотрудника "${member.full_name}" (id=${member.id})?`
  );
  if (!ok) return;

  try {
    await api.delete(`/api/crew-members/${member.id}/`);
    if (selected.value && selected.value.id === member.id) {
      cancelEdit();
    }
    await loadStaff();
  } catch (e) {
    console.error(e);
    alert("Ошибка при удалении сотрудника.");
  }
};

onMounted(loadStaff);
</script>

<style scoped>
.error {
  color: #d32f2f;
}

.success {
  color: #2e7d32;
}
</style>