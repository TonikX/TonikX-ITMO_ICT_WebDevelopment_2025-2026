<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="pa-4">
          <v-card-title class="text-center"
            >Parks Management System</v-card-title
          >
          <v-card-subtitle class="text-center"
            >Efficient management of parks</v-card-subtitle
          >

          <v-card-text>
            <v-alert type="info" class="mb-4">Authorization required</v-alert>

            <div class="text-center mb-4">
              <v-btn :to="{ name: 'login' }" color="primary" class="mr-2"
                >Sign In</v-btn
              >
              <v-btn :to="{ name: 'register' }" color="secondary"
                >Create Account</v-btn
              >
            </div>

            <v-divider class="my-4"></v-divider>

            <v-card variant="outlined">
              <v-card-text>
                <p class="font-weight-bold">Demo credentials:</p>
                <p>User: user / user123</p>
              </v-card-text>
            </v-card>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useAuthStore } from "@/store/auth";
const auth = useAuthStore();
</script>
