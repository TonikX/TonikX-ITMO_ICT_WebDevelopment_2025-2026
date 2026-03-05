<script setup>
import {onMounted, ref} from "vue";
import {useRoute} from "vue-router";
import axios from "axios";
import IndividualContractModal from "@/components/individual_contract/IndividualContractModal.vue";

const route = useRoute();
const client = ref(null);
const contracts = ref([]);
const agents = ref([]);
const isLoading = ref(false);
const isError = ref(false);
const isContractModalVisible = ref(false);
const selectedContract = ref(null);

const contractTypes = {
  "m": "Медицинский",
  "l": "Страхование жизни и имущества",
  "a": "Несчастный случай",
};

const contractStatuses = {
  "a": "Активный",
  "p": "Приостановлен",
  "e": "Истёкший"
};

async function fetchClientDetails() {
  try {
    const response = await axios.get(`/insurance/clients/${route.params.id}`);
    client.value = response.data;
    await fetchContracts();
  } catch (error) {
    console.error("Ошибка загрузки данных клиента", error);
    isError.value = true;
  }
}

async function fetchContracts() {
  await axios
      .get("/insurance/clients/contracts")
      .then(response => contracts.value = response.data.filter(contract => contract.client?.id === client.value.id))
      .catch(error => console.error("Ошибка загрузки контрактов", error));
}

async function fetchAgents() {
  await axios.get("/insurance/agents").then(response => {
    agents.value = response.data
  }).catch(error => {
    isError.value = true;
    console.error("Ошибка загрузки агентов", error);
  });
}

function openContractModal(contract) {
  selectedContract.value = contract;
  isContractModalVisible.value = true;
}

async function saveContract(contract) {
  try {
    if (contract.id) {
      await axios.put(`/insurance/clients/contracts/${contract.id}/`, contract);
    } else {
      await axios.post(`/insurance/clients/contracts`, contract);
    }
    await fetchContracts();
  } catch (error) {
    console.error("Ошибка сохранения контракта", error);
  }
}

onMounted(async () => {
  isLoading.value = true;
  await fetchClientDetails();
  await fetchAgents();
  isLoading.value = false;
});

</script>

<template>
  <div v-if="isLoading">Загрузка...</div>
  <div v-else-if="isError">Ошибка загрузки данных.</div>
  <div v-else-if="client">
    <section class="client-details">
      <h1>{{ client.second_name }} {{ client.first_name }}</h1>
      <p><strong>Возраст:</strong> {{ client.age }}</p>
      <p><strong>Паспорт:</strong> {{ client.passport }}</p>
    </section>

    <section class="contracts-section">
      <h2>Контракты</h2>
      <v-btn color="primary" @click="openContractModal">Создать контракт</v-btn>
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
            </v-card-text>
            <v-card-actions>
              <v-btn size="small" icon @click="openContractModal(contract)">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-list-item>
      </v-list>
      <p v-else>Нет контрактов</p>
    </section>
  </div>
  <IndividualContractModal
      v-model="isContractModalVisible"
      :agents="agents"
      :contract-data="selectedContract"
      @submit-contract="saveContract"
      :client-data="client"
    />
</template>

<style scoped>
.client-details {
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
