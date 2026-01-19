<template>
  <DataTableCrud
    title="Stays"
    :endpoint="endpoints.crud.stays"
    :columns="columns"
    :formFields="formFields"
  >
    <!-- Кастомный вывод клиента/комнаты -->
    <template #item.client="{ item }">
      {{ clientLabel(item.client) }}
    </template>

    <template #item.room="{ item }">
      {{ roomLabel(item.room) }}
    </template>
  </DataTableCrud>
</template>

<script setup>
import { ref, onMounted } from "vue";
import DataTableCrud from "@/components/DataTableCrud.vue";
import { endpoints } from "@/api/endpoints";
import { http } from "@/api/http";

const clients = ref([]);
const rooms = ref([]);

const columns = [
  { key: "id", title: "ID" },
  { key: "client", title: "Client" },
  { key: "room", title: "Room" },
  { key: "check_in", title: "Check-in" },
  { key: "check_out", title: "Check-out" },
];

const formFields = [
  {
    key: "client",
    label: "Client",
    type: "select",
    items: clients,
    itemTitle: "label",
    itemValue: "id",
    md: 6,
  },
  {
    key: "room",
    label: "Room",
    type: "select",
    items: rooms,
    itemTitle: "label",
    itemValue: "id",
    md: 6,
  },
  { key: "check_in", label: "Check-in", type: "date", md: 6 },
  { key: "check_out", label: "Check-out (можно пусто)", type: "date", md: 6 },
];

function clientLabel(clientId) {
  const c = clients.value.find((x) => x.id === clientId);
  return c ? c.label : `#${clientId}`;
}

function roomLabel(roomId) {
  const r = rooms.value.find((x) => x.id === roomId);
  return r ? r.label : `#${roomId}`;
}

async function loadRefs() {
  const [cRes, rRes] = await Promise.all([
    http.get(endpoints.crud.clients),
    http.get(endpoints.crud.rooms),
  ]);

  clients.value = cRes.data.map((c) => ({
    id: c.id,
    label: `${c.last_name} ${c.first_name} (паспорт: ${c.passport_number})`,
  }));

  rooms.value = rRes.data.map((r) => ({
    id: r.id,
    label: `№${r.number}, этаж ${r.floor}, ${r.type}, ${r.price_per_day}/day`,
  }));
}

onMounted(loadRefs);
</script>