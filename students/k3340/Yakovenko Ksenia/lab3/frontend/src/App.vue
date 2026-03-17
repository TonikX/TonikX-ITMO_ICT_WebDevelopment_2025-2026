<template>
  <v-app>
    <v-app-bar>
      <v-app-bar-title>Employment Exchange</v-app-bar-title>
      <v-spacer />
      <v-btn variant="text" to="/vacancies">Vacancies</v-btn>
      <v-btn variant="text" to="/applicants">Applicants</v-btn>
      <v-btn variant="text" to="/applicants/manage">Manage Applicants</v-btn>
      <v-btn variant="text" to="/analytics">Analytics</v-btn>
      <v-divider vertical class="mx-2" />
      <v-btn variant="text" to="/login">Login</v-btn>
      <v-btn variant="text" to="/register">Register</v-btn>
      <v-btn variant="text" to="/account">Account</v-btn>
    </v-app-bar>

    <v-main>
      <v-container class="py-6">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>