<script>
export default {
    data() {
        return {
            username: '',
            password: '',
            isLoading: false
        }
    },

    methods: {
        async login() {
            this.isLoading = true

            try {
                const response = await fetch('http://127.0.0.1:8000/auth/token/login/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username: this.username,
                        password: this.password
                    })
                })

                const data = await response.json()

                if (response.ok && data.auth_token) {
                    localStorage.setItem('auth_token', data.auth_token)
                    localStorage.setItem('username', this.username)
                    console.log('Токен сохранён:', data.auth_token)
                    this.$router.push('/main')
                } else {
                    alert("Неверные имя пользователя или пароль")
                }
            } catch (error) {
                console.log('Ошибка соединения с сервером:', error)
                alert('Ошибка соединения с сервером')
            } finally {
                this.isLoading = false
            }
        }
    }
}
</script>


<template>
  <v-container class="fill-height" fluid>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card flat>
          <v-card-title>
            <v-btn :to="{ path: '/auth' }" class="mb-4">
              <v-icon>mdi-arrow-left</v-icon>
              Отмена
            </v-btn>
            <br>
            <span class="text-h4">Вход</span>
          </v-card-title>

          <v-card-text>
            <v-text-field
              v-model="username"
              label="Логин"
              :disabled="isLoading"
              outlined
              clearable
            ></v-text-field>

            <v-text-field
              v-model="password"
              label="Пароль"
              type="password"
              :disabled="isLoading"
              outlined
              clearable
            ></v-text-field>

            <v-btn
              block
              color="primary"
              @click="login"
              :disabled="isLoading || !username || !password"
              :loading="isLoading"
              large
            >
              Войти
            </v-btn>

            <div class="text-center mt-4">
              <router-link to="/signup" class="text-decoration-none">
                Зарегистрироваться
              </router-link>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
