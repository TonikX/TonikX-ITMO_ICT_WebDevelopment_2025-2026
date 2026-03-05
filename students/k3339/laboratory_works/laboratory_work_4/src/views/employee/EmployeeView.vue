<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import EmployeeList from "@/components/employee/EmployeeList.vue";
import EmployeeModal from "@/components/employee/EmployeeModal.vue";

const employees = ref([]);
const isLoading = ref(false);
const isError = ref(false);
const isAddModalVisible = ref(false);

async function fetchEmployees() {
  isLoading.value = true;
  await axios
      .get('manufactory/employees')
      .then(response => {
        employees.value = response.data;
      })
      .catch(error => {
        console.error("Ошибка загрузки сотрудников", error);
        isError.value = true;
      })
      .finally(() => {
        isLoading.value = false;
      });
}

async function addEmployee(employee) {
  await axios.post(`manufactory/employees/`, employee).then(fetchEmployees).catch(error => {
    isError.value = true;
    console.error(`Ошибка добавления сотрудника: ${error}`);
  })
}

async function deleteEmployee(id) {
  await axios.delete(`manufactory/employees/${id}/`).then(() => {
    employees.value = employees.value.filter(item => item.id !== id);
  }).catch(error => {
    isError.value = true;
    console.error(`Ошибка удаления сотрудника: ${error}`);
  })
}

async function updateEmployee(employee) {
  await axios.put(`manufactory/employees/${employee.id}/`, employee).then(fetchEmployees).catch(error => {
    isError.value = true;
    console.error(`Ошибка обновления сотрудника: ${error}`);
  })
}

onMounted(fetchEmployees);

</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <template v-if="isLoading">
      <v-skeleton-loader
          type="card"
          class="mt-4"
          max-width="500"
      ></v-skeleton-loader>
    </template>
    <template v-else>
      <h2>Список сотрудников</h2>
      <v-btn color="primary" @click="isAddModalVisible = true">Добавить сотрудника</v-btn>
      <EmployeeList :employees="employees" @delete-employee="deleteEmployee" @update-employee="updateEmployee"/>
      <EmployeeModal
          v-model="isAddModalVisible"
          mode="add"
          @submit-employee="addEmployee"
      />
    </template>
  </div>
</template>

<style scoped>
.info {
  flex-grow: 1;
  margin-right: 10px;
}

.actions {
  display: flex;
  gap: 5px;
}

.actions > .v-btn {
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}
</style>
