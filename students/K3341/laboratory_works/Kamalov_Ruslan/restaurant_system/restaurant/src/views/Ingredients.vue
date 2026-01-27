<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Ингредиенты</span>
            <div>
              <v-btn color="warning" @click="fetchLowStock" class="mr-2">
                <v-icon left>mdi-alert</v-icon>
                Низкий запас
              </v-btn>
              <v-btn color="primary" @click="openDialog()">
                <v-icon left>mdi-plus</v-icon>
                Добавить ингредиент
              </v-btn>
            </div>
          </v-card-title>

          <v-data-table
            :headers="headers"
            :items="ingredients"
            :loading="loading"
            class="elevation-1"
          >
            <template #item.is_low_stock="{ item }">
              <v-chip :color="item.is_low_stock ? 'red' : 'green'" text-color="white" small>
                {{ item.is_low_stock ? "Низкий" : "Норма" }}
              </v-chip>
            </template>

            <template #item.actions="{ item }">
              <v-btn icon small @click="openDialog(item)" class="mr-2">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn icon small @click="deleteIngredient(item.id)">
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
          {{ editedIndex === -1 ? "Новый ингредиент" : "Редактировать ингредиент" }}
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="editedItem.name"
              label="Наименование"
              :rules="[(v) => !!v || 'Поле обязательно']"
              required
            ></v-text-field>

            <v-text-field
              v-model="editedItem.stock_quantity"
              label="Количество на складе"
              type="number"
              :rules="[
                (v) => !!v || 'Поле обязательно',
                (v) => v >= 0 || 'Должно быть больше или равно 0',
              ]"
              required
            ></v-text-field>

            <v-text-field
              v-model="editedItem.minimum_stock"
              label="Необходимый запас"
              type="number"
              :rules="[
                (v) => !!v || 'Поле обязательно',
                (v) => v >= 0 || 'Должно быть больше или равно 0',
              ]"
              required
            ></v-text-field>

            <v-text-field
              v-model="editedItem.price_per_unit"
              label="Цена за единицу"
              type="number"
              step="0.01"
              :rules="[(v) => !!v || 'Поле обязательно', (v) => v > 0 || 'Должно быть больше 0']"
              required
            ></v-text-field>

            <v-text-field
              v-model="editedItem.supplier"
              label="Поставщик"
              :rules="[(v) => !!v || 'Поле обязательно']"
              required
            ></v-text-field>

            <v-select
              v-model="editedItem.ingredient_type"
              :items="typeOptions"
              label="Тип ингредиента"
              :rules="[(v) => !!v || 'Поле обязательно']"
              required
            ></v-select>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="saveIngredient" :disabled="!valid">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { restaurantAPI } from "@/services/api";

const ingredients = ref([]);
const loading = ref(false);
const dialog = ref(false);
const valid = ref(false);
const editedIndex = ref(-1);

const editedItem = ref({
  name: "",
  stock_quantity: 0,
  minimum_stock: 0,
  price_per_unit: 0,
  supplier: "",
  ingredient_type: "",
});

const defaultItem = {
  name: "",
  stock_quantity: 0,
  minimum_stock: 0,
  price_per_unit: 0,
  supplier: "",
  ingredient_type: "",
};

const headers = [
  { title: "Наименование", key: "name" },
  { title: "Количество", key: "stock_quantity" },
  { title: "Мин. запас", key: "minimum_stock" },
  { title: "Цена", key: "price_per_unit" },
  { title: "Поставщик", key: "supplier" },
  { title: "Тип", key: "ingredient_type_display" },
  { title: "Статус", key: "is_low_stock" },
  { title: "Действия", key: "actions", sortable: false },
];

const typeOptions = [
  { title: "Мясо", value: "meat" },
  { title: "Овощи", value: "vegetable" },
  { title: "Молочные продукты", value: "dairy" },
  { title: "Специи", value: "spice" },
  { title: "Другое", value: "other" },
];

const fetchIngredients = async () => {
  loading.value = true;
  try {
    const response = await restaurantAPI.getIngredients();
    ingredients.value = response.data.results || response.data;
  } catch (error) {
    console.error("Error fetching ingredients:", error);
  }
  loading.value = false;
};

const fetchLowStock = async () => {
  loading.value = true;
  try {
    const response = await restaurantAPI.getLowStockIngredients();
    ingredients.value = response.data;
  } catch (error) {
    console.error("Error fetching low stock ingredients:", error);
  }
  loading.value = false;
};

const openDialog = (item = null) => {
  if (item) {
    editedIndex.value = ingredients.value.indexOf(item);
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

const saveIngredient = async () => {
  try {
    if (editedIndex.value > -1) {
      await restaurantAPI.updateIngredient(editedItem.value.id, editedItem.value);
    } else {
      await restaurantAPI.createIngredient(editedItem.value);
    }
    await fetchIngredients();
    closeDialog();
  } catch (error) {
    console.error("Error saving ingredient:", error);
  }
};

const deleteIngredient = async (id) => {
  if (confirm("Вы уверены, что хотите удалить этот ингредиент?")) {
    try {
      await restaurantAPI.deleteIngredient(id);
      await fetchIngredients();
    } catch (error) {
      console.error("Error deleting ingredient:", error);
    }
  }
};

onMounted(() => {
  fetchIngredients();
});
</script>
