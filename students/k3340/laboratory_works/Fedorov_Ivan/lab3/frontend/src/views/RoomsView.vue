<template>
  <v-container>
    <div class="d-flex align-center mb-4">
      <h2 class="mr-4">Номера</h2>
      <v-spacer />
      <v-btn color="primary" @click="openCreate">Добавить</v-btn>
      <v-btn class="ml-2" variant="outlined" @click="loadAvailable">Свободные</v-btn>
      <v-btn class="ml-2" variant="outlined" @click="loadAll">Все</v-btn>
    </div>

    <v-alert v-if="error" type="error" class="mb-3">{{ error }}</v-alert>

    <v-data-table :headers="headers" :items="rooms" :loading="loading">
      <template #item.is_available="{ item }">
        <v-chip :color="item.is_available ? 'green' : 'red'">
          {{ item.is_available ? "Свободен" : "Занят" }}
        </v-chip>
      </template>

      <template #item.actions="{ item }">
        <v-btn size="small" variant="text" @click="openEdit(item)">изм.</v-btn>
        <v-btn size="small" variant="text" color="red" @click="remove(item)">удал.</v-btn>
      </template>
    </v-data-table>

    <v-dialog v-model="dialog" max-width="520">
      <v-card>
        <v-card-title>{{ form.id ? "Изменить номер" : "Добавить номер" }}</v-card-title>
        <v-card-text>
          <v-text-field v-model="form.number" label="Номер" />
          <v-text-field v-model.number="form.floor" label="Этаж" type="number" />
          <v-select
            v-model="form.room_type"
            label="Тип"
            :items="[
              { title: 'single', value: 'single' },
              { title: 'double', value: 'double' },
              { title: 'triple', value: 'triple' },
            ]"
          />
          <v-text-field v-model.number="form.price_per_day" label="Цена/сутки" type="number" />
          <v-text-field v-model="form.phone" label="Телефон" />
          <v-switch v-model="form.is_available" label="Свободен" />
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

const rooms = ref([]);
const loading = ref(false);
const saving = ref(false);
const error = ref("");

const headers = [
  { title: "Номер", key: "number" },
  { title: "Этаж", key: "floor" },
  { title: "Тип", key: "room_type" },
  { title: "Цена", key: "price_per_day" },
  { title: "Телефон", key: "phone" },
  { title: "Статус", key: "is_available" },
  { title: "Действия", key: "actions", sortable: false },
];

const dialog = ref(false);
const form = ref({
  id: null,
  number: "",
  floor: 1,
  room_type: "single",
  price_per_day: 0,
  phone: "",
  is_available: true,
});

function openCreate() {
  form.value = { id: null, number: "", floor: 1, room_type: "single", price_per_day: 0, phone: "", is_available: true };
  dialog.value = true;
}

function openEdit(item) {
  form.value = { ...item };
  dialog.value = true;
}

async function loadAll() {
  error.value = "";
  loading.value = true;
  try {
    const res = await http.get(EP.rooms);
    rooms.value = res.data;
  } catch (e) {
    error.value = "Не удалось загрузить номера";
  } finally {
    loading.value = false;
  }
}

async function loadAvailable() {
  error.value = "";
  loading.value = true;
  try {
    const res = await http.get(EP.roomsAvailable);
    rooms.value = res.data.rooms || res.data; // если backend возвращает {count, rooms}
  } catch (e) {
    error.value = "Не удалось загрузить свободные номера";
  } finally {
    loading.value = false;
  }
}

async function save() {
  saving.value = true;
  error.value = "";
  try {
    if (form.value.id) {
      await http.put(`${EP.rooms}${form.value.id}/`, form.value);
    } else {
      await http.post(EP.rooms, form.value);
    }
    dialog.value = false;
    await loadAll();
  } catch (e) {
    error.value = "Ошибка сохранения";
  } finally {
    saving.value = false;
  }
}

async function remove(item) {
  if (!confirm("Удалить номер?")) return;
  error.value = "";
  try {
    await http.delete(`${EP.rooms}${item.id}/`);
    await loadAll();
  } catch (e) {
    error.value = "Ошибка удаления";
  }
}

onMounted(loadAll);
</script>
