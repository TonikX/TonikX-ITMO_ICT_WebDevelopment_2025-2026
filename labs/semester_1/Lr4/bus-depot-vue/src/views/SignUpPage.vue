<script>
export default {
    data() {
        return {
            username: '',
            password: '',
            rePassword: '',
            isLoading: false
        }
    },
    methods: {
        async createAccount() {
            if (this.password !== this.rePassword) {
                alert('Пароли не совпадают');
                return;
            }

            const userData = {
                username: this.username,
                password: this.password,
                re_password: this.rePassword
            };

            this.isLoading = true;

            try {
                const response = await fetch('http://127.0.0.1:8000/auth/users/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(userData)
                });

                if (response.ok) {
                    alert('Аккаунт успешно создан. Теперь вы можете войти в него.');
                    this.$router.push('/login');
                } else {
                    console.log(await response.json());
                    alert("Ошибка при создании аккаунта");
                }
            } catch (error) {
                alert("Ошибка соединения с сервером");
            } finally {
                this.isLoading = false;
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
            <span class="text-h4">Регистрация</span>
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

            <v-text-field
              v-model="rePassword"
              label="Повторить пароль"
              type="password"
              :disabled="isLoading"
              outlined
              clearable
            ></v-text-field>

            <v-btn
              block
              color="primary"
              @click="createAccount"
              :disabled="isLoading || !username || !password || !rePassword"
              :loading="isLoading"
              large
            >
              Создать аккаунт
            </v-btn>

            <div class="text-center mt-4">
              <router-link to="/login" class="text-decoration-none">
                Войти
              </router-link>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
