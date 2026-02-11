<template>
  <v-container class="fill-height justify-center">
    <v-card width="400" class="pa-6">
      <div class="text-center mb-6">
        <v-avatar color="primary" size="64" class="mb-4">
          <v-icon icon="mdi-account-lock" color="white" size="32"></v-icon>
        </v-avatar>
        <h2 class="text-h5 font-weight-bold">Вход в систему</h2>
      </div>

      <v-form @submit.prevent="login">
        <v-text-field 
          v-model="username" 
          label="Логин" 
          prepend-inner-icon="mdi-account"
          variant="outlined"
        ></v-text-field>
        
        <v-text-field 
          v-model="password" 
          label="Пароль" 
          type="password" 
          prepend-inner-icon="mdi-lock"
          variant="outlined"
        ></v-text-field>
        
        <v-btn block color="primary" size="large" type="submit" class="mt-2">
          Войти
        </v-btn>
      </v-form>

      <!-- ССЫЛКА НА РЕГИСТРАЦИЮ -->
      <div class="text-center mt-6">
        <span class="text-medium-emphasis">Нет аккаунта? </span>
        <router-link to="/register" class="text-primary font-weight-bold text-decoration-none">
          Зарегистрироваться
        </router-link>
      </div>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios';
export default {
  data: () => ({ username: '', password: '' }),
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/auth/token/login/', {
          username: this.username,
          password: this.password
        });
        localStorage.setItem('auth_token', response.data.auth_token);
        this.$router.push('/assignments');
      } catch (e) {
        alert('Неверный логин или пароль');
      }
    }
  }
}
</script>