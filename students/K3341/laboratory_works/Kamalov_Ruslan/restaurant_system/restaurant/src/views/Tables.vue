<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Столы</span>
            <v-btn color="primary" @click="openDialog()">
              <v-icon left>mdi-plus</v-icon>
              Добавить стол
            </v-btn>
          </v-card-title>

          <v-data-table :headers="headers" :items="tables" :loading="loading" class="elevation-1">
            <template v-slot:[`item.status`]="{ item }">
              <v-chip :color="item.status === 'free' ? 'green' : 'red'" text-color="white" small>
                {{ item.status_display }}
              </v-chip>
            </template>

            <template v-slot:[`item.actions`]="{ item }">
              <v-btn icon small @click="toggleTableStatus(item)" class="mr-2">
                <v-icon>{{ item.status === "free" ? "mdi-lock" : "mdi-lock-open" }}</v-icon>
              </v-btn>
              <v-btn icon small @click="openDialog(item)" class="mr-2">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn icon small @click="deleteTable(item.id)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          {{ editedIndex === -1 ? "Новый стол" : "Редактировать стол" }}
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="editedItem.table_number"
              label="Номер стола"
              type="number"
              :rules="[(v) => !!v || 'Поле обязательно', (v) => v > 0 || 'Должно быть больше 0']"
              required
            ></v-text-field>

            <v-text-field
              v-model="editedItem.capacity"
              label="Вместимость"
              type="number"
              :rules="[(v) => !!v || 'Поле обязательно', (v) => v > 0 || 'Должно быть больше 0']"
              required
            ></v-text-field>

            <v-select
              v-model="editedItem.status"
              :items="statusOptions"
              label="Статус"
              :rules="[(v) => !!v || 'Поле обязательно']"
              required
            ></v-select>

            <v-select
              v-model="editedItem.employee"
              :items="waiters"
              item-title="full_name"
              item-value="id"
              label="Обслуживающий официант"
              clearable
            ></v-select>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="saveTable" :disabled="!valid">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { restaurantAPI } from "@/services/api";

const tables = ref([]);
const waiters = ref([]);
const loading = ref(false);
const dialog = ref(false);
const valid = ref(false);
const editedIndex = ref(-1);

const editedItem = ref({
  table_number: 0,
  capacity: 0,
  status: "free",
  employee: null,
});

const defaultItem = {
  table_number: 0,
  capacity: 0,
  status: "free",
  employee: null,
};

const headers = [
  { title: "Номер стола", key: "table_number" },
  { title: "Вместимость", key: "capacity" },
  { title: "Статус", key: "status" },
  { title: "Официант", key: "waiter_name" },
  { title: "Действия", key: "actions", sortable: false },
];

const statusOptions = [
  { title: "Свободен", value: "free" },
  { title: "Занят", value: "occupied" },
];

const fetchTables = async () => {
  loading.value = true;
  try {
    const response = await restaurantAPI.getTables();
    tables.value = response.data.results || response.data;
  } catch (error) {
    console.error("Error fetching tables:", error);
  }
  loading.value = false;
};

const fetchWaiters = async () => {
  try {
    const response = await restaurantAPI.getEmployees();
    const employees = response.data.results || response.data;
    waiters.value = employees.filter((emp) => emp.category === "waiter");
  } catch (error) {
    console.error("Error fetching waiters:", error);
  }
};

const toggleTableStatus = async (table) => {
  const newStatus = table.status === "free" ? "occupied" : "free";
  try {
    await restaurantAPI.updateTableStatus(table.id, newStatus);
    await fetchTables();
  } catch (error) {
    console.error("Error updating table status:", error);
  }
};

const openDialog = (item = null) => {
  if (item) {
    editedIndex.value = tables.value.indexOf(item);
    editedItem.value = { ...item };
  } else {
    editedIndex.value = -1;
    editedItem.value = { ...defaultItem };
  }
  dialog.value = true;
};

const closeDialog = () => {
  dialog.value = false;
  editedItem.value = { ...defaultItem };
  editedIndex.value = -1;
};

const saveTable = async () => {
  try {
    if (editedIndex.value > -1) {
      await restaurantAPI.updateTable(editedItem.value.id, editedItem.value);
    } else {
      await restaurantAPI.createTable(editedItem.value);
    }
    await fetchTables();
    closeDialog();
  } catch (error) {
    console.error("Error saving table:", error);
  }
};

const deleteTable = async (id) => {
  if (confirm("Вы уверены, что хотите удалить этот стол?")) {
    try {
      await restaurantAPI.deleteTable(id);
      await fetchTables();
    } catch (error) {
      console.error("Error deleting table:", error);
    }
  }
};

onMounted(() => {
  fetchTables();
  fetchWaiters();
});
</script>
