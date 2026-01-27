<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Блюда</span>
            <v-btn color="primary" @click="openDialog()">
              <v-icon left>mdi-plus</v-icon>
              Добавить блюдо
            </v-btn>
          </v-card-title>

          <v-data-table :headers="headers" :items="dishes" :loading="loading" class="elevation-1">
            <template v-slot:[`item.calculated_price`]="{ item }">
              {{ item.calculated_price?.toFixed(2) }} ₽
            </template>

            <template v-slot:[`item.actions`]="{ item }">
              <v-btn icon small @click="openDialog(item)" class="mr-2">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn icon small @click="deleteDish(item.id)">
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
          {{ editedIndex === -1 ? "Новое блюдо" : "Редактировать блюдо" }}
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="editedItem.name"
              label="Название блюда"
              :rules="[(v) => !!v || 'Поле обязательно']"
              required
            ></v-text-field>

            <v-select
              v-model="editedItem.dish_type"
              :items="dishTypeOptions"
              label="Тип блюда"
              :rules="[(v) => !!v || 'Поле обязательно']"
              required
            ></v-select>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="saveDish" :disabled="!valid">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { restaurantAPI } from "@/services/api";

const dishes = ref([]);
const loading = ref(false);
const dialog = ref(false);
const valid = ref(false);
const editedIndex = ref(-1);

const editedItem = ref({
  name: "",
  dish_type: "",
});

const defaultItem = {
  name: "",
  dish_type: "",
};

const headers = [
  { title: "Название", key: "name" },
  { title: "Тип блюда", key: "dish_type_display" },
  { title: "Цена", key: "calculated_price" },
  { title: "Действия", key: "actions", sortable: false },
];

const dishTypeOptions = [
  { title: "Закуска", value: "appetizer" },
  { title: "Суп", value: "soup" },
  { title: "Основное блюдо", value: "main" },
  { title: "Десерт", value: "dessert" },
  { title: "Напиток", value: "drink" },
];

const fetchDishes = async () => {
  loading.value = true;
  try {
    const response = await restaurantAPI.getDishes();
    dishes.value = response.data.results || response.data;
  } catch (error) {
    console.error("Error fetching dishes:", error);
  }
  loading.value = false;
};

const openDialog = (item = null) => {
  if (item) {
    editedIndex.value = dishes.value.indexOf(item);
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

const saveDish = async () => {
  try {
    if (editedIndex.value > -1) {
      await restaurantAPI.updateDish(editedItem.value.id, editedItem.value);
    } else {
      await restaurantAPI.createDish(editedItem.value);
    }
    await fetchDishes();
    closeDialog();
  } catch (error) {
    console.error("Error saving dish:", error);
  }
};

const deleteDish = async (id) => {
  if (confirm("Вы уверены, что хотите удалить это блюдо?")) {
    try {
      await restaurantAPI.deleteDish(id);
      await fetchDishes();
    } catch (error) {
      console.error("Error deleting dish:", error);
    }
  }
};

onMounted(() => {
  fetchDishes();
});
</script>
