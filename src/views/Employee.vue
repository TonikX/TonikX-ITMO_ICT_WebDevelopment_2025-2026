<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import {tokenStore} from "@/stores/token.js";
import EmployeeModal from "@/components/EmployeeModal.vue";
import EmployeeList from "@/components/EmployeeList.vue";

const token = tokenStore();
const employees = ref([]);
const isAddModalVisible = ref(false);
const isLoading = ref(true);

async function fetchEmployee() {
  await axios
      .get("api/employees/", {
        headers: {
          Authorization: `Token ${token.token}`,
        },
      })
      .then((response) => {
        if (response.status === 200) {
          employees.value = response.data;
          isLoading.value = false
        }
      })
      .catch((error) => {
        console.log(error);
      });
}

async function handleAddEmployee(employee) {
  await axios
      .post("api/employees/", employee, {
        headers: {
          Authorization: `Token ${token.token}`,
        },
      })
      .then(() => {
        fetchEmployee();
        isAddModalVisible.value = false;
      })
      .catch((error) => {
        console.log(error);
      });
}

async function deleteEmployee(id) {
  await axios
      .delete(`api/employees/${id}/`, {
        headers: {
          Authorization: `Token ${token.token}`,
        },
      })
      .then(() => {
        fetchEmployee();
      })
      .catch((error) => {
        console.log(error);
      });
}

onMounted(() => fetchEmployee());
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
      <h2>Сотрудники</h2>

      <EmployeeList :employees="employees" @delete-employee="deleteEmployee"/>

      <v-btn color="primary" @click="isAddModalVisible = true">Добавить Сотрудника</v-btn>
      <EmployeeModal
          v-model="isAddModalVisible"
          mode="add"
          @submit-employee="handleAddEmployee"
      />
    </template>
  </div>
</template>