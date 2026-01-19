<template>
  <v-container>
    <div class="d-flex justify-space-between align-center mb-6">
      <div>
        <h1>Dashboard</h1>
        <p class="text-subtitle-1">
          Welcome back, {{ authStore.user?.username || "User" }}
        </p>
      </div>

      <div class="d-flex gap-2">
        <v-btn @click="router.push('/')">Back to Home</v-btn>
        <v-btn @click="router.push('/settings')" variant="outlined">
          Settings
        </v-btn>
        <v-btn @click="handleLogout" color="error">Logout</v-btn>
      </div>
    </div>

    <v-card class="mb-6">
      <v-card-title>Park Management</v-card-title>
      <v-card-subtitle
        >Select a park to view and manage its details</v-card-subtitle
      >
      <v-card-text>
        <ObjectList @select="handleSelectObject" />
      </v-card-text>
    </v-card>

    <v-card>
      <v-card-title>Quick Actions</v-card-title>
      <v-card-text>
        <v-btn @click="router.push('/objects/new')" color="primary">
          + Add New Object
        </v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth";
import ObjectList from "@/components/ObjectList.vue";

const authStore = useAuthStore();
const router = useRouter();

const handleSelectObject = (object) => {
  router.push(`/objects/${object.id}`);
};

const handleLogout = async () => {
  await authStore.logout();
  router.push("/login");
};
</script>
