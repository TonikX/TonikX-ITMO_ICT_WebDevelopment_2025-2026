<template>
  <v-container>
    <v-form @submit.prevent="login">
      <v-text-field v-model="form.username" label="User name" required></v-text-field>
      <v-text-field v-model="form.password" label="Password" type="password" required></v-text-field>
      <v-btn type="submit" class="ma-2" color="primary">Войти</v-btn>
    </v-form>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
    };
  },
  methods: {
    async login() {
      try {
        await this.$store.dispatch("auth/login", this.form);
        this.$router.push("/profile");
      } catch (error) {
        console.error("Ошибка авторизации:", error);
      }
    },
  },
};
</script>