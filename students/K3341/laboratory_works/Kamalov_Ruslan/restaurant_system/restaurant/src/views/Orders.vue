<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Заказы</span>
            <div>
              <v-select
                v-model="selectedStatus"
                :items="statusFilterOptions"
                label="Фильтр по статусу"
                @update:model-value="filterByStatus"
                class="mr-2"
                style="width: 200px; display: inline-block"
              ></v-select>
              <v-btn color="primary" @click="openDialog()">
                <v-icon left>mdi-plus</v-icon>
                Новый заказ
              </v-btn>
            </div>
          </v-card-title>

          <v-data-table :headers="headers" :items="orders" :loading="loading" class="elevation-1">
            <template v-slot:[`item.status`]="{ item }">
              <v-chip :color="getStatusColor(item.status)" text-color="white" small>
                {{ item.status_display }}
              </v-chip>
            </template>

            <template v-slot:[`item.total_price`]="{ item }">
              {{ item.total_price?.toFixed(2) }} ₽
            </template>

            <template v-slot:[`item.actions`]="{ item }">
              <v-menu>
                <template v-slot:activator="{ props }">
                  <v-btn icon small v-bind="props" class="mr-2">
                    <v-icon>mdi-cog</v-icon>
                  </v-btn>
                </template>
                <v-list>
                  <v-list-item
                    v-for="status in statusOptions"
                    :key="status.value"
                    @click="updateOrderStatus(item.id, status.value)"
                  >
                    <v-list-item-title>{{ status.title }}</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
              <v-btn icon small @click="deleteOrder(item.id)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="800px">
      <v-card>
        <v-card-title> Новый заказ </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-select
              v-model="editedItem.table"
              :items="freeTables"
              item-title="table_number"
              item-value="id"
              label="Стол"
              :rules="[(v) => !!v || 'Поле обязательно']"
              required
            ></v-select>

            <v-textarea v-model="editedItem.comments" label="Комментарии" rows="3"></v-textarea>

            <v-divider class="my-4"></v-divider>

            <h3>Блюда в заказе</h3>
            <div v-for="(detail, index) in editedItem.order_details" :key="index" class="mb-3">
              <v-row>
                <v-col cols="6">
                  <v-select
                    v-model="detail.dish"
                    :items="dishes"
                    item-title="name"
                    item-value="id"
                    label="Блюдо"
                    required
                  ></v-select>
                </v-col>
                <v-col cols="3">
                  <v-text-field
                    v-model="detail.quantity"
                    label="Количество"
                    type="number"
                    min="1"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="2">
                  <v-btn icon @click="removeOrderDetail(index)">
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </v-col>
              </v-row>
              <v-text-field
                v-model="detail.special_requests"
                label="Особые пожелания"
                dense
              ></v-text-field>
            </div>

            <v-btn @click="addOrderDetail" color="secondary" small>
              <v-icon left>mdi-plus</v-icon>
              Добавить блюдо
            </v-btn>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog">Отмена</v-btn>
          <v-btn
            color="primary"
            @click="saveOrder"
            :disabled="!valid || editedItem.order_details.length === 0"
            >Сохранить</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { restaurantAPI } from "@/services/api";

const orders = ref([]);
const dishes = ref([]);
const freeTables = ref([]);
const loading = ref(false);
const dialog = ref(false);
const valid = ref(false);
const selectedStatus = ref("all");

const editedItem = ref({
  table: null,
  comments: "",
  order_details: [],
});

const defaultItem = {
  table: null,
  comments: "",
  order_details: [],
};

const headers = [
  { title: "ID", key: "id" },
  { title: "Стол", key: "table_number" },
  { title: "Дата", key: "order_date" },
  { title: "Статус", key: "status" },
  { title: "Сумма", key: "total_price" },
  { title: "Действия", key: "actions", sortable: false },
];

const statusOptions = [
  { title: "Принят", value: "received" },
  { title: "Готовится", value: "cooking" },
  { title: "Готов", value: "ready" },
  { title: "Выдан", value: "served" },
  { title: "Оплачен", value: "paid" },
];

const statusFilterOptions = [{ title: "Все", value: "all" }, ...statusOptions];

const getStatusColor = (status) => {
  const colors = {
    received: "blue",
    cooking: "orange",
    ready: "green",
    served: "purple",
    paid: "grey",
  };
  return colors[status] || "grey";
};

const fetchOrders = async () => {
  loading.value = true;
  try {
    const response = await restaurantAPI.getOrders();
    orders.value = response.data.results || response.data;
  } catch (error) {
    console.error("Error fetching orders:", error);
  }
  loading.value = false;
};

const fetchDishes = async () => {
  try {
    const response = await restaurantAPI.getDishes();
    dishes.value = response.data.results || response.data;
  } catch (error) {
    console.error("Error fetching dishes:", error);
  }
};

const fetchFreeTables = async () => {
  try {
    const response = await restaurantAPI.getTables();
    const tables = response.data.results || response.data;
    freeTables.value = tables.filter((table) => table.status === "free");
  } catch (error) {
    console.error("Error fetching tables:", error);
  }
};

const filterByStatus = async () => {
  if (selectedStatus.value === "all") {
    await fetchOrders();
  } else {
    loading.value = true;
    try {
      const response = await restaurantAPI.getOrdersByStatus(selectedStatus.value);
      orders.value = response.data;
    } catch (error) {
      console.error("Error filtering orders:", error);
    }
    loading.value = false;
  }
};

const updateOrderStatus = async (orderId, newStatus) => {
  try {
    await restaurantAPI.updateOrderStatus(orderId, newStatus);
    await fetchOrders();
  } catch (error) {
    console.error("Error updating order status:", error);
  }
};

const openDialog = () => {
  editedItem.value = { ...defaultItem, order_details: [] };
  dialog.value = true;
};

const closeDialog = () => {
  dialog.value = false;
  editedItem.value = { ...defaultItem };
};

const addOrderDetail = () => {
  editedItem.value.order_details.push({
    dish: null,
    quantity: 1,
    special_requests: "",
  });
};

const removeOrderDetail = (index) => {
  editedItem.value.order_details.splice(index, 1);
};

const saveOrder = async () => {
  try {
    await restaurantAPI.createOrder(editedItem.value);
    await fetchOrders();
    closeDialog();
  } catch (error) {
    console.error("Error saving order:", error);
  }
};

const deleteOrder = async (id) => {
  if (confirm("Вы уверены, что хотите удалить этот заказ?")) {
    try {
      await restaurantAPI.deleteOrder(id);
      await fetchOrders();
    } catch (error) {
      console.error("Error deleting order:", error);
    }
  }
};

onMounted(() => {
  fetchOrders();
  fetchDishes();
  fetchFreeTables();
});
</script>
