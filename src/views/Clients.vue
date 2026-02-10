<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import AddClientModal from "@/components/AddClient.vue"; 
import ClientsSamePeriod from "@/components/AddClient.vue";
import { tokenStore } from "@/stores/token.js";

const tokenStorage = tokenStore();
const clients = ref([]);
const search = ref("");
const headers = ref([
  { text: "Имя", value: "first_name" },
  { text: "Фамилия", value: "last_name" },
  { text: "Отчество", value: "middle_name" },
  { text: "Город", value: "city" },
  { text: "Последняя комната", value: "last_room" },
  { text: "Действия", value: "actions", sortable: false },
]);


const isShowModal = ref(false);

function fetchClients() {
  axios
    .get("/api/clients/", {
      headers: {
        Authorization: `Token ${tokenStorage.token}`, 
      },
    })
    .then((response) => {
      clients.value = response.data; 
    })
    .catch((error) => {
      console.error("Ошибка загрузки клиентов:", error);
    });
}


async function deleteClient(id) {
  try {
    await axios.delete(`/api/clients/${id}`, {
      headers: {
        Authorization: `Token ${tokenStorage.token}`,
      },
    });
    fetchClients(); 
  } catch (error) {
    console.error("Ошибка удаления клиента:", error);
  }
}


function toggleModal() {
  isShowModal.value = !isShowModal.value;
}


onMounted(fetchClients);
</script>

<template>
  <v-container>
    <h1>Клиенты</h1>
    <v-text-field 
      v-model="search" 
      label="Поиск" 
      class="mb-3" 
      append-icon="mdi-magnify"
    ></v-text-field>

    <v-data-table
      :headers="headers"
      :items="clients"
      :search="search"
      item-value="id"
      class="elevation-1"
      :items-per-page="5"
    >
      <template v-slot:top>
        <v-btn color="primary" @click="toggleModal">Добавить клиента</v-btn>
      </template>

      <template v-slot:[`item.actions`]="{ item }">
        <v-btn icon color="primary" @click="editClient(item.id)">
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
        <v-btn icon color="error" @click="deleteClient(item.id)">
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </template>
    </v-data-table>
    <AddClientModal
      v-model="isShowModal"
      @refresh="fetchClients"
    />
  </v-container>
</template>
