<template>
  <v-container>
    <h1>Профиль</h1>

    <v-card v-if="user && ! isEditing" class="pa-4">
      <v-card-text>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Username:</strong> {{ user.username }}</p>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="isEditing = true">Редактировать</v-btn>
      </v-card-actions>
    </v-card>

    <v-card v-if="isEditing" class="pa-4">
      <v-card-title>Редактировать профиль</v-card-title>
      <v-card-text>
        <v-alert v-if="errorMessage" type="error" closable @click:close="errorMessage = ''">
          {{ errorMessage }}
        </v-alert>

        <v-alert v-if="successMessage" type="success" closable @click:close="successMessage = ''">
          {{ successMessage }}
        </v-alert>

        <v-form @submit.prevent="saveProfile">
          <v-text-field
            v-model="form.email"
            label="Email"
            type="email"
            required
          ></v-text-field>
          <v-text-field
            v-model="form.username"
            label="Username"
            required
          ></v-text-field>

          <v-divider class="my-4"></v-divider>
          <h3>Текущий пароль (требуется для изменения username или пароля)</h3>

          <v-text-field
            v-model="passwordForm.current_password"
            label="Текущий пароль"
            type="password"
          ></v-text-field>

          <v-divider class="my-4"></v-divider>
          <h3>Сменить пароль (необязательно)</h3>

          <v-text-field
            v-model="passwordForm.new_password"
            label="Новый пароль"
            type="password"
          ></v-text-field>
          <v-text-field
            v-model="passwordForm. re_new_password"
            label="Подтвердите новый пароль"
            type="password"
          ></v-text-field>

          <v-card-actions>
            <v-btn type="submit" color="primary">Сохранить</v-btn>
            <v-btn @click="cancelEdit" color="grey">Отмена</v-btn>
          </v-card-actions>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      isEditing: false,
      form: {
        email: "",
        username: "",
      },
      passwordForm: {
        current_password: "",
        new_password: "",
        re_new_password: "",
      },
      errorMessage: "",
      successMessage: "",
    };
  },
  computed: {
    user() {
      return this.$store.state.auth.user;
    },
  },
  async created() {
    await this.$store.dispatch("auth/getProfile");
    if (this.user) {
      this.form.email = this.user.email;
      this.form.username = this.user.username;
    }
  },
  methods: {
    async saveProfile() {
      this.errorMessage = "";
      this.successMessage = "";

      try {
        if (this. form.username !== this.user.username && ! this.passwordForm.current_password) {
          this.errorMessage = "Для изменения username необходимо ввести текущий пароль";
          return;
        }

        console.log("Saving profile with data:", this.form, this.passwordForm);

        await this.$store.dispatch("auth/updateProfile", {
          email: this.form.email,
          username: this.form.username,
          current_password: this.passwordForm.current_password,
        });

        if (this.passwordForm.new_password) {
          if (! this.passwordForm.current_password) {
            this. errorMessage = "Для смены пароля необходимо ввести текущий пароль";
            return;
          }

          if (this.passwordForm.new_password !== this.passwordForm.re_new_password) {
            this.errorMessage = "Новые пароли не совпадают";
            return;
          }

          await this.$store.dispatch("auth/changePassword", {
            current_password: this.passwordForm.current_password,
            new_password: this.passwordForm.new_password,
            re_new_password: this.passwordForm.re_new_password,
          });
        }

        this.successMessage = "Профиль успешно обновлён";

        this.passwordForm = {
          current_password: "",
          new_password: "",
          re_new_password: "",
        };

        setTimeout(() => {
          this.isEditing = false;
        }, 1500);

      } catch (error) {
        console.error("Ошибка обновления профиля:", error);

        if (error.response && error.response.data) {
          const errors = error.response.data;
          if (errors.detail) {
            this.errorMessage = errors.detail;
          } else if (errors.current_password) {
            this.errorMessage = "Неверный текущий пароль";
          } else {
            this.errorMessage = JSON.stringify(errors);
          }
        } else {
          this.errorMessage = "Произошла ошибка при сохранении данных";
        }
      }
    },
    cancelEdit() {
      this.isEditing = false;
      this.errorMessage = "";
      this.successMessage = "";

      if (this.user) {
        this.form.email = this. user.email;
        this. form.username = this.user. username;
      }

      this.passwordForm = {
        current_password: "",
        new_password: "",
        re_new_password: "",
      };
    },
  },
};
</script>