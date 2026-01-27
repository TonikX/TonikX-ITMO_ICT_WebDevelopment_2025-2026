<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-breadcrumbs :items="breadcrumbs" class="pl-0">
          <template v-slot:divider>
            <v-icon>mdi-chevron-right</v-icon>
          </template>
        </v-breadcrumbs>

        <v-card>
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>
              <v-icon class="mr-2">mdi-account-cog</v-icon>
              Профиль пользователя
            </v-toolbar-title>
            <v-spacer />
            <v-btn icon @click="editMode = !editMode">
              <v-icon>{{ editMode ? 'mdi-close' : 'mdi-pencil' }}</v-icon>
            </v-btn>
          </v-toolbar>

          <v-card-text class="pa-6">
            <v-form ref="form" v-model="valid" @submit.prevent="saveProfile">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="profile.first_name"
                    label="Имя"
                    :rules="[rules.required]"
                    variant="outlined"
                    :readonly="!editMode"
                    :disabled="loading"
                    class="mb-4"
                  />
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="profile.last_name"
                    label="Фамилия"
                    :rules="[rules.required]"
                    variant="outlined"
                    :readonly="!editMode"
                    :disabled="loading"
                    class="mb-4"
                  />
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="profile.username"
                    label="Имя пользователя"
                    :rules="[rules.required]"
                    variant="outlined"
                    :readonly="!editMode"
                    :disabled="loading"
                    class="mb-4"
                  />
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="profile.email"
                    label="Email"
                    :rules="[rules.required, rules.email]"
                    variant="outlined"
                    :readonly="!editMode"
                    :disabled="loading"
                    class="mb-4"
                  />
                </v-col>
              </v-row>

              <v-divider class="my-6" />

              <h3 class="text-h6 mb-4">Смена пароля</h3>

              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="passwords.current_password"
                    label="Текущий пароль"
                    :type="showPassword ? 'text' : 'password'"
                    :rules="editPassword ? [rules.required] : []"
                    variant="outlined"
                    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                    @click:append="showPassword = !showPassword"
                    :disabled="loading"
                    class="mb-4"
                  />
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="passwords.new_password"
                    label="Новый пароль"
                    :type="showPassword ? 'text' : 'password'"
                    :rules="editPassword ? [rules.required, rules.minLength(6)] : []"
                    variant="outlined"
                    :disabled="loading"
                    class="mb-4"
                  />
                </v-col>
              </v-row>

              <v-alert
                v-if="error"
                type="error"
                density="compact"
                class="mb-4"
              >
                {{ error }}
              </v-alert>

              <v-alert
                v-if="success"
                type="success"
                density="compact"
                class="mb-4"
              >
                {{ success }}
              </v-alert>

              <div v-if="editMode" class="d-flex justify-end gap-2">
                <v-btn color="grey" @click="cancelEdit" :disabled="loading">
                  Отмена
                </v-btn>
                <v-btn color="primary" type="submit" :loading="loading" :disabled="!valid || loading">
                  Сохранить изменения
                </v-btn>
              </div>
            </v-form>
          </v-card-text>

          <v-card-actions class="pa-4 bg-grey-lighten-4">
            <div class="d-flex align-center">
              <v-icon color="grey" class="mr-2">mdi-calendar</v-icon>
              <span class="text-caption text-grey">Аккаунт создан: {{ formatDate(profile.date_joined) }}</span>
            </div>
            <v-spacer />
            <v-btn color="error" variant="text" @click="logout">
              <v-icon left>mdi-logout</v-icon>
              Выйти
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'Profile',
  data() {
    return {
      valid: false,
      loading: false,
      editMode: false,
      editPassword: false,
      showPassword: false,
      error: null,
      success: null,
      profile: {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        date_joined: ''
      },
      passwords: {
        current_password: '',
        new_password: ''
      },
      rules: {
        required: value => !!value || 'Обязательное поле',
        minLength: min => value => (value && value.length >= min) || `Минимум ${min} символов`,
        email: value => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          return pattern.test(value) || 'Некорректный email'
        }
      }
    }
  },
  computed: {
    ...mapState('auth', ['user']),
    breadcrumbs() {
      return [
        { title: 'Главная', to: '/dashboard' },
        { title: 'Профиль', disabled: true }
      ]
    }
  },
  watch: {
    user: {
      immediate: true,
      handler(newUser) {
        if (newUser) {
          this.profile = { ...newUser }
        }
      }
    }
  },
  methods: {
    ...mapActions('auth', ['updateProfile', 'logout']),
    notify(type, message) {
      if (this.$toast && typeof this.$toast[type] === 'function') {
        this.$toast[type](message)
      }
    },

    async saveProfile() {
      if (!this.$refs.form.validate()) return

      this.loading = true
      this.error = null
      this.success = null

      try {
        const result = await this.$store.dispatch('auth/updateProfile', this.profile)

        if (result.success) {
          this.success = 'Профиль успешно обновлен'
          this.editMode = false
          this.notify('success', 'Профиль обновлен')
        } else {
          this.error = result.error?.detail || 'Ошибка обновления профиля'
          this.notify('error', 'Ошибка обновления')
        }
      } catch (err) {
        this.error = 'Ошибка подключения к серверу'
        this.notify('error', 'Сервер не отвечает')
      } finally {
        this.loading = false
      }
    },

    cancelEdit() {
      this.editMode = false
      this.profile = { ...this.user }
      this.passwords = {
        current_password: '',
        new_password: ''
      }
      this.error = null
      this.success = null
    },

    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    },

    async logout() {
      await this.$store.dispatch('auth/logout')
      this.$router.push('/login')
    }
  }
}
</script>