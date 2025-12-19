<template>
  <v-container>
    <v-form @submit.prevent="register">
      <v-alert v-if="errorMessage" type="error" closable @click:close="errorMessage = ''">
        {{ errorMessage }}
      </v-alert>

      <v-alert v-if="fieldErrors.length > 0" type="error" closable @click:close="fieldErrors = []">
        <ul>
          <li v-for="(error, index) in fieldErrors" :key="index">{{ error }}</li>
        </ul>
      </v-alert>

      <v-text-field v-model="form.email" label="Email" required></v-text-field>
      <v-text-field v-model="form.username" label="Username" required></v-text-field>
      <v-text-field v-model="form.password" label="Password" type="password" required></v-text-field>
      <v-btn type="submit" class="ma-2" color="primary">Зарегистрироваться</v-btn>
    </v-form>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      form: {
        email: "",
        username: "",
        password: "",
      },
      errorMessage: "",
      fieldErrors:  [],
    };
  },
  methods: {
    async register() {
      this.errorMessage = "";
      this.fieldErrors = [];

      try {
        await this.$store.dispatch("auth/register", this.form);
        this.$router.push("/login");
      } catch (error) {
        console.error("Ошибка регистрации:", error);

        if (error.response && error.response.data) {
          const errors = error.response.data;

          if (errors.detail) {
            this.errorMessage = errors.detail;
          } else {
            for (const field in errors) {
              if (Array.isArray(errors[field])) {
                errors[field].forEach((msg) => {
                  this.fieldErrors.push(`${field}: ${msg}`);
                });
              } else {
                this.fieldErrors.push(`${field}: ${errors[field]}`);
              }
            }
          }
        } else {
          this.errorMessage = "Произошла неизвестная ошибка.  Попробуйте снова.";
        }
      }
    },
  },
};
</script>