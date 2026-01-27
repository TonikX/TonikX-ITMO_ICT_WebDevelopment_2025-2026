<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Должности</span>
            <v-btn color="primary" @click="openDialog()">
              <v-icon left>mdi-plus</v-icon>
              Добавить должность
            </v-btn>
          </v-card-title>

          <v-data-table
            :headers="headers"
            :items="positions"
            :loading="loading"
            class="elevation-1"
          >
            <template v-slot:[`item.actions`]="{ item }">
              <v-btn icon small @click="openDialog(item)" class="mr-2">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn icon small @click="deletePosition(item.id)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          {{ editedIndex === -1 ? "Новая должность" : "Редактировать должность" }}
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="editedItem.position"
              label="Название должности"
              :rules="[(v) => !!v || 'Поле обязательно']"
              required
            ></v-text-field>

            <v-text-field
              v-model="editedItem.minimum_wage"
              label="Минимальная зарплата"
              type="number"
              step="0.01"
              :rules="[(v) => !!v || 'Поле обязательно', (v) => v > 0 || 'Должно быть больше 0']"
              required
            ></v-text-field>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="savePosition" :disabled="!valid">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { restaurantAPI } from "@/services/api";

const positions = ref([]);
const loading = ref(false);
const dialog = ref(false);
const valid = ref(false);
const editedIndex = ref(-1);

const editedItem = ref({
  position: "",
  minimum_wage: 0,
});

const defaultItem = {
  position: "",
  minimum_wage: 0,
};

const headers = [
  { title: "Название должности", key: "position" },
  { title: "Минимальная зарплата", key: "minimum_wage" },
  { title: "Действия", key: "actions", sortable: false },
];

const fetchPositions = async () => {
  loading.value = true;
  try {
    const response = await restaurantAPI.getPositions();
    positions.value = response.data.results || response.data;
  } catch (error) {
    console.error("Error fetching positions:", error);
  }
  loading.value = false;
};

const openDialog = (item = null) => {
  if (item) {
    editedIndex.value = positions.value.indexOf(item);
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

const savePosition = async () => {
  try {
    if (editedIndex.value > -1) {
      await restaurantAPI.updatePosition(editedItem.value.id, editedItem.value);
    } else {
      await restaurantAPI.createPosition(editedItem.value);
    }
    await fetchPositions();
    closeDialog();
  } catch (error) {
    console.error("Error saving position:", error);
  }
};

const deletePosition = async (id) => {
  if (confirm("Вы уверены, что хотите удалить эту должность?")) {
    try {
      await restaurantAPI.deletePosition(id);
      await fetchPositions();
    } catch (error) {
      console.error("Error deleting position:", error);
    }
  }
};

onMounted(() => {
  fetchPositions();
});
</script>
