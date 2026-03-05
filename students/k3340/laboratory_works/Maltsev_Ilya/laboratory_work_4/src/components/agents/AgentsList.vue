<script setup>
import { ref } from "vue";
import AgentsModal from "@/components/agents/AgentsModal.vue";

defineProps({
  agents: {
    type: Array,
    default: () => [],
  },
});

const emits = defineEmits(["delete-agent", "update-agent"]);

const isEditModalVisible = ref(false);
const selectedAgent = ref(null);

function handleEdit(agent) {
  selectedAgent.value = { ...agent };
  isEditModalVisible.value = true;
}

function handleUpdateAgent(agent) {
  emits("update-agent", agent);
  isEditModalVisible.value = false;
}

function deleteAgent(id) {
  emits("delete-agent", id);
}
</script>

<template>
  <div class="agent-list">
    <div v-if="agents.length === 0" class="no-data">
      Нет данных для отображения.
    </div>

    <v-list two-line>
      <v-list-item v-for="agent in agents" :key="agent.id" class="agent-item">
        <v-card class="agent-card">
          <v-card-title class="agent-name">
            {{ agent.second_name }} {{ agent.first_name }}
            {{ agent.patronymic ?? "" }}
          </v-card-title>
          <v-card-actions class="agent-card-actions">
            <v-btn size="small" icon :to="`/agents/${agent.id}`">
              <v-icon size="22">mdi-eye</v-icon>
            </v-btn>
            <v-btn size="small" icon @click="handleEdit(agent)">
              <v-icon size="22">mdi-pencil</v-icon>
            </v-btn>
            <v-btn size="small" icon color="error" @click="deleteAgent(agent.id)">
              <v-icon size="22">mdi-delete</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-list-item>
    </v-list>

    <AgentsModal
        v-model="isEditModalVisible"
        :agentData="selectedAgent"
        mode="edit"
        @submit-agent="handleUpdateAgent"
    />
  </div>
</template>

<style scoped>
.agent-list {
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

.agent-card {
  width: 100%;
  border-radius: 12px;
  transition: 0.3s ease-in-out;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 15px;
}

.agent-card:hover {
  transform: translateY(-2px);
  box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.15);
}

.agent-name {
  font-weight: 600;
  font-size: 16px;
  flex-grow: 1;
}

.agent-card-actions {
  display: flex;
  gap: 10px;
}

.agent-item {
  border-bottom: 1px solid #eee;
  padding: 5px 0;
}
</style>
