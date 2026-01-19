<template>
  <DataTableCrud
    title="Cleaning schedules"
    :endpoint="endpoints.crud.schedules"
    :columns="columns"
    :formFields="formFields"
  >
    <template #item.employee="{ item }">
      {{ employeeLabel(item.employee) }}
    </template>

    <template #item.weekday="{ item }">
      {{ weekdayLabel(item.weekday) }}
    </template>
  </DataTableCrud>
</template>

<script setup>
import { ref, onMounted } from "vue";
import DataTableCrud from "@/components/DataTableCrud.vue";
import { endpoints } from "@/api/endpoints";
import { http } from "@/api/http";

const employees = ref([]);

const columns = [
  { key: "id", title: "ID" },
  { key: "employee", title: "Employee" },
  { key: "floor", title: "Floor" },
  { key: "weekday", title: "Weekday" },
];

const weekdayItems = [
  { value: 0, title: "Пн" },
  { value: 1, title: "Вт" },
  { value: 2, title: "Ср" },
  { value: 3, title: "Чт" },
  { value: 4, title: "Пт" },
  { value: 5, title: "Сб" },
  { value: 6, title: "Вс" },
];

const formFields = [
  {
    key: "employee",
    label: "Employee",
    type: "select",
    items: employees,
    itemTitle: "label",
    itemValue: "id",
    md: 6,
  },
  { key: "floor", label: "Floor", type: "number", md: 6 },
  {
    key: "weekday",
    label: "Weekday",
    type: "select",
    items: weekdayItems,
    itemTitle: "title",
    itemValue: "value",
    md: 6,
  },
];

function employeeLabel(id) {
  const e = employees.value.find((x) => x.id === id);
  return e ? e.label : `#${id}`;
}

function weekdayLabel(v) {
  const w = weekdayItems.find((x) => x.value === v);
  return w ? w.title : v;
}

async function loadEmployees() {
  const res = await http.get(endpoints.crud.employees);
  employees.value = res.data.map((e) => ({
    id: e.id,
    label: `${e.last_name} ${e.first_name} ${e.patronymic || ""}`.trim(),
  }));
}

onMounted(loadEmployees);
</script>