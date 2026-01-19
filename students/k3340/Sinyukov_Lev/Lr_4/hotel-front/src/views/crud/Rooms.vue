<template>
  <DataTableCrud
    title="Rooms"
    :endpoint="endpoints.crud.rooms"
    :columns="columns"
    :formFields="formFields"
  />
</template>

<script setup>
import DataTableCrud from "@/components/DataTableCrud.vue";
import { endpoints } from "@/api/endpoints";

const columns = [
  { key: "id", title: "ID" },
  { key: "number", title: "Number" },
  { key: "floor", title: "Floor" },
  { key: "type", title: "Type" },
  { key: "price_per_day", title: "Price/day" },
  { key: "phone", title: "Phone" },
];

const formFields = [
  { key: "number", label: "Number", type: "number" },
  { key: "floor", label: "Floor", type: "number" },
  { key: "type", label: "Type (S/D/T)" },
  { key: "price_per_day", label: "Price/day" },
  { key: "phone", label: "Phone" },
];
</script>