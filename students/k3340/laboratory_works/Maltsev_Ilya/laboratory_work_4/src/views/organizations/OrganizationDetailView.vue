<script setup>
import {onMounted, ref} from "vue";
import {useRoute} from "vue-router";
import axios from "axios";
import router from "@/utils/router.js";
import OrganizationsModal from "@/components/organizations/OrganizationsModal.vue";
import CollectiveContractModal from "@/components/collective_contract/CollectiveContractModal.vue";
import ParticipantModal from "@/components/collective_contract/ParticipantModal.vue";

const route = useRoute();
const organization = ref(null);
const contracts = ref([]);
const agents = ref([])
const clients = ref([]);
const riskCategories = ref([]);
const isLoading = ref(false);
const isError = ref(false);
const isContractModalVisible = ref(false);
const isEditOrganizationModalVisible = ref(false);
const isAddParticipantModalVisible = ref(false);
const selectedContract = ref(null);
const selectedContractParticipants = ref([]);

const contractTypes = {
  "m": "Медицинский",
  "l": "Страхование жизни и имущества",
  "a": "Несчастный случай",
  "g": "Ипотека"
};

const contractStatuses = {
  "a": "Активный",
  "p": "Приостановлен",
  "e": "Истёкший"
};

async function fetchOrganizationDetails() {
  await axios.get(`/insurance/organizations/${route.params.id}`).then(response => {
    organization.value = response.data;
  }).catch(error => {
    console.error("Ошибка загрузки данных организации", error);
    isError.value = true;
  });
}

async function fetchContracts() {
  await axios.get("/insurance/organizations/contracts").then(response => {
    contracts.value = response.data.filter(contract => contract.organization?.id === organization.value.id)
  }).catch(error => {
    isError.value = true;
    console.error("Ошибка загрузки контрактов", error);
  });
}

async function fetchAgents() {
  await axios.get("/insurance/agents").then(response => {
    agents.value = response.data
  }).catch(error => {
    isError.value = true;
    console.error("Ошибка загрузки агентов", error);
  });
}

async function fetchRiskCategories() {
  await axios.get("/insurance/categories").then(response => {
    riskCategories.value = response.data
  }).catch(error => {
    isError.value = true;
    console.error("Ошибка загрузки категорий", error);
  });
}

async function fetchClients() {
  await axios.get("/insurance/clients").then(response => {
    clients.value = response.data
  }).catch(error => {
    isError.value = true;
    console.error("Ошибка загрузки клиентов", error);
  });
}


function openContractModal(contract = null) {
  selectedContract.value = contract ? {...contract} : null;
  selectedContractParticipants.value = contract ? contract.insured_employees : [];
  isContractModalVisible.value = true;
}


async function saveContract(contract) {
  try {
    if (contract.id) {
      await axios.put(`/insurance/organizations/contracts/${contract.id}/`, contract);
    } else {
      await axios.post(`/insurance/organizations/contracts/`, contract);
    }
    await fetchContracts();
  } catch (error) {
    console.error("Ошибка сохранения контракта", error);
  }
}

async function deleteContract(contractId) {
  await axios
      .delete(`/insurance/organizations/contracts/${contractId}/`)
      .then(contracts.value = contracts.value.filter(contract => contract.id !== contractId))
      .catch(error => console.error("Ошибка удаления контракта", error));
}

async function updateOrganization(updatedData) {
  await axios
      .put(`/insurance/organizations/${organization.value.id}/`, updatedData)
      .then(organization.value = updatedData)
      .catch(error => {
        console.error("Ошибка обновления информации об организации", error);
      });
}

async function deleteOrganization() {
  await axios
      .delete(`/insurance/organizations/${organization.value.id}/`)
      .then(router.push(`/organizations/`))
      .catch(error => console.error("Ошибка удаления организации", error));
}

async function addParticipantToContract(participant) {
  await axios
      .post(`/insurance/employees/`, participant)
      .then(() => {
        selectedContractParticipants.value.push(participant);
        fetchContracts()
      })
      .catch(error => console.error("Ошибка добавления участника", error));
}

function handleAddParticipant(contract) {
  selectedContract.value = contract;
  isAddParticipantModalVisible.value = true;
}


onMounted(async () => {
  isLoading.value = true;
  await fetchOrganizationDetails();
  await fetchContracts();
  await fetchAgents();
  await fetchRiskCategories();
  await fetchClients();
  isLoading.value = false;
});
</script>

<template>
  <div v-if="isLoading">Загрузка...</div>
  <div v-else-if="isError">Ошибка загрузки данных.</div>
  <div v-else-if="organization">
    <section class="organization-details">
      <h1>{{ organization.full_name }}</h1>
      <p><strong>Краткое название:</strong> {{ organization.short_name }}</p>
      <p><strong>Адрес:</strong> {{ organization.address }}</p>
      <p><strong>Банковский код:</strong> {{ organization.bank_code }}</p>
      <p><strong>Специализация:</strong> {{ organization.specialization }}</p>
      <v-btn-group>
        <v-btn color="primary" @click="isEditOrganizationModalVisible = true">Редактировать</v-btn>
        <v-btn color="error" @click="deleteOrganization">Удалить</v-btn>
      </v-btn-group>
    </section>

    <section class="contracts-section">
      <h2>Контракты</h2>
      <v-btn color="primary" @click="openContractModal()">Создать контракт</v-btn>
      <v-list v-if="contracts.length">
        <v-list-item v-for="contract in contracts" :key="contract.id">
          <v-card class="contract-card">
            <v-card-title>Контракт №{{ contract.id }}</v-card-title>
            <v-card-subtitle>
              Дата подписания: {{ contract.sign_date }} <br/>
              Дата начала: {{ contract.start_date }} <br/>
              Дата окончания: {{ contract.end_date }}
            </v-card-subtitle>
            <v-card-text>
              <p><strong>Тип контракта:</strong> {{ contractTypes[contract.type] || "Неизвестный" }}</p>
              <p><strong>Статус контракта:</strong> {{ contractStatuses[contract.status] || "Неизвестный" }}</p>
              <p><strong>Агент:</strong> {{ contract.agent.second_name }} {{ contract.agent.first_name }}
                {{ contract.agent.patronymic }}</p>
              <p><strong>Телефон агента:</strong> {{ contract.agent.phone_number }}</p>
              <h3>Участники</h3>
              <ul>
                <li v-for="participant in contract.insured_employees" :key="participant.id">
                  {{ participant.client.second_name }} {{ participant.client.first_name }} -
                  {{ participant.risk_category.title }}
                </li>
              </ul>
              <v-btn color="success" @click="handleAddParticipant(contract)">Добавить участника</v-btn>
            </v-card-text>
            <v-card-actions>
              <v-btn size="small" icon @click="openContractModal(contract)">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn size="small" icon color="error" @click="deleteContract(contract.id)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-list-item>
      </v-list>
      <p v-else>Нет контрактов</p>
    </section>
  </div>
  <OrganizationsModal
      v-model="isEditOrganizationModalVisible"
      :organization-data="organization"
      mode="edit"
      @submit-organization="updateOrganization"
  />

  <CollectiveContractModal
      v-model="isContractModalVisible"
      :contract-data="selectedContract"
      :organization-data="organization"
      :agents="agents"
      @submit-contract="saveContract"
  />
  <ParticipantModal
      v-model="isAddParticipantModalVisible"
      :contract-data="selectedContract"
      :clients="clients"
      :categories="riskCategories"
      @submit-participant="addParticipantToContract"
  />
</template>

<style scoped>
.organization-details {
  padding: 20px;
  border-radius: 10px;
  background-color: #e6f7ff;
  margin-bottom: 30px;
  text-align: center;
}

.contracts-section {
  margin-bottom: 40px;
  padding: 20px;
  border-radius: 10px;
}

.contract-card {
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  background: white;
}
</style>