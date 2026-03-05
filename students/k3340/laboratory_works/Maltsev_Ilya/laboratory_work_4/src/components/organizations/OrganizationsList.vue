<script setup>
import { ref } from "vue";
import OrganizationsModal from "@/components/organizations/OrganizationsModal.vue";
import router from "@/utils/router.js";

defineProps({
  organizations: {
    type: Array,
    default: () => [],
  },
});

const emits = defineEmits(["delete-organization", "update-organization"]);

const isEditModalVisible = ref(false);
const selectedOrganization = ref(null);

function handleEdit(organization) {
  selectedOrganization.value = { ...organization };
  isEditModalVisible.value = true;
}

function handleUpdateOrganization(organization) {
  emits("update-organization", organization);
  isEditModalVisible.value = false;
}

function deleteOrganization(id) {
  emits("delete-organization", id);
}
</script>

<template>
  <div class="organization-list">
    <div v-if="organizations.length === 0" class="no-data">
      Нет данных для отображения.
    </div>

    <v-list two-line>
      <v-list-item v-for="organization in organizations" :key="organization.id" class="organization-item">
        <v-card class="organization-card"  @click="router.push(`/organizations/${organization.id}`)">
          <v-card-title class="organization-name">
            {{ organization.full_name }} ({{ organization.short_name }})
          </v-card-title>
          <v-card-subtitle>
            Адрес: {{ organization.address }} <br />
            Специализация: {{ organization.specialization }}
          </v-card-subtitle>
        </v-card>
      </v-list-item>
    </v-list>

    <OrganizationsModal
        v-model="isEditModalVisible"
        :organizationData="selectedOrganization"
        mode="edit"
        @submit-organization="handleUpdateOrganization"
    />
  </div>
</template>

<style scoped>
.organization-list {
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

.organization-card {
  width: 100%;
  border-radius: 12px;
  transition: 0.3s ease-in-out;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 15px;
}

.organization-card:hover {
  transform: translateY(-2px);
  box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.15);
}

.organization-name {
  font-weight: 600;
  font-size: 16px;
  flex-grow: 1;
}

.organization-card-actions {
  display: flex;
  gap: 10px;
}

.organization-item {
  border-bottom: 1px solid #eee;
  padding: 5px 0;
}
</style>
