<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '../../store/auth'

const auth = useAuthStore()
const user = computed(() => auth.user)

const handleLogout = async () => {
  await auth.logout()
}
</script>

<template>
  <v-container class="py-8">
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="text-h6">Profile</v-card-title>
          <v-card-text>
            <v-list density="compact">
              <v-list-item>
                <v-list-item-title>Username</v-list-item-title>
                <v-list-item-subtitle>{{ user?.username }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Email</v-list-item-title>
                <v-list-item-subtitle>{{ user?.email || '—' }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn color="primary" @click="handleLogout">Logout</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

