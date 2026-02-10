<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { tokenStore } from "@/stores/token.js";

const token = tokenStore();

const profile = ref({
  username: "",
  email: "",
});

const passwords = ref({
  current_password: "",
  new_password: "",
});

async function loadProfile() {
  const res = await axios.get("/auth/users/me/", {
    headers: {
      Authorization: `Token ${token.token}`,
    },
  });
  profile.value.username = res.data.username;
  profile.value.email = res.data.email;
}
async function updateProfile() {
  try {
    await axios.patch(
      "/auth/users/me/",
      {
        username: profile.value.username,
        email: profile.value.email,
      },
      {
        headers: {
          Authorization: `Token ${token.token}`,
        },
      }
    );
    alert("Профиль обновлён");
  } catch (e) {
    console.error(e.response?.data || e);
    alert("Ошибка обновления профиля");
  }
}

async function changePassword() {
  try {
    await axios.post(
      "/auth/users/set_password/",
      {
        current_password: passwords.value.current_password,
        new_password: passwords.value.new_password,
      },
      {
        headers: {
          Authorization: `Token ${token.token}`,
        },
      }
    );

    alert("Пароль успешно изменён");
    passwords.value.current_password = "";
    passwords.value.new_password = "";
  } catch (error) {
    console.error("Ошибка смены пароля:", error.response?.data || error);
    alert("Ошибка при смене пароля");
  }
}



onMounted(loadProfile);
</script>

<template>
  <v-container>
    <h2>Профиль</h2>

    <v-card class="pa-4 mb-6">
      <h3>Основные данные</h3>
      <v-text-field label="Логин" v-model="profile.username" />
      <v-text-field label="Email" v-model="profile.email" />
      <v-btn color="primary" @click="updateProfile">Сохранить</v-btn>
    </v-card>

    <v-card class="pa-4">
      <h3>Смена пароля</h3>
      <v-text-field
        label="Текущий пароль"
        type="password"
        v-model="passwords.current_password"
      />
      <v-text-field
        label="Новый пароль"
        type="password"
        v-model="passwords.new_password"
      />
      <v-btn color="error" @click="changePassword">Сменить пароль</v-btn>
    </v-card>
  </v-container>
</template>
