<script setup>
import { ref } from "vue";
import ClientsModal from "@/components/clients/ClientsModal.vue";

defineProps({
  clients: {
    type: Array,
    default: () => [],
  },
});

const emits = defineEmits(["delete-client", "update-client"]);

const isEditModalVisible = ref(false);
const selectedClient = ref(null);

function handleEdit(client) {
  selectedClient.value = { ...client };
  isEditModalVisible.value = true;
}

function handleUpdateClient(client) {
  emits("update-client", client);
  isEditModalVisible.value = false;
}

function deleteClient(id) {
  emits("delete-client", id);
}
</script>

<template>
  <div class="client-list">
    <div v-if="clients.length === 0" class="no-data">
      Нет данных для отображения.
    </div>

    <v-list two-line>
      <v-list-item v-for="client in clients" :key="client.id" class="client-item">
        <v-card class="client-card">
          <v-card-title class="client-name">
            {{ client.second_name }} {{ client.first_name }}
          </v-card-title>
          <v-card-subtitle>
            Возраст: {{ client.age }} <br />
            Паспорт: {{ client.passport }}
          </v-card-subtitle>
          <v-card-actions class="client-card-actions">
            <v-btn size="small" icon :to="`/clients/${client.id}`">
              <v-icon size="22">mdi-eye</v-icon>
            </v-btn>
            <v-btn size="small" icon @click="handleEdit(client)">
              <v-icon size="22">mdi-pencil</v-icon>
            </v-btn>
            <v-btn size="small" icon color="error" @click="deleteClient(client.id)">
              <v-icon size="22">mdi-delete</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-list-item>
    </v-list>

    <ClientsModal
        v-model="isEditModalVisible"
        :clientData="selectedClient"
        mode="edit"
        @submit-client="handleUpdateClient"
    />
  </div>
</template>

<style scoped>
.client-list {
  max-width: 600px;
  margin: auto;
  padding: 20px;
}

.no-data {
  text-align: center;
  font-size: 18px;
  color: #888;
  margin-top: 20px;
}

.client-card {
  width: 100%;
  border-radius: 12px;
  transition: 0.3s ease-in-out;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 15px;
}

.client-card:hover {
  transform: translateY(-2px);
  box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.15);
}

.client-name {
  font-weight: 600;
  font-size: 16px;
  flex-grow: 1;
}

.client-card-actions {
  display: flex;
  gap: 10px;
}

.client-item {
  border-bottom: 1px solid #eee;
  padding: 5px 0;
}
</style>
