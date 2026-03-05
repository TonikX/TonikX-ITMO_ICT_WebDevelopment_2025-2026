<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import ClientsList from "@/components/clients/ClientsList.vue";
import ClientsModal from "@/components/clients/ClientsModal.vue";

const clients = ref([]);
const isLoading = ref(false);
const isError = ref(false);
const isAddModalVisible = ref(false);

async function fetchClients() {
  isLoading.value = true;
  await axios
      .get("/insurance/clients")
      .then(response => clients.value = response.data)
      .catch(error => {
        console.error("Ошибка загрузки клиентов", error);
        isError.value = true;
      })
      .finally(() => isLoading.value = false);
}

async function addClient(client) {
  await axios
      .post("/insurance/clients/", client)
      .then(fetchClients)
      .catch(error => {
        isError.value = true;
        console.error("Ошибка добавления клиента", error);
      });
}

async function deleteClient(id) {
  await axios
      .delete(`/insurance/clients/${id}/`)
      .then(clients.value = clients.value.filter(client => client.id !== id))
      .catch(error => {
        isError.value = true;
        console.error("Ошибка удаления клиента", error);
      });
}

async function updateClient(client) {
  await axios
      .put(`/insurance/clients/${client.id}/`, client)
      .then(fetchClients)
      .catch(error => {
        isError.value = true;
        console.error("Ошибка обновления клиента", error);
      });
}

onMounted(fetchClients);
</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <template v-if="isLoading">
      <v-skeleton-loader type="card" class="mt-4" max-width="500"></v-skeleton-loader>
    </template>
    <template v-else>
      <h2>Список клиентов</h2>
      <v-btn color="primary" @click="isAddModalVisible = true">Добавить клиента</v-btn>
      <ClientsList :clients="clients" @delete-client="deleteClient" @update-client="updateClient"/>
      <ClientsModal v-model="isAddModalVisible" mode="add" @submit-client="addClient"/>
    </template>
  </div>
</template>

<style scoped>
.actions > .v-btn {
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}
</style>
