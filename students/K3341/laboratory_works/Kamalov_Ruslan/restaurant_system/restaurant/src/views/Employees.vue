<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Сотрудники</span>
            <v-btn color="primary" @click="openDialog()">
              <v-icon left>mdi-plus</v-icon>
              Добавить сотрудника
            </v-btn>
          </v-card-title>

          <v-data-table
            :headers="headers"
            :items="employees"
            :loading="loading"
            class="elevation-1"
          >
            <template #item.actions="{ item }">
              <v-btn icon small @click="openDialog(item)" class="mr-2">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn icon small @click="deleteEmployee(item.id)">
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
          {{ editedIndex === -1 ? "Новый сотрудник" : "Редактировать сотрудника" }}
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="editedItem.full_name"
              label="ФИО"
              :rules="[(v) => !!v || 'Поле обязательно']"
              required
            ></v-text-field>

            <v-text-field
              v-model="editedItem.passport_data"
              label="Паспортные данные"
              :rules="[(v) => !!v || 'Поле обязательно']"
              required
            ></v-text-field>

            <v-select
              v-model="editedItem.category"
              :items="categoryOptions"
              label="Категория"
              :rules="[(v) => !!v || 'Поле обязательно']"
              required
            ></v-select>

            <v-select
              v-model="editedItem.position"
              :items="positions"
              item-title="position"
              item-value="id"
              label="Должность"
              :rules="[(v) => !!v || 'Поле обязательно']"
              required
            ></v-select>

            <v-text-field
              v-model="editedItem.salary"
              label="Оклад"
              type="number"
              :rules="[(v) => !!v || 'Поле обязательно', (v) => v > 0 || 'Должно быть больше 0']"
              required
            ></v-text-field>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="saveEmployee" :disabled="!valid">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { restaurantAPI } from "@/services/api";

const employees = ref([]);
const positions = ref([]);
const loading = ref(false);
const dialog = ref(false);
const valid = ref(false);
const editedIndex = ref(-1);

const editedItem = ref({
  full_name: "",
  passport_data: "",
  category: "",
  position: null,
  salary: 0,
});

const defaultItem = {
  full_name: "",
  passport_data: "",
  category: "",
  position: null,
  salary: 0,
};

const headers = [
  { title: "ФИО", key: "full_name" },
  { title: "Категория", key: "category_display" },
  { title: "Должность", key: "position_name" },
  { title: "Оклад", key: "salary" },
  { title: "Действия", key: "actions", sortable: false },
];

const categoryOptions = [
  { title: "Шеф-повар", value: "chef" },
  { title: "Повар", value: "cook" },
  { title: "Официант", value: "waiter" },
];

const fetchEmployees = async () => {
  loading.value = true;
  try {
    const response = await restaurantAPI.getEmployees();
    employees.value = response.data.results || response.data;
  } catch (error) {
    console.error("Error fetching employees:", error);
  }
  loading.value = false;
};

const fetchPositions = async () => {
  try {
    const response = await restaurantAPI.getPositions();
    positions.value = response.data.results || response.data;
  } catch (error) {
    console.error("Error fetching positions:", error);
  }
};

const openDialog = (item = null) => {
  if (item) {
    editedIndex.value = employees.value.indexOf(item);
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

const saveEmployee = async () => {
  try {
    if (editedIndex.value > -1) {
      await restaurantAPI.updateEmployee(editedItem.value.id, editedItem.value);
    } else {
      await restaurantAPI.createEmployee(editedItem.value);
    }
    await fetchEmployees();
    closeDialog();
  } catch (error) {
    console.error("Error saving employee:", error);
  }
};

const deleteEmployee = async (id) => {
  if (confirm("Вы уверены, что хотите удалить этого сотрудника?")) {
    try {
      await restaurantAPI.deleteEmployee(id);
      await fetchEmployees();
    } catch (error) {
      console.error("Error deleting employee:", error);
    }
  }
};

onMounted(() => {
  fetchEmployees();
  fetchPositions();
});
</script>
