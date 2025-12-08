<template>
  <v-container class="mt-10" max-width="500">
    <h2 class="mb-4">Профиль</h2>

    <!-- Основные данные -->
    <v-form @submit.prevent="saveProfile">
      <v-text-field
        v-model="username"
        label="Логин"
        disabled
      />
      <v-text-field
        v-model="email"
        label="Email"
      />

      <v-btn
        type="submit"
        color="primary"
        class="mt-4"
        :loading="savingProfile"
      >
        Сохранить профиль
      </v-btn>
    </v-form>

    <v-divider class="my-6" />

    <!-- Смена пароля -->
    <h3 class="mb-4">Смена пароля</h3>

    <v-form @submit.prevent="changePassword">
      <v-text-field
        v-model="currentPassword"
        label="Текущий пароль"
        type="password"
        required
      />
      <v-text-field
        v-model="newPassword"
        label="Новый пароль"
        type="password"
        required
      />
      <v-text-field
        v-model="newPassword2"
        label="Повтор нового пароля"
        type="password"
        required
      />

      <v-btn
        type="submit"
        color="secondary"
        class="mt-4"
        :loading="changingPassword"
      >
        Обновить пароль
      </v-btn>
    </v-form>

    <p v-if="message" class="mt-4">{{ message }}</p>
    <p v-if="error" class="mt-2" style="color: #ff5252">{{ error }}</p>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import http from "../../api/http";

const username = ref("");
const email = ref("");

const currentPassword = ref("");
const newPassword = ref("");
const newPassword2 = ref("");

const savingProfile = ref(false);
const changingPassword = ref(false);

const message = ref("");
const error = ref("");

onMounted(async () => {
  try {
    const res = await http.get("/auth/users/me/");
    username.value = res.data.username;
    email.value = res.data.email || "";
  } catch (e) {
    console.error(e);
  }
});

const saveProfile = async () => {
  savingProfile.value = true;
  message.value = "";
  error.value = "";

  try {
    await http.patch("/auth/users/me/", {
      email: email.value,
    });
    message.value = "Профиль обновлён";
  } catch (e) {
    console.error(e);
    error.value = "Ошибка обновления профиля";
  } finally {
    savingProfile.value = false;
  }
};

const changePassword = async () => {
  if (newPassword.value !== newPassword2.value) {
    error.value = "Новые пароли не совпадают";
    return;
  }

  changingPassword.value = true;
  message.value = "";
  error.value = "";

  try {
    await http.post("/auth/users/set_password/", {
      current_password: currentPassword.value,
      new_password: newPassword.value,
    });

    message.value = "Пароль успешно изменён";
    currentPassword.value = "";
    newPassword.value = "";
    newPassword2.value = "";
  } catch (e) {
    console.error(e);
    error.value = "Ошибка смены пароля (проверьте текущий пароль)";
  } finally {
    changingPassword.value = false;
  }
};
</script>