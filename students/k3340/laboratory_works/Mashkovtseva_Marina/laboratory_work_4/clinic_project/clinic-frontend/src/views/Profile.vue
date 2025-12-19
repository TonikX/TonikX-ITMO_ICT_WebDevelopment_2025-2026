<template>
  <div style="width: 100%;">
    <v-card width="100%" class="pa-6" elevation="2" style="max-width: 1200px; margin: 0 auto;">
      <v-card-title class="headline font-weight-bold">Профиль</v-card-title>

      <v-card-text>
        <v-text-field
          label="Имя пользователя"
          v-model="user.username"
          disabled
          outlined
          class="mb-4"
          style="width: 100%; min-width: 500px;"
        />

        <v-text-field
          label="Email"
          v-model="email"
          outlined
          class="mb-4"
          style="width: 100%; min-width: 500px;"
        />

        <v-btn color="primary" class="mt-2" @click="updateEmail">
          Сохранить email
        </v-btn>

        <v-divider class="my-4" />

        <v-text-field
          label="Старый пароль"
          v-model="password.old"
          type="password"
          outlined
          class="mb-4"
          style="width: 100%; min-width: 500px;"
        />

        <v-text-field
          label="Новый пароль"
          v-model="password.new"
          type="password"
          outlined
          class="mb-4"
          style="width: 100%; min-width: 500px;"
        />

        <v-btn color="error" class="mt-2" @click="changePassword">
          Сменить пароль
        </v-btn>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn text @click="logout">Выйти</v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import api from "../api/axios";

export default {
  data() {
    return {
      user: {},
      email: "",
      password: {
        old: "",
        new: "",
      },
    };
  },
  async mounted() {
    const res = await api.get("/auth/users/me/");
    this.user = res.data;
    this.email = res.data.email;
  },
  methods: {
    async updateEmail() {
      await api.patch("/auth/users/me/", {
        email: this.email,
      });
      alert("Email обновлён");
    },

    async changePassword() {
      await api.post("/auth/users/set_password/", {
        current_password: this.password.old,
        new_password: this.password.new,
      });

      alert("Пароль изменён");
      this.password.old = "";
      this.password.new = "";
    },

    logout() {
      localStorage.removeItem("token");
      window.location.href = "/login";
    },
  },
};
</script>