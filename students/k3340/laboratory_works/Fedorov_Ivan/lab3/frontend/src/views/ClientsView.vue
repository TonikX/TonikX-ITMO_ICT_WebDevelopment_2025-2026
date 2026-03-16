<template>
  <v-container>
    <div class="d-flex align-center mb-4">
      <h2 class="mr-4">Клиенты</h2>
      <v-spacer />
      <v-btn color="primary" @click="openCreate">Заселить</v-btn>
    </div>

    <v-alert v-if="error" type="error" class="mb-3">{{ error }}</v-alert>

    <v-data-table :headers="headers" :items="clients" :loading="loading">
      <template #item.actions="{ item }">
        <v-btn size="small" variant="text" color="red" @click="openCheckout(item)">
          выселить
        </v-btn>
      </template>
    </v-data-table>

    <!-- create client -->
    <v-dialog v-model="dialog" max-width="560">
      <v-card>
        <v-card-title>Заселение клиента</v-card-title>
        <v-card-text>
          <v-text-field v-model="form.passport" label="Паспорт" />
          <v-text-field v-model="form.last_name" label="Фамилия" />
          <v-text-field v-model="form.first_name" label="Имя" />
          <v-text-field v-model="form.middle_name" label="Отчество" />
          <v-text-field v-model="form.city" label="Город" />
          <v-text-field v-model="form.check_in_date" label="Дата заселения (YYYY-MM-DD)" />
          <v-text-field v-model="form.check_out_date" label="Дата выселения (опц.)" />

          <v-text-field v-model.number="form.room" label="ID комнаты (room)" type="number" />
          <small class="text-grey">room — это ID комнаты, как в твоём Postman</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="dialog=false">Отмена</v-btn>
          <v-btn color="primary" :loading="saving" @click="createClient">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- checkout -->
    <v-dialog v-model="checkoutDialog" max-width="420">
      <v-card>
        <v-card-title>Выселение клиента</v-card-title>
        <v-card-text>
          <div class="mb-2">
            {{ checkoutClient?.last_name }} {{ checkoutClient?.first_name }} (id={{ checkoutClient?.id }})
          </div>
          <v-text-field v-model="checkoutDate" label="Дата выселения (YYYY-MM-DD)" />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="checkoutDialog=false">Отмена</v-btn>
          <v-btn color="red" :loading="saving" @click="checkOut">Выселить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import http from "../services/http";
import { EP } from "../services/endpoints";

const clients = ref([]);
const loading = ref(false);
const saving = ref(false);
const error = ref("");

const headers = [
  { title: "ID", key: "id" },
  { title: "Фамилия", key: "last_name" },
  { title: "Имя", key: "first_name" },
  { title: "Паспорт", key: "passport" },
  { title: "Город", key: "city" },
  { title: "Заселение", key: "check_in_date" },
  { title: "Выселение", key: "check_out_date" },
  { title: "Room", key: "room" },
  { title: "Действия", key: "actions", sortable: false },
];

const dialog = ref(false);
const form = ref({
  passport: "",
  last_name: "",
  first_name: "",
  middle_name: "",
  city: "",
  check_in_date: "",
  check_out_date: null,
  room: null,
});

function openCreate() {
  form.value = {
    passport: "",
    last_name: "",
    first_name: "",
    middle_name: "",
    city: "",
    check_in_date: "",
    check_out_date: null,
    room: null,
  };
  dialog.value = true;
}

async function loadClients() {
  error.value = "";
  loading.value = true;
  try {
    const res = await http.get(EP.clients);
    clients.value = res.data;
  } catch (e) {
    error.value = "Не удалось загрузить клиентов";
  } finally {
    loading.value = false;
  }
}

async function createClient() {
  saving.value = true;
  error.value = "";
  try {
    await http.post(EP.clients, form.value);
    dialog.value = false;
    await loadClients();
  } catch (e) {
    error.value = "Ошибка создания клиента (проверь room id и поля)";
  } finally {
    saving.value = false;
  }
}

const checkoutDialog = ref(false);
const checkoutClient = ref(null);
const checkoutDate = ref("");

function openCheckout(item) {
  checkoutClient.value = item;
  checkoutDate.value = "";
  checkoutDialog.value = true;
}

async function checkOut() {
  saving.value = true;
  error.value = "";
  try {
    await http.post(`${EP.clients}${checkoutClient.value.id}/check_out/`, {
      check_out_date: checkoutDate.value,
    });
    checkoutDialog.value = false;
    await loadClients();
  } catch (e) {
    error.value = "Ошибка выселения";
  } finally {
    saving.value = false;
  }
}

onMounted(loadClients);
</script>
