<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import OrganizationsList from "@/components/organizations/OrganizationsList.vue";
import OrganizationsModal from "@/components/organizations/OrganizationsModal.vue";

const organizations = ref([]);
const isLoading = ref(false);
const isError = ref(false);
const isAddModalVisible = ref(false);

async function fetchOrganizations() {
  isLoading.value = true;
  await axios.get("insurance/organizations").then(response => organizations.value = response.data).catch(error => {
    console.error("Ошибка загрузки организаций", error);
    isError.value = true;
  }).finally(() => isLoading.value = false)
}

async function addOrganization(organization) {
  await axios.post("insurance/organizations/", organization).then(fetchOrganizations).catch(error => {
        isError.value = true;
        console.error("Ошибка добавления организации", error);
      }
  );
}

async function deleteOrganization(id) {
  await axios.delete(`insurance/organizations/${id}/`).then(organizations.value = organizations.value.filter(org => org.id !== id)).catch(error => {
    isError.value = true;
    console.error("Ошибка удаления организации", error);
  })
}

async function updateOrganization(organization) {
  await axios.put(`insurance/organizations/${organization.id}/`, organization).then(fetchOrganizations).catch(error => {
    isError.value = true;
    console.error("Ошибка обновления организации", error);
  });
}

onMounted(fetchOrganizations);
</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <template v-if="isLoading">
      <v-skeleton-loader type="card" class="mt-4" max-width="500"></v-skeleton-loader>
    </template>
    <template v-else>
      <h2>Список организаций</h2>
      <v-btn color="primary" @click="isAddModalVisible = true">Добавить организацию</v-btn>
      <OrganizationsList :organizations="organizations" @delete-organization="deleteOrganization"
                         @update-organization="updateOrganization"/>
      <OrganizationsModal v-model="isAddModalVisible" mode="add" @submit-organization="addOrganization"/>
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
