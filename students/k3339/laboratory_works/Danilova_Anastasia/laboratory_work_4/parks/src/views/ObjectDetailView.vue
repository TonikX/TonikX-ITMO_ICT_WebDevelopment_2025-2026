<template>
  <v-container>
    <div v-if="object">
      <div class="d-flex justify-space-between mb-4">
        <v-btn @click="$router.push('/dashboard')">Back to Dashboard</v-btn>
        <v-btn @click="goToEdit" color="primary">Edit Object</v-btn>
      </div>

      <v-card class="mb-6">
        <v-card-title>{{ object.name }}</v-card-title>
        <v-card-text>
          <p>{{ object.address }}</p>
          <p>
            <strong>Status:</strong>
            <v-chip :color="object.is_serviced ? 'green' : 'grey'">
              {{ object.is_serviced ? "Under Service" : "Not Serviced" }}
            </v-chip>
          </p>
        </v-card-text>
      </v-card>

      <v-tabs v-model="tab" class="mb-6">
        <v-tab value="plants">Plants</v-tab>
        <v-tab value="contracts">Contracts</v-tab>
      </v-tabs>

      <v-window v-model="tab">
        <v-window-item value="plants">
          <PlantList :objectId="object.id" />
        </v-window-item>
        <v-window-item value="contracts">
          <ObjectContracts :objectId="object.id" />
        </v-window-item>
      </v-window>
    </div>

    <div v-else class="text-center">Loading...</div>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth";
import { getObjectById } from "@/services/objectsService";
import PlantList from "@/components/PlantList.vue";
import ObjectContracts from "@/components/ObjectContracts.vue";

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();

const object = ref(null);
const tab = ref("plants");
const loading = ref(true);
const error = ref(null);

const goToEdit = () => {
  router.push(`/objects/${route.params.id}/edit`);
};

onMounted(async () => {
  try {
    loading.value = true;
    object.value = await getObjectById(route.params.id, auth.token);
  } catch (err) {
    console.error("Failed to load object:", err);
    error.value = "Failed to load object data";
  } finally {
    loading.value = false;
  }
});
</script>
