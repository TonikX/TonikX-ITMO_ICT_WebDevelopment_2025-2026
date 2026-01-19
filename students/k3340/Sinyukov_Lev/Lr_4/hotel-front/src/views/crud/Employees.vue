<template>
  <DataTableCrud
    title="Employees"
    :endpoint="endpoints.crud.employees"
    :columns="columns"
    :formFields="formFields"
  >
    <template #item.is_active="{ item }">
      <v-chip :color="item.is_active ? 'success' : 'grey'">
        {{ item.is_active ? "active" : "inactive" }}
      </v-chip>
    </template>
  </DataTableCrud>
</template>

<script setup>
import DataTableCrud from "@/components/DataTableCrud.vue";
import { endpoints } from "@/api/endpoints";

const columns = [
  { key: "id", title: "ID" },
  { key: "last_name", title: "Last name" },
  { key: "first_name", title: "First name" },
  { key: "patronymic", title: "Patronymic" },
  { key: "is_active", title: "Active" },
];

const formFields = [
  { key: "last_name", label: "Last name", md: 6 },
  { key: "first_name", label: "First name", md: 6 },
  { key: "patronymic", label: "Patronymic", md: 6 },
  { key: "is_active", label: "Is active", type: "switch", md: 6 },
];
</script>