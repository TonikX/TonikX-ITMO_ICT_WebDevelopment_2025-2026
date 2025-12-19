<template>
  <v-container>
    <v-form @submit.prevent="updateProfile">
      <v-text-field v-model="form.username" label="Username" required></v-text-field>
      <v-btn type="submit" class="ma-2" color="primary">Сохранить</v-btn>
    </v-form>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      form: {
        username: this.$store.state.auth.user.username,
      },
    };
  },
  methods: {
    async updateProfile() {
      try {
        await this.$store.dispatch("auth/updateProfile", this.form);
        this.$router.push("/profile");
      } catch (error) {
        console.error("Ошибка обновления профиля:", error);
      }
    },
  },
};
</script>