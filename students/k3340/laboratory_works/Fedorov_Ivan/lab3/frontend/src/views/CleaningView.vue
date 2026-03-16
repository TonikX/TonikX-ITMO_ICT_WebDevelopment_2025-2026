<template>
  <v-container>
    <div class="d-flex align-center mb-4">
      <h2 class="mr-4">График уборки</h2>
      <v-spacer />
      <v-btn color="primary" @click="openCreate">Добавить</v-btn>
    </div>

    <v-alert v-if="error" type="error" class="mb-3">{{ error }}</v-alert>

    <v-data-table :headers="headers" :items="items" :loading="loading">
      <template #item.actions="{ item }">
        <v-btn size="small" variant="text" @click="openEdit(item)">изм.</v-btn>
        <v-btn size="small" variant="text" color="red" @click="remove(item)">удал.</v-btn>
      </template>
    </v-data-table>

    <v-dialog v-model="dialog" max-width="520">
      <v-card>
        <v-card-title>{{ form.id ? "Изменить" : "Добавить" }}</v-card-title>
        <v-card-text>
          <v-text-field v-model.number="form.employee" label="Employee ID" type="number" />
          <v-text-field v-model.number="form.floor" label="Этаж" type="number" />
          <v-select
            v-model="form.day_of_week"
            label="День"
            :items="[
              { title: 'mon', value: 'mon' },
              { title: 'tue', value: 'tue' },
              { title: 'wed', value: 'wed' },
              { title: 'thu', value: 'thu' },
              { title: 'fri', value: 'fri' },
              { title: 'sat', value: 'sat' },
              { title: 'sun', value: 'sun' },
            ]"
          />
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

const items = ref([]);
const loading = ref(false);
const saving = ref(false);
const error = ref("");

const headers = [
  { title: "ID", key: "id" },
  { title: "Employee", key: "employee" },
  { title: "Этаж", key: "floor" },
  { title: "День", key: "day_of_week" },
  { title: "Действия", key: "actions", sortable: false },
];

const dialog = ref(false);
const form = ref({ id: null, employee: null, floor: 1, day_of_week: "mon" });

function openCreate() {
  form.value = { id: null, employee: null, floor: 1, day_of_week: "mon" };
  dialog.value = true;
}

function openEdit(item) {
  form.value = { ...item };
  dialog.value = true;
}

async function load() {
  error.value = "";
  loading.value = true;
  try {
    const res = await http.get(EP.cleaning);
    items.value = res.data;
  } catch (e) {
    error.value = "Не удалось загрузить график";
  } finally {
    loading.value = false;
  }
}

async function save() {
  saving.value = true;
  try {
    if (form.value.id) {
      await http.put(`${EP.cleaning}${form.value.id}/`, form.value);
    } else {
      await http.post(EP.cleaning, form.value);
    }
    dialog.value = false;
    await load();
  } catch (e) {
    error.value = "Ошибка сохранения (проверь employee id)";
  } finally {
    saving.value = false;
  }
}

async function remove(item) {
  if (!confirm("Удалить запись?")) return;
  try {
    await http.delete(`${EP.cleaning}${item.id}/`);
    await load();
  } catch (e) {
    error.value = "Ошибка удаления";
  }
}

onMounted(load);
</script>
