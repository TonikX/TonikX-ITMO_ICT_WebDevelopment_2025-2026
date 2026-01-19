<template>
  <DataTableCrud
    title="Clients"
    :endpoint="endpoints.crud.clients"
    :columns="columns"
    :formFields="formFields"
  />
</template>

<script setup>
import DataTableCrud from "@/components/DataTableCrud.vue";
import { endpoints } from "@/api/endpoints";

const columns = [
  { key: "id", title: "ID" },
  { key: "passport_number", title: "Passport" },
  { key: "last_name", title: "Last name" },
  { key: "first_name", title: "First name" },
  { key: "patronymic", title: "Patronymic" },
  { key: "city_from", title: "City" },
  { key: "address", title: "Address" },
];

const formFields = [
  { key: "passport_number", label: "Passport number" },
  { key: "last_name", label: "Last name" },
  { key: "first_name", label: "First name" },
  { key: "patronymic", label: "Patronymic" },
  { key: "city_from", label: "City from" },
  { key: "address", label: "Address" },
];
</script>