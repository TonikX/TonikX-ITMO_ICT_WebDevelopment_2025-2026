<template>
  <v-container class="d-flex align-center justify-center" style="height: 80vh;">
    <v-card width="100%" max-width="400" class="pa-4">
      <v-card-title class="text-h5 text-center mb-4">
        Вход
      </v-card-title>

      <v-form @submit.prevent="handleLogin">
        <v-card-text>
          <v-text-field
              v-model="email"
              label="Username"
              type="username"
              variant="outlined"
              :rules="[v => !!v || 'Обязательно']"
              required
              class="mb-4"
          />

          <v-text-field
              v-model="password"
              label="Пароль"
              :type="showPassword ? 'text' : 'password'"
              variant="outlined"
              :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append-inner="showPassword = !showPassword"
              :rules="[v => !!v || 'Обязательно']"
              required
              class="mb-4"
          />

          <v-alert
              v-if="authError"
              type="error"
              density="compact"
              class="mb-4"
          >
            <div v-for="(value, key) in authError" :key="key">
              {{ Array.isArray(value) ? value[0] : value }}
            </div>
          </v-alert>

          <v-btn
              type="submit"
              color="primary"
              block
              :loading="isLoading"
          >
            Войти
          </v-btn>

          <div class="text-center mt-4">
            <router-link to="/register" class="text-primary">
              Регистрация
            </router-link>
          </div>
        </v-card-text>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'LoginView',

  data() {
    return {
      email: '',
      password: '',
      showPassword: false
    }
  },

  computed: {
    ...mapGetters(['isLoading', 'authError'])
  },

  methods: {
    ...mapActions(['login']),

    async handleLogin() {
      if (!this.email || !this.password) {
        return
      }

      const result = await this.login({
        email: this.email,
        password: this.password
      })

      if (result.success) {
        this.$router.push('/')
      }
    }
  }
}
</script>