<template>
  <v-container class="d-flex align-center justify-center" style="height: 80vh;">
    <v-card width="100%" max-width="500" class="pa-4">
      <v-card-title class="text-h5 text-center mb-4">
        Регистрация
      </v-card-title>

      <v-form @submit.prevent="handleRegister">
        <v-card-text>
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                  v-model="firstName"
                  label="Имя"
                  variant="outlined"
                  required
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                  v-model="lastName"
                  label="Фамилия"
                  variant="outlined"
              />
            </v-col>

            <v-col cols="12">
              <v-text-field
                  v-model="username"
                  label="Логин (username)"
                  variant="outlined"
                  :rules="[v => !!v || 'Обязательно']"
                  required
              />
            </v-col>

            <v-col cols="12">
              <v-text-field
                  v-model="email"
                  label="Email"
                  type="email"
                  variant="outlined"
                  :rules="[v => !!v || 'Обязательно']"
                  required
              />
            </v-col>

            <v-col cols="12">
              <v-text-field
                  v-model="phone"
                  label="Телефон"
                  variant="outlined"
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                  v-model="password"
                  label="Пароль"
                  :type="showPassword ? 'text' : 'password'"
                  variant="outlined"
                  :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                  @click:append-inner="showPassword = !showPassword"
                  :rules="[v => !!v || 'Обязательно']"
                  required
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                  v-model="confirmPassword"
                  label="Подтверждение"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  variant="outlined"
                  :append-inner-icon="showConfirmPassword ? 'mdi-eye-off' : 'mdi-eye'"
                  @click:append-inner="showConfirmPassword = !showConfirmPassword"
                  :rules="[v => !!v || 'Обязательно', v => v === password || 'Не совпадает']"
                  required
              />
            </v-col>
          </v-row>

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
            Зарегистрироваться
          </v-btn>

          <div class="text-center mt-4">
            <router-link to="/login" class="text-primary">
              Войти
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
  name: 'RegisterView',

  data() {
    return {
      firstName: '',
      lastName: '',
      username: '',
      email: '',
      phone: '',
      password: '',
      confirmPassword: '',
      showPassword: false,
      showConfirmPassword: false
    }
  },

  computed: {
    ...mapGetters(['isLoading', 'authError'])
  },

  methods: {
    ...mapActions(['register']),

    async handleRegister() {
      if (!this.username || !this.email || !this.password) {
        return
      }

      if (this.password !== this.confirmPassword) {
        return
      }

      const userData = {
        email: this.email,
        first_name: this.firstName,
        last_name: this.lastName,
        username: this.username,
        phone: this.phone || '',
        password: this.password
      }

      const result = await this.register(userData)

      if (result.success) {
        this.$router.push('/')
      }
    }
  }
}
</script>