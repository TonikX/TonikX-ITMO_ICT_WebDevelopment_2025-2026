<script setup>
import {onMounted, ref} from 'vue';
import {useRoute} from 'vue-router';
import axios from "axios";

const employeeId = ref(null);
const employeeData = ref();
const isLoading = ref(true);
const isError = ref(false);
const route = useRoute();
employeeId.value = route.params.id;

async function fetchEmployeesCells() {
  isLoading.value = true;
  await axios
      .get(`manufactory/employees/${employeeId.value}`)
      .then(response => {
        employeeData.value = response.data;
      })
      .catch(error => {
        console.error("Ошибка загрузки сотрудников", error);
        isError.value = true;
      })
      .finally(() => {
        isLoading.value = false;
      });
}

onMounted(fetchEmployeesCells)
</script>

<template>
  <div v-if="isLoading">Загрузка...</div>
  <div v-else-if="isError" class="error">Произошла ошибка при загрузке данных.</div>
  <div v-else>
    <v-card class="employee-details-card" width="800">
      <v-card-title>
        {{ employeeData.second_name }} {{ employeeData.first_name }}
        {{ employeeData.patronymic }}
      </v-card-title>
      <v-card-subtitle>
        Паспортные данные: {{ employeeData.passport }}
      </v-card-subtitle>
      <v-divider></v-divider>
      <v-card-text>
        <h3>Закреплённые клетки:</h3>
        <v-list>
          <v-list-item
              v-for="(detail, index) in employeeData.responsible_cells"
              :key="index"
          >
            <v-list-item-content>
              <v-list-item-title>Клетка {{ detail.cell_code }}</v-list-item-title>
              <v-list-item-subtitle>
                Цех {{ detail.workshop.title }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
  </div>
</template>

<style scoped>
.employee-details-card {
  margin: 0 auto;
  padding: 16px;
}

.error {
  color: red;
  font-weight: bold;
  margin-top: 16px;
}
</style>