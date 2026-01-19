<template>
  <v-navigation-drawer app permanent width="280">
    <v-list nav density="comfortable">
      <v-list-item title="DjangoSchool" subtitle="Hotel Frontend" />
      <v-divider class="my-2" />

      <v-list-item to="/" title="Главная" />
      <v-list-item to="/profile" title="Профиль" />

      <v-divider class="my-2" />
      <v-list-subheader>CRUD</v-list-subheader>
      <v-list-item to="/rooms" title="Rooms" />
      <v-list-item to="/clients" title="Clients" />
      <v-list-item to="/stays" title="Stays" />
      <v-list-item to="/employees" title="Employees" />
      <v-list-item to="/schedules" title="Schedules" />

      <v-divider class="my-2" />
      <v-list-subheader>Analytics</v-list-subheader>
      <v-list-item to="/analytics/free-rooms" title="Free rooms" />
      <v-list-item to="/analytics/clients-from-city" title="Clients from city" />
      <v-list-item to="/analytics/clients-in-room" title="Clients in room" />
      <v-list-item to="/analytics/who-cleaned" title="Who cleaned" />
      <v-list-item to="/analytics/clients-overlap" title="Clients overlap" />

      <v-divider class="my-2" />
      <v-list-subheader>Reports</v-list-subheader>
      <v-list-item to="/reports/quarter" title="Quarter report" />
    </v-list>

    <template #append>
      <div class="pa-2">
        <v-btn block variant="tonal" @click="logout">Logout</v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const auth = useAuthStore();
const router = useRouter();

function logout() {
  auth.logout();
  router.push("/login");
}
</script>