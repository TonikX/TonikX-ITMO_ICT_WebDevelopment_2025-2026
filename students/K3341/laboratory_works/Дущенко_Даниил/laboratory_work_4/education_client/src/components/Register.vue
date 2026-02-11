<template>
  <v-container class="fill-height justify-center">
    <v-card width="400" class="pa-6">
      <div class="text-center mb-6">
        <h2 class="text-h5 font-weight-bold">Регистрация</h2>
      </div>

      <v-form @submit.prevent="register">
        <v-text-field v-model="username" label="Придумайте Логин" prepend-inner-icon="mdi-account-plus"></v-text-field>
        <v-text-field v-model="password" label="Пароль" type="password" prepend-inner-icon="mdi-lock"></v-text-field>
        
        <v-btn block color="success" size="large" type="submit" class="mt-4">
          Создать аккаунт
        </v-btn>
        
        <div class="text-center mt-4">
          <router-link to="/" class="text-decoration-none text-primary">
            Уже есть аккаунт? Войти
          </router-link>
        </div>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios';
export default {
  data: () => ({ username: '', password: '' }),
  methods: {
    async register() {
      try {
        await axios.post('http://127.0.0.1:8000/auth/users/', {
          username: this.username,
          password: this.password
        });
        alert('Успешно! Теперь войдите.');
        this.$router.push('/');
      } catch (e) {
        alert('Ошибка регистрации (возможно, логин занят)');
      }
    }
  }
}
</script>