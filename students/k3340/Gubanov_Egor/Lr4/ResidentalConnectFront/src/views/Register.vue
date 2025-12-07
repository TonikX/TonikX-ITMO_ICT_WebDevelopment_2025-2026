<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="10" md="8" lg="6">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark>
            <v-toolbar-title>Регистрация</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleRegister">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.username"
                    label="Имя пользователя *"
                    prepend-inner-icon="mdi-account"
                    variant="outlined"
                    required
                    :error-messages="errors.username"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.email"
                    label="Email *"
                    prepend-inner-icon="mdi-email"
                    type="email"
                    variant="outlined"
                    required
                    :error-messages="errors.email"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.password"
                    label="Пароль *"
                    prepend-inner-icon="mdi-lock"
                    type="password"
                    variant="outlined"
                    required
                    :error-messages="errors.password"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.first_name"
                    label="Имя"
                    prepend-inner-icon="mdi-account"
                    variant="outlined"
                    :error-messages="errors.first_name"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.last_name"
                    label="Фамилия"
                    prepend-inner-icon="mdi-account"
                    variant="outlined"
                    :error-messages="errors.last_name"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                  <v-select
                    v-model="formData.role"
                    label="Роль *"
                    prepend-inner-icon="mdi-account-tie"
                    :items="roleOptions"
                    variant="outlined"
                    required
                    :error-messages="errors.role"
                  ></v-select>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.phone_number"
                    label="Номер телефона"
                    prepend-inner-icon="mdi-phone"
                    variant="outlined"
                    :error-messages="errors.phone_number"
                  ></v-text-field>
                </v-col>

                <v-col cols="12">
                  <v-text-field
                    v-model="formData.address"
                    label="Адрес"
                    prepend-inner-icon="mdi-home"
                    variant="outlined"
                    :error-messages="errors.address"
                  ></v-text-field>
                </v-col>
              </v-row>

              <v-alert
                v-if="errorMessage"
                type="error"
                class="mb-4"
                closable
                @click:close="errorMessage = ''"
              >
                {{ errorMessage }}
              </v-alert>

              <v-btn
                type="submit"
                color="primary"
                block
                size="large"
                :loading="loading"
                class="mt-4"
              >
                Зарегистрироваться
              </v-btn>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text to="/login">
              Уже есть аккаунт? Войти
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'Register',
  data() {
    return {
      formData: {
        username: '',
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        role: 'resident',
        phone_number: '',
        address: '',
      },
      roleOptions: [
        { title: 'Жилец', value: 'resident' },
        { title: 'Мастер', value: 'master' },
        { title: 'Диспетчер', value: 'dispatcher' },
      ],
      errors: {},
      errorMessage: '',
      loading: false,
    }
  },
  methods: {
    async handleRegister() {
      this.errors = {}
      this.errorMessage = ''
      this.loading = true

      if (!this.formData.username) {
        this.errors.username = 'Введите имя пользователя'
        this.loading = false
        return
      }

      if (!this.formData.email) {
        this.errors.email = 'Введите email'
        this.loading = false
        return
      }

      if (!this.formData.password) {
        this.errors.password = 'Введите пароль'
        this.loading = false
        return
      }

      if (!this.formData.role) {
        this.errors.role = 'Выберите роль'
        this.loading = false
        return
      }

      const dataToSend = {
        username: this.formData.username,
        email: this.formData.email,
        password: this.formData.password,
        role: this.formData.role,
      }
      
      if (this.formData.first_name) {
        dataToSend.first_name = this.formData.first_name
      }
      if (this.formData.last_name) {
        dataToSend.last_name = this.formData.last_name
      }
      if (this.formData.phone_number) {
        dataToSend.phone_number = this.formData.phone_number
      }
      if (this.formData.address) {
        dataToSend.address = this.formData.address
      }

      try {
        const authStore = useAuthStore()
        const result = await authStore.register(dataToSend)

        if (result.success) {
          this.$router.push('/')
        } else {
          this.errorMessage = result.error || 'Ошибка регистрации'
          
          if (result.fieldErrors) {
            Object.keys(result.fieldErrors).forEach((key) => {
              this.errors[key] = result.fieldErrors[key]
            })
          } else if (result.error && typeof result.error === 'string') {
            const errorParts = result.error.split(',')
            errorParts.forEach((part) => {
              const match = part.match(/(\w+):\s*(.+)/)
              if (match) {
                const fieldName = match[1].trim()
                const errorText = match[2].trim()
                if (this.errors[fieldName]) {
                  if (Array.isArray(this.errors[fieldName])) {
                    this.errors[fieldName].push(errorText)
                  } else {
                    this.errors[fieldName] = [this.errors[fieldName], errorText]
                  }
                } else {
                  this.errors[fieldName] = errorText
                }
              }
            })
          }
        }
      } catch (error) {
        console.error('Registration error:', error)
        this.errorMessage = 'Произошла ошибка при регистрации. Попробуйте еще раз.'
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

