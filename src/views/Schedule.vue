<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import ScheduleModal from "@/components/ScheduleModal.vue";
import { tokenStore } from "@/stores/token.js";

const tokenStorage = tokenStore();

// Состояния
const schedules = ref([]);
const employees = ref([]);
const floors = ref([]);
const isEditModalVisible = ref(false);
const selectedSchedule = ref({});

// Вспомогательная функция для формирования ФИО сотрудника
function formatFullName(employee) {
  if (!employee) return "";
  return `${employee.last_name} ${employee.first_name} ${employee.middle_name}`.trim();
}

// Функции для работы с API
async function fetchSchedules() {
  try {
    const response = await axios.get(`api/cleaning-schedules`, {
      headers: { Authorization: `Token ${tokenStorage.token}` },
    });
    const scheduleData = response.data;
    
    // Загружаем сотрудников для каждой записи расписания
    const employeeIds = [...new Set(scheduleData.map(schedule => schedule.employee))];
    const employeeResponse = await axios.get(`api/employees`, {
      headers: { Authorization: `Token ${tokenStorage.token}` },
    });
    
    // Индексируем сотрудников по id для быстрого доступа
    const employeeMap = employeeResponse.data.reduce((acc, employee) => {
      acc[employee.id] = employee;
      return acc;
    }, {});

    // Обновляем расписания с полным именем сотрудника
    schedules.value = scheduleData.map(schedule => ({
      ...schedule,
      employee_full_name: formatFullName(employeeMap[schedule.employee]),
      employee_obj: employeeMap[schedule.employee], // Сохраняем объект сотрудника для дальнейшего использования
    }));
  } catch (error) {
    console.error("Ошибка при загрузке расписаний:", error);
  }
}

async function fetchEmployees() {
  try {
    const response = await axios.get(`api/employees`, {
      headers: { Authorization: `Token ${tokenStorage.token}` },
    });
    employees.value = response.data;
  } catch (error) {
    console.error("Ошибка при загрузке сотрудников:", error);
  }
}

async function fetchFloors() {
  try {
    const response = await axios.get(`api/floors`, {
      headers: { Authorization: `Token ${tokenStorage.token}` },
    });
    floors.value = response.data;
  } catch (error) {
    console.error("Ошибка при загрузке этажей:", error);
  }
}

async function saveSchedule(schedule) {
  try {
    if (schedule.id) {
      // Обновление расписания
      await axios.put(`api/cleaning-schedules/${schedule.id}/`, schedule, {
        headers: { Authorization: `Token ${tokenStorage.token}` },
      });
    } else {
      // Создание нового расписания
      await axios.post(`api/cleaning-schedules/`, schedule, {
        headers: { Authorization: `Token ${tokenStorage.token}` },
      });
    }
    await fetchSchedules();
    isEditModalVisible.value = false;
  } catch (error) {
    console.error("Ошибка при сохранении расписания:", error);
  }
}

async function deleteSchedule(scheduleId) {
  try {
    await axios.delete(`api/cleaning-schedules/${scheduleId}/`, {
      headers: { Authorization: `Token ${tokenStorage.token}` },
    });
    await fetchSchedules();
  } catch (error) {
    console.error("Ошибка при удалении расписания:", error);
  }
}

// Обработчики
function handleCreate() {
  selectedSchedule.value = { employee: null, day_of_week: "", floor: "" };
  isEditModalVisible.value = true;
}

function handleEdit(schedule) {
  selectedSchedule.value = { ...schedule };
  isEditModalVisible.value = true;
}

function handleDelete(scheduleId) {
  if (confirm("Вы уверены, что хотите удалить это расписание?")) {
    deleteSchedule(scheduleId);
  }
}

function handleUpdate(schedule) {
  saveSchedule(schedule);
}

// Загрузка данных при монтировании
onMounted(() => {
  fetchSchedules();
  fetchEmployees();
  fetchFloors();
});
</script>

<template>
  <v-container class="fill-height" fluid>
    <!-- Таблица расписаний -->
    <v-data-table
      :headers="[
        { text: 'Сотрудник', value: 'employee_full_name' },
        { text: 'День недели', value: 'day_of_week' },
        { text: 'Этаж', value: 'floor' },
        { text: 'Действия', value: 'actions', sortable: false },
      ]"
      :items="schedules"
      class="elevation-1"
    >
      <template #item.actions="{ item }">
        <v-btn color="primary" @click="handleEdit(item)">Редактировать</v-btn>
        <v-btn color="error" @click="handleDelete(item.id)">Удалить</v-btn>
      </template>
    </v-data-table>

    <!-- Модальное окно для создания/редактирования расписания -->
    <ScheduleModal
      v-model="isEditModalVisible"
      :schedule="selectedSchedule"
      :employees="employees"
      :floors="floors"
      @save-schedule="handleUpdate"
    />

    <!-- Кнопка создания нового расписания, выравненная по центру внизу -->
    <v-row class="fill-height" align="center" justify="center">
      <v-col cols="auto">
        <v-btn color="primary" class="mb-4" @click="handleCreate">
          Создать расписание
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>
