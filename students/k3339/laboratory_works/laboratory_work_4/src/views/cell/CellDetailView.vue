<script setup>
import {onMounted, ref} from 'vue';
import axios from 'axios';
import {useRoute} from 'vue-router';
import CellEmployeeModal from "@/components/cell/CellEmployeeModal.vue";
import CellMoveModal from "@/components/cell/CellMoveModal.vue";

const route = useRoute();
const cells = ref([]);
const cellId = ref(null)
const cell = ref(null)
const availableEmployees = ref([]);
const responsibleEmployees = ref([]);
const showMoveModal = ref(false);
const showLinkModal = ref(false);
const selectedChicken = ref(null);
const isLoading = ref(true);
const isError = ref(false);
const chickensInCell = ref([]);
cellId.value = route.params.id;

async function fetchChickenInCell() {
  await axios
      .get(`/manufactory/chicken/`)
      .then(response => {
        chickensInCell.value = response.data.filter(chicken => chicken.cell.cell_code === cellId.value);
        console.log(cellId.value)
        console.log(chickensInCell.value)
      })
      .catch(error => {
        console.error("Ошибка загрузки куриц в клетке", error);
        isError.value = true;
      })
      .finally(() => {
        isLoading.value = false;
      })
}

async function fetchCells() {
  await axios
      .get('/manufactory/cells')
      .then(response => {
        cells.value = response.data;
        cell.value = response.data.find(cell => cell.cell_code === cellId.value);
        console.log(cell.value)
      })
      .catch(error => {
        console.error("Ошибка загрузки клеток", error);
        isError.value = true;
      })
}

async function fetchResponsibleEmployees() {
  await axios
      .get(`/manufactory/employees/cells`)
      .then(response => {
        responsibleEmployees.value = response.data.filter(responsibleEmployee => responsibleEmployee.cell === cellId.value)
      })
      .catch(error => {
        console.error("Ошибка загрузки сотрудников", error);
        isError.value = true;
      })
}

async function fetchAvailableEmployees() {
  await axios
      .get(`/manufactory/employees`)
      .then(response => {
        availableEmployees.value = response.data;
      })
      .catch(error => {
        console.error("Ошибка загрузки сотрудников", error);
        isError.value = true;
      })
}

async function assignEmployee(employee) {
  showLinkModal.value = false
  await axios
      .post(`/manufactory/employees/cells`, employee)
      .then(fetchResponsibleEmployees)
      .catch(error => {
        isError.value = true;
        console.error(`Ошибка привязки сотрудника: ${error}`)
      })
}

async function unassignEmployee(id) {
  await axios
      .delete(`/manufactory/employees/cells/${id}`)
      .then(fetchResponsibleEmployees)
      .catch(error => {
        isError.value = true;
        console.error(`Ошибка удаления сотрудника: ${error}`)
      })
}

async function moveChicken(chicken) {
  showMoveModal.value = false
  await axios
      .put(`/manufactory/chicken/${chicken.id}`, chicken)
      .then(fetchChickenInCell)
      .catch(error => {
        isError.value = true;
        console.error(`Ошибка переноса курицы: ${error}`)
      })
}

function handleMoveChickenClick(chicken) {
  showMoveModal.value = true
  selectedChicken.value = chicken
}


onMounted(() => {
  fetchCells();
  fetchChickenInCell();
  fetchResponsibleEmployees();
  fetchAvailableEmployees();
});
</script>

<template>
  <div v-if="cell" class="p-4">
    <h1 class="text-2xl font-bold mb-4">Клетка: {{ cell.cell_code }}</h1>
    <p><strong>Цех:</strong> {{ cell.workshop.title }}</p>
    <p><strong>Ряд:</strong> {{ cell.row }}</p>
    <p><strong>Место:</strong> {{ cell.column }}</p>

    <h2 class="text-xl font-bold mt-4">Ответственные сотрудники</h2>
    <v-btn @click="showLinkModal = true" class="btn">Привязать сотрудника</v-btn>
    <v-list v-if="responsibleEmployees" class="items-list">
      <v-list-item v-for="responsibleEmployee in responsibleEmployees" :key="responsibleEmployee.id">
        <v-list-item-title>{{ responsibleEmployee.employee.second_name }} {{ responsibleEmployee.employee.first_name }}
          {{ responsibleEmployee.employee.patronymic ?? "" }}
          <v-btn @click="unassignEmployee(responsibleEmployee.id)" class="btn ml-2">Отвязать сотрудника</v-btn>
        </v-list-item-title>
      </v-list-item>
    </v-list>

    <h2 class="text-xl font-bold mt-4">Курицы в клетке </h2>
    <v-list v-if="chickensInCell.length" class="items-list">
      <v-list-item v-for="chicken in chickensInCell" :key="chicken.id" class="chicken-item">
        <v-list-item-title class="font-medium text-lg">
          Курица номер {{ chicken.id }} ({{ chicken.breed.name }})
        </v-list-item-title>
        <v-btn @click="handleMoveChickenClick(chicken)" class="btn-action">Переместить</v-btn>
      </v-list-item>
    </v-list>
    <CellEmployeeModal
        v-model="showLinkModal"
        mode="add"
        :employees=availableEmployees
        :cell=cell
        @submit-employee="assignEmployee"
    />

    <CellMoveModal
        v-model="showMoveModal"
        :chicken-data="selectedChicken"
        :cells="cells"
        @submit-chicken="moveChicken"
    />


  </div>
</template>

<style scoped>
.btn {
  padding: 8px 12px;
  background-color: #007BFF;
  color: white;
  border-radius: 4px;
}

.btn-action {
  padding: 8px 12px;
  background-color: #28a745;
  color: white;
  border-radius: 4px;
  margin-right: 8px;
}

.btn-action:hover {
  background-color: #218838;
}

.items-list {
  background: white;
  border-radius: 8px;
  padding: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-top: 10px;
}

.chicken-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.chicken-item:last-child {
  border-bottom: none;
}
</style>

