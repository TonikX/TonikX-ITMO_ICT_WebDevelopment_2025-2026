<!-- views/LoginView.vue -->
<template>
  <v-container class="fill-height">
    <v-responsive class="align-center text-center fill-height">
      <v-card
        class="mx-auto pa-6"
        max-width="450"
        elevation="8"
      >
        <v-card-item>

          <v-card-title class="text-h4 font-weight-bold">
            Добро пожаловать!
          </v-card-title>

        </v-card-item>

        <v-card-text>
          <RegisterForm />
        </v-card-text>

        <v-divider class="my-4"></v-divider>

        <v-card-actions class="justify-center">
          <span class="text-body-2 mr-2">Есть аккаунт?</span>
          <v-btn
            to="/login"
            variant="text"
            color="primary"
          >
            Войти
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-responsive>
  </v-container>
</template>

<script setup>
import RegisterForm from '@/components/Auth/RegisterForm.vue'
</script>