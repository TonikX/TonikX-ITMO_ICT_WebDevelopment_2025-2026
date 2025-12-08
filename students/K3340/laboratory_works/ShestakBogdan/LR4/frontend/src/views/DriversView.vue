<template>
  <v-container class="mt-6">
    <div class="d-flex justify-space-between align-center mb-4">
      <h2>Водители</h2>

      <div>
        <v-btn color="primary" class="mr-2" @click="loadData">
          Обновить
        </v-btn>

        <v-btn
          v-if="isAdmin"
          color="secondary"
          @click="openCreateDialog"
        >
          Добавить водителя
        </v-btn>
      </div>
    </div>

    <v-data-table
      :items="drivers"
      :headers="headersToShow"
      :loading="loading"
      loading-text="Загрузка..."
      class="elevation-1"
    >
      <template #item.salary="{ item }">
        {{ item.salary }}
      </template>

      <template #item.actions="{ item }">
        <div v-if="isAdmin" class="d-flex ga-2">
          <v-btn
            size="small"
            variant="outlined"
            color="#929292"
            @click="openEditDialog(item)"
          >
            Изменить
          </v-btn>
          <v-btn
            size="small"
            variant="outlined"
            color="error"
            @click="deleteDriver(item)"
          >
            Удалить
          </v-btn>
        </div>
      </template>
    </v-data-table>

    <!-- Диалог создания / редактирования водителя -->
    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>
          {{ editedDriver.id ? 'Редактирование водителя' : 'Новый водитель' }}
        </v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field
              v-model="editedDriver.full_name"
              label="ФИО"
              required
            />
            <v-text-field
              v-model="editedDriver.passport"
              label="Паспорт"
              required
            />
            <v-select
              v-model="editedDriver.driver_class"
              :items="['A', 'B', 'C']"
              label="Класс"
              required
            />
            <v-text-field
              v-model.number="editedDriver.experience_years"
              label="Стаж (лет)"
              type="number"
            />
            <v-text-field
              v-model.number="editedDriver.base_salary"
              label="Базовый оклад"
              type="number"
            />
            <v-text-field
              v-model="editedDriver.birth_date"
              label="Дата рождения (ГГГГ-ММ-ДД)"
              placeholder="1990-01-01"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="saveDriver">
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import http from "../api/http";

const drivers = ref([]);
const loading = ref(false);
const isAdmin = ref(false);

const dialog = ref(false);
const editedDriver = ref({});

const baseHeaders = [
  { title: "ФИО", value: "full_name" },
  { title: "Класс", value: "driver_class" },
  { title: "Стаж", value: "experience_years" },
  { title: "Базовый оклад", value: "base_salary" },
  { title: "Зарплата", value: "salary" },
];

const headersToShow = computed(() => {
  if (isAdmin.value) {
    return [
      ...baseHeaders,
      { title: "Действия", value: "actions", sortable: false },
    ];
  }
  return baseHeaders;
});

const loadData = async () => {
  loading.value = true;
  try {
    // кто мы
    try {
      const meRes = await http.get("/api/me/");
      isAdmin.value = !!meRes.data.is_staff;
    } catch {
      isAdmin.value = false;
    }

    const driversRes = await http.get("/api/drivers/");
    drivers.value = driversRes.data;
  } catch (e) {
    console.error("Ошибка загрузки водителей:", e);
  } finally {
    loading.value = false;
  }
};

const openCreateDialog = () => {
  editedDriver.value = {
    full_name: "",
    passport: "",
    driver_class: "C",
    experience_years: 0,
    base_salary: 0,
    birth_date: "",
  };
  dialog.value = true;
};

const openEditDialog = (item) => {
  editedDriver.value = { ...item };
  dialog.value = true;
};

const closeDialog = () => {
  dialog.value = false;
};

const saveDriver = async () => {
  const data = { ...editedDriver.value };
  try {
    if (data.id) {
      await http.put(`/api/drivers/${data.id}/`, data);
    } else {
      await http.post("/api/drivers/", data);
    }
    dialog.value = false;
    await loadData();
  } catch (e) {
    console.error("Ошибка сохранения водителя:", e);
  }
};

const deleteDriver = async (item) => {
  if (!confirm(`Удалить водителя "${item.full_name}"?`)) return;
  try {
    await http.delete(`/api/drivers/${item.id}/`);
    await loadData();
  } catch (e) {
    console.error("Ошибка удаления водителя:", e);
  }
};

onMounted(loadData);
</script>