<script setup>
import {onMounted, ref} from 'vue';
import {useRoute} from 'vue-router';
import axios from "axios";

const agentId = ref(null);
const agentData = ref();
const isLoading = ref(true);
const isError = ref(false);
const route = useRoute();
const individualContracts = ref([]);
const collectiveContracts = ref([]);
agentId.value = route.params.id;

async function fetchAgent() {
  isLoading.value = true;
  await axios
      .get(`insurance/agents/${agentId.value}`)
      .then(response => {
        agentData.value = response.data;
      })
      .catch(error => {
        console.error("Ошибка загрузки агентов", error);
        isError.value = true;
      })
}

async function fetchIndividualContracts() {
  isLoading.value = true;
  await axios
      .get(`insurance/clients/contracts`)
      .then(response => {
        individualContracts.value = response.data.filter(contract =>
            Number(contract.agent?.id) === Number(agentId.value)
        );
      })
      .catch(error => {
        console.error("Ошибка загрузки контрактов", error);
        isError.value = true;
      })
}

async function fetchCollectiveContracts() {
  isLoading.value = true;
  await axios
      .get(`insurance/organizations/contracts`)
      .then(response => {
        collectiveContracts.value = response.data.filter(contract =>
            Number(contract.agent.id) === Number(agentId.value));
      })
      .catch(error => {
        console.error("Ошибка загрузки контрактов", error);
        isError.value = true;
      })
}


onMounted(async () => {
  await fetchAgent();
  await fetchIndividualContracts();
  await fetchCollectiveContracts();
  console.log(agentData.value)
  isLoading.value = false;
})
</script>

<template>
  <div v-if="isLoading">Загрузка...</div>
  <div v-else-if="isError">Ошибка загрузки данных.</div>
  <div v-else-if="agentData">
    <section class="agent-details">
      <h1>Информация об агенте</h1>
      <p><strong>ФИО:</strong> {{ agentData.second_name }} {{ agentData.first_name }} {{ agentData.patronymic }}</p>
      <p><strong>Паспорт:</strong> {{ agentData.passport }}</p>
      <p><strong>Телефон:</strong> {{ agentData.phone_number }}</p>
    </section>

    <section class="contract-section individual-contracts">
      <h2>Индивидуальные контракты</h2>
      <v-list v-if="individualContracts.length">
        <v-list-item v-for="contract in individualContracts" :key="contract.id">
          <v-card class="contract-card">
            <v-card-title>Клиент: {{ contract.client.second_name }} {{ contract.client.first_name }}</v-card-title>
            <v-card-subtitle>
              Дата подписания: {{ contract.sign_date }} <br />
              Дата начала: {{ contract.start_date }} <br />
              Дата окончания: {{ contract.end_date }}
            </v-card-subtitle>
          </v-card>
        </v-list-item>
      </v-list>
      <p v-else>Нет индивидуальных контрактов</p>
    </section>

    <section class="contract-section collective-contracts">
      <h2>Коллективные контракты</h2>
      <v-list v-if="collectiveContracts.length">
        <v-list-item v-for="contract in collectiveContracts" :key="contract.id">
          <v-card class="contract-card">
            <v-card-title>Организация: {{ contract.organization.full_name }}</v-card-title>
            <v-card-subtitle>
              Адрес: {{ contract.organization.address }} <br />
              Специализация: {{ contract.organization.specialization }}
            </v-card-subtitle>
            <v-card-text>
              <strong>Застрахованные сотрудники:</strong>
              <ul>
                <li v-for="employee in contract.insured_employees" :key="employee.id">
                  {{ employee.client.second_name }} {{ employee.client.first_name }} — Категория риска: {{ employee.risk_category.title }} ({{ employee.risk_category.payment_amount }} руб.)
                </li>
              </ul>
              Дата подписания: {{ contract.sign_date }} <br />
              Дата начала: {{ contract.start_date }} <br />
              Дата окончания: {{ contract.end_date }}
            </v-card-text>
          </v-card>
        </v-list-item>
      </v-list>
      <p v-else>Нет коллективных контрактов</p>
    </section>
  </div>
</template>

<style scoped>
h2 {
  font-size: 20px;
  margin-top: 20px;
}

.contract-section {
  margin-bottom: 40px;
  padding: 20px;
  border-radius: 10px;
}

.agent-details {
  padding: 20px;
  border-radius: 10px;
  background-color: #e6f7ff;
  margin-bottom: 30px;
  text-align: center;
}


.individual-contracts {
  background-color: #f0f8ff;
}

.collective-contracts {
  background-color: #fff0f5;
}

.contract-card {
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  background: white;
}
</style>