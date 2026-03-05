<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import AgentsModal from "@/components/agents/AgentsModal.vue";
import AgentsList from "@/components/agents/AgentsList.vue";

const agents = ref([]);
const isLoading = ref(false);
const isError = ref(false);
const isAddModalVisible = ref(false);

async function fetchAgents() {
  isLoading.value = true;
  await axios
      .get('insurance/agents')
      .then(response => {
        agents.value = response.data;
      })
      .catch(error => {
        console.error("Ошибка загрузки агентов", error);
        isError.value = true;
      })
      .finally(() => {
        isLoading.value = false;
      });
}

async function addAgent(agent) {
  await axios.post(`insurance/agents/`, agent).then(fetchAgents).catch(error => {
    isError.value = true;
    console.error(`Ошибка добавления агента: ${error}`);
  })
}

async function deleteAgent(id) {
  await axios.delete(`insurance/agents/${id}/`).then(() => {
    agents.value = agents.value.filter(item => item.id !== id);
  }).catch(error => {
    isError.value = true;
    console.error(`Ошибка удаления агента: ${error}`);
  })
}

async function updateAgent(agent) {
  await axios.put(`insurance/agents/${agent.id}/`, agent).then(fetchAgents).catch(error => {
    isError.value = true;
    console.error(`Ошибка обновления агента: ${error}`);
  })
}

onMounted(fetchAgents);

</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <template v-if="isLoading">
      <v-skeleton-loader
          type="card"
          class="mt-4"
          max-width="500"
      ></v-skeleton-loader>
    </template>
    <template v-else>
      <h2>Список агентов</h2>
      <v-btn color="primary" @click="isAddModalVisible = true">Добавить агента</v-btn>
      <AgentsList :agents="agents" @delete-agent="deleteAgent" @update-agent="updateAgent"/>
      <AgentsModal
          v-model="isAddModalVisible"
          mode="add"
          @submit-agent="addAgent"
      />
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