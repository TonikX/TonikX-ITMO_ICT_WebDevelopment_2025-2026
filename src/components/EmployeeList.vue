<script setup>
import { tokenStore } from "@/stores/token.js";

const token = tokenStore();
defineProps({
  employees: Array,
});

defineEmits("delete-employee");

const headers = [
  { text: "Фамилия", value: "last_name" },
  { text: "Имя", value: "first_name" },
  { text: "Отчество", value: "middle_name" },
  { text: "Номер паспорта", value: "passport_number" },
  { text: "Действия", value: "actions", sortable: false },
];
</script>

<template>
    <v-container>
      <v-data-table
        :headers="headers"
        :items="employees"
        item-value="id"
        class="elevation-1"
        :items-per-page="5"
      >
        <!-- Заголовки таблицы -->
        <template v-slot:[`item.actions`]="{ item }">
          <v-btn icon small color="error" @click="$emit('delete-employee', item.id)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
  
        <!-- Настройка заголовков -->
        <template v-slot:header>
          <tr>
            <th v-for="header in headers" :key="header.value">{{ header.text }}</th>
          </tr>
        </template>
      </v-data-table>
    </v-container>
  </template>


<style scoped>
.v-data-table th {
  font-weight: bold;
  background-color: #f0f0f0;
  padding: 10px;
  font-size: 16px;
}

.v-data-table td {
  padding: 8px;
}

.v-btn small {
  font-size: 14px;
  padding: 4px 8px;
}
</style>
