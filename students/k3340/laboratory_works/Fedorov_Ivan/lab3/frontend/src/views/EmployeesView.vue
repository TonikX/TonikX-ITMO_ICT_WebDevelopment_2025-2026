<template>
  <v-container>
    <div class="d-flex align-center mb-4">
      <h2 class="mr-4">Сотрудники</h2>
      <v-spacer />
      <v-btn color="primary" @click="openCreate">Добавить</v-btn>
    </div>

    <v-alert v-if="error" type="error" class="mb-3">{{ error }}</v-alert>

    <v-data-table :headers="headers" :items="employees" :loading="loading">
      <template #item.is_active="{ item }">
        <v-chip :color="item.is_active ? 'green' : 'grey'">
          {{ item.is_active ? "работает" : "уволен" }}
        </v-chip>
      </template>

      <template #item.actions="{ item }">
        <v-btn size="small" variant="text" @click="openEdit(item)">изм.</v-btn>
        <v-btn size="small" variant="text" color="red" @click="remove(item)">удал.</v-btn>

        <v-divider vertical class="mx-2" />

        <v-btn size="small" variant="text" color="orange" @click="unjob(item)">уволить</v-btn>
        <v-btn size="small" variant="text" color="green" @click="getjob(item)">принять</v-btn>
      </template>
    </v-data-table>

    <v-dialog v-model="dialog" max-width="520">
      <v-card>
        <v-card-title>{{ form.id ? "Изменить сотрудника" : "Добавить сотрудника" }}</v-card-title>
        <v-card-text>
          <v-text-field v-model="form.last_name" label="Фамилия" />
          <v-text-field v-model="form.first_name" label="Имя" />
          <v-text-field v-model="form.middle_name" label="Отчество" />
          <v-switch v-model="form.is_active" label="Работает" />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="dialog=false">Отмена</v-btn>
          <v-btn color="primary" :loading="saving" @click="save">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import http from "../services/http";
import { EP } from "../services/endpoints";

const employees = ref([]);
const loading = ref(false);
const saving = ref(false);
const error = ref("");

const headers = [
  { title: "ID", key: "id" },
  { title: "Фамилия", key: "last_name" },
  { title: "Имя", key: "first_name" },
  { title: "Отчество", key: "middle_name" },
  { title: "Статус", key: "is_active" },
  { title: "Действия", key: "actions", sortable: false },
];

const dialog = ref(false);
const form = ref({ id: null, last_name: "", first_name: "", middle_name: "", is_active: true });

function openCreate() {
  form.value = { id: null, last_name: "", first_name: "", middle_name: "", is_active: true };
  dialog.value = true;
}

function openEdit(item) {
  form.value = { ...item };
  dialog.value = true;
}

async function loadEmployees() {
  error.value = "";
  loading.value = true;
  try {
    const res = await http.get(EP.employees);
    employees.value = res.data;
  } catch (e) {
    error.value = "Не удалось загрузить сотрудников";
  } finally {
    loading.value = false;
  }
}

async function save() {
  saving.value = true;
  error.value = "";
  try {
    if (form.value.id) {
      await http.put(`${EP.employees}${form.value.id}/`, form.value);
    } else {
      await http.post(EP.employees, form.value);
    }
    dialog.value = false;
    await loadEmployees();
  } catch (e) {
    error.value = "Ошибка сохранения";
  } finally {
    saving.value = false;
  }
}

async function remove(item) {
  if (!confirm("Удалить сотрудника?")) return;
  try {
    await http.delete(`${EP.employees}${item.id}/`);
    await loadEmployees();
  } catch (e) {
    error.value = "Ошибка удаления";
  }
}

// кастомные: у тебя отдельные POST запросы
async function unjob(item) {
  try {
    await http.post(EP.unjobEmployees, { employee_id: item.id });
    await loadEmployees();
  } catch (e) {
    error.value = "Не удалось уволить (проверь EP.unjobEmployees)";
  }
}

async function getjob(item) {
  try {
    await http.post(EP.getjobEmployees, { employee_id: item.id });
    await loadEmployees();
  } catch (e) {
    error.value = "Не удалось принять (проверь EP.getjobEmployees)";
  }
}

onMounted(loadEmployees);
</script>
