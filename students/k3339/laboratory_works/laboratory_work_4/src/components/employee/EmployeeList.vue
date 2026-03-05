<script setup>

import EmployeeModal from "@/components/employee/EmployeeModal.vue";
import {ref} from "vue";

defineProps({
  employees: {
    type: Array
  }
})

const emits = defineEmits(["delete-employee", "update-employee"]);

const isEditModalVisible = ref(false);
const selectedEmployee = ref({});

function handleEdit(employee) {
  selectedEmployee.value = {...employee};
  isEditModalVisible.value = true;
}

function handleUpdateEmployee(employee) {
  emits("update-employee", employee);
  isEditModalVisible.value = false
}

function deleteEmployee(id) {
  emits("delete-employee", id);
}

</script>

<template>
  <div class="employee-list">
    <template v-for="employee in employees" :key="employee.id">
      <v-card class="employee-card" width="600">
        <v-card-title>
          {{ employee.second_name }} {{ employee.first_name }}
          {{ employee.patronymic ?? "" }}
        </v-card-title>
        <v-card-actions class="alpinist-card-actions">
          <v-btn
              size="x-small"
              icon
              :to="`/employees/${employee.id}`"
          >
            <v-icon size="18">mdi-eye</v-icon>
          </v-btn>
          <v-btn
              size="x-small"
              icon
              @click="handleEdit(employee)"
          >
            <v-icon size="18">mdi-pencil</v-icon>
          </v-btn>
          <v-btn
              size="x-small"
              icon
              color="error"
              @click="deleteEmployee(employee.id)"
          >
            <v-icon size="18">mdi-delete</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
      <div v-if="employees.length === 0">
        Нет данных для отображения.
      </div>
    </template>

    <EmployeeModal
        v-model="isEditModalVisible"
        :employeeData="selectedEmployee"
        mode="edit"
        @submit-employee="handleUpdateEmployee"
    />
  </div>
</template>

<style scoped>
.employee-list {
  max-width: 600px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

.employee-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
}

.employee-card {
  margin-bottom: 16px;
  position: relative;
  padding-bottom: 50px;
}

.alpinist-card-actions {
  position: absolute;
  bottom: 10px;
  right: 10px;
  display: flex;
  gap: 8px;
}
</style>
