<template>
  <v-container class="mt-6">
    <div class="d-flex justify-space-between align-center mb-4">
      <h2>Смены</h2>

      <div>
        <v-btn color="primary" class="mr-2" @click="loadData">
          Обновить
        </v-btn>

        <v-btn
          v-if="isAdmin"
          color="secondary"
          @click="openCreateDialog"
        >
          Добавить смену
        </v-btn>
      </div>
    </div>

    <v-data-table
      :items="shifts"
      :headers="headersToShow"
      :loading="loading"
      loading-text="Загрузка..."
      class="elevation-1"
    >
      <template #item.driver="{ item }">
        {{ driverName(item.driver) }}
      </template>

      <template #item.bus="{ item }">
        {{ busLabel(item.bus) }}
      </template>

      <template #item.route="{ item }">
        {{ routeLabel(item.route) }}
      </template>

      <template #item.status="{ item }">
        <v-chip :color="statusColor(item.status)" size="small">
          {{ statusLabel(item.status) }}
        </v-chip>
      </template>

      <template #item.actions="{ item }">
        <div v-if="isAdmin" class="d-flex ga-2">
          <v-btn
            size="small"
            variant="outlined"
            color="#929292"
            @click="openEditDialog(item)"
          >
            Изменить
          </v-btn>
          <v-btn
            size="small"
            variant="outlined"
            color="error"
            @click="deleteShift(item)"
          >
            Удалить
          </v-btn>
        </div>
      </template>
    </v-data-table>

    <!-- Диалог создания / редактирования смены -->
    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title>
          {{ editedShift.id ? 'Редактирование смены' : 'Новая смена' }}
        </v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field
              v-model="editedShift.date"
              label="Дата (ГГГГ-ММ-ДД)"
              required
            />
            <v-text-field
              v-model="editedShift.start_time"
              label="Время начала (ЧЧ:ММ)"
              required
            />
            <v-text-field
              v-model="editedShift.end_time"
              label="Время окончания (ЧЧ:ММ)"
              required
            />

            <v-select
              v-model="editedShift.driver"
              :items="drivers"
              item-title="full_name"
              item-value="id"
              label="Водитель"
              required
            />

            <v-select
              v-model="editedShift.bus"
              :items="buses"
              item-title="reg_number"
              item-value="id"
              label="Автобус"
              required
            />

            <v-select
              v-model="editedShift.route"
              :items="routes"
              :item-title="routeTitle"
              item-value="id"
              label="Маршрут"
              required
            />

            <v-select
              v-model="editedShift.status"
              :items="statusOptions"
              item-title="label"
              item-value="value"
              label="Статус"
              required
            />

            <v-text-field
              v-model="editedShift.reason"
              label="Причина (если не вышел)"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="saveShift">
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import http from "../api/http";

const shifts = ref([]);
const drivers = ref([]);
const buses = ref([]);
const routes = ref([]);

const loading = ref(false);
const isAdmin = ref(false);

const dialog = ref(false);
const editedShift = ref({});

const statusMap = {
  ON_LINE: "Вышел на линию",
  BROKEN: "Поломка",
  NO_DRIVER: "Нет водителя",
  OTHER: "Другая причина",
};

const statusOptions = [
  { value: "ON_LINE", label: "Вышел на линию" },
  { value: "BROKEN", label: "Поломка" },
  { value: "NO_DRIVER", label: "Нет водителя" },
  { value: "OTHER", label: "Другая причина" },
];

const baseHeaders = [
  { title: "Дата", value: "date" },
  { title: "Начало", value: "start_time" },
  { title: "Окончание", value: "end_time" },
  { title: "Водитель", value: "driver" },
  { title: "Автобус", value: "bus" },
  { title: "Маршрут", value: "route" },
  { title: "Статус", value: "status" },
  { title: "Причина", value: "reason" },
];

const headersToShow = computed(() => {
  if (isAdmin.value) {
    return [...baseHeaders, { title: "Действия", value: "actions", sortable: false }];
  }
  return baseHeaders;
});

const loadData = async () => {
  loading.value = true;
  try {
    // кто мы
    try {
      const meRes = await http.get("/api/me/");
      isAdmin.value = !!meRes.data.is_staff;
    } catch {
      isAdmin.value = false;
    }

    const [shiftsRes, driversRes, busesRes, routesRes] = await Promise.all([
      http.get("/api/shifts/"),
      http.get("/api/drivers/"),
      http.get("/api/buses/"),
      http.get("/api/routes/"),
    ]);

    shifts.value = shiftsRes.data;
    drivers.value = driversRes.data;
    buses.value = busesRes.data;
    routes.value = routesRes.data;
  } catch (e) {
    console.error("Ошибка загрузки смен:", e);
  } finally {
    loading.value = false;
  }
};

const driverName = (id) => {
  const d = drivers.value.find((x) => x.id === id);
  return d ? d.full_name : `#${id}`;
};

const busLabel = (id) => {
  const b = buses.value.find((x) => x.id === id);
  return b ? b.reg_number : `#${id}`;
};

const routeTitle = (r) =>
  `${r.number}: ${r.start_point} → ${r.end_point}`;

const routeLabel = (id) => {
  const r = routes.value.find((x) => x.id === id);
  return r ? routeTitle(r) : `Маршрут #${id}`;
};

const statusLabel = (value) => statusMap[value] || value;

const statusColor = (value) => {
  switch (value) {
    case "ON_LINE":
      return "green";
    case "BROKEN":
      return "red";
    case "NO_DRIVER":
      return "orange";
    case "OTHER":
      return "blue-grey";
    default:
      return "grey";
  }
};

// диалог

const openCreateDialog = () => {
  editedShift.value = {
    date: "",
    start_time: "",
    end_time: "",
    driver: null,
    bus: null,
    route: null,
    status: "ON_LINE",
    reason: "",
  };
  dialog.value = true;
};

const openEditDialog = (item) => {
  editedShift.value = { ...item };
  dialog.value = true;
};

const closeDialog = () => {
  dialog.value = false;
};

const saveShift = async () => {
  const data = { ...editedShift.value };

  try {
    if (data.id) {
      await http.put(`/api/shifts/${data.id}/`, data);
    } else {
      await http.post("/api/shifts/", data);
    }
    dialog.value = false;
    await loadData();
  } catch (e) {
    console.error("Ошибка сохранения смены:", e);
  }
};

const deleteShift = async (item) => {
  if (!confirm(`Удалить смену ${item.date} для водителя #${item.driver}?`)) return;
  try {
    await http.delete(`/api/shifts/${item.id}/`);
    await loadData();
  } catch (e) {
    console.error("Ошибка удаления смены:", e);
  }
};

onMounted(loadData);
</script>