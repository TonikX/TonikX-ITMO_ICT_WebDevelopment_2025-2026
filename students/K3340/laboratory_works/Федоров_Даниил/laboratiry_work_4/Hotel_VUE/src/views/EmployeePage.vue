<template>
  <v-container>
    <v-container>
      <h1>Все номера</h1>
      <v-btn v-if="!addingEmployee" @click="addingEmployee = true" color="primary">Добавить работника</v-btn>
    </v-container>
    <v-container>
      <v-form @submit.prevent="addEmployee" v-if="addingEmployee">
        <v-text-field v-model="newEmployee.first_name" label="Имя" required></v-text-field>
        <v-text-field v-model="newEmployee.last_name" label="Фамилия" required></v-text-field>
        <v-text-field v-model="newEmployee.middle_name" label="Отчество" required></v-text-field>
        <v-text-field v-model="newEmployee.add_date" label="Дата принятия на работу" type="date" required></v-text-field>

        <v-btn color="primary" type="submit">Добавить</v-btn>
        <v-btn @click="addingEmployee = false" color="secondary">Отмена</v-btn>
      </v-form>
    </v-container>
    <v-row>
      <v-col v-for="employee in employees" :key="employee.id" cols="12" md="27">
        <EmployeeCard :employee="employee" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import EmployeeCard from '@/components/EmployeeCard.vue';

const employees = ref([]);

const fetchEmployee = async () => {
  try {
    const response = await axios.get('api/Employees');
    employees.value = response.data;
  } catch (error) {
    console.error('Ошибка при получении списка работников:', error);
  }
};

const addingEmployee = ref(false);
const newEmployee = ref({
  first_name: '',
  last_name: '',
  middle_name: '',
  add_date: null,
  delete_date: null,
  dismissed: false,
});

const addEmployee = async () => {
  try {
    await axios.post('api/Employees/', {
      first_name: newEmployee.value.first_name,
      last_name: newEmployee.value.last_name,
      middle_name: newEmployee.value.middle_name,
      add_date: newEmployee.value.add_date,
      delete_date: newEmployee.value.delete_date,
      dismissed: newEmployee.value.dismissed,
    });
    alert('Работник добавлен');
    addingEmployee.value = false;
    fetchEmployee();
  } catch (error) {
    console.error('Ошибка при добавлении работника', error);
    alert('Ошибка при добавлении работника');
  }
};

onMounted(() => {
  fetchEmployee();
});
</script>
