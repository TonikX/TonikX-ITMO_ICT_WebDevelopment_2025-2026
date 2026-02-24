<template>
  <v-container class="my-8">
    <h1 class="text-h4 text-center mb-6">Личный кабинет</h1>

    <v-row>
      <v-col cols="12" md="6">
        <v-card class="pa-4">
          <v-card-title class="mb-4">Профиль</v-card-title>

          <v-card-text>
            <div class="mb-3">
              <strong>Имя:</strong> {{ user.first_name || 'Не указано' }}
            </div>
            <div class="mb-3">
              <strong>Фамилия:</strong> {{ user.last_name || 'Не указано' }}
            </div>
            <div class="mb-3">
              <strong>Логин:</strong> {{ user.username }}
            </div>
            <div class="mb-3">
              <strong>Email:</strong> {{ user.email }}
            </div>
            <div class="mb-3">
              <strong>Телефон:</strong> {{ user.phone || 'Не указан' }}
            </div>
            <div class="mb-3">
              <strong>Роль:</strong> {{ user.role }}
            </div>
            <div class="mb-3">
              <strong>Дата регистрации:</strong> {{ formatDate(user.date_joined) }}
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card class="pa-4">
          <v-card-title class="mb-4">Редактировать профиль</v-card-title>

          <v-form @submit.prevent="updateProfile">
            <v-card-text>
              <v-text-field
                  v-model="editForm.first_name"
                  label="Имя"
                  variant="outlined"
                  class="mb-3"
              />

              <v-text-field
                  v-model="editForm.last_name"
                  label="Фамилия"
                  variant="outlined"
                  class="mb-3"
              />

              <v-text-field
                  v-model="editForm.phone"
                  label="Телефон"
                  variant="outlined"
                  class="mb-3"
              />

              <v-alert
                  v-if="updateError"
                  type="error"
                  density="compact"
                  class="mb-4"
              >
                <div v-for="(value, key) in updateError" :key="key">
                  {{ Array.isArray(value) ? value[0] : value }}
                </div>
              </v-alert>

              <v-alert
                  v-if="updateSuccess"
                  type="success"
                  density="compact"
                  class="mb-4"
              >
                Профиль обновлен
              </v-alert>

              <v-btn
                  type="submit"
                  color="primary"
                  :loading="isLoading"
              >
                Сохранить
              </v-btn>
            </v-card-text>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import axios from 'axios'

export default {
  name: 'ProfileView',

  data() {
    return {
      editForm: {
        first_name: '',
        last_name: '',
        phone: ''
      },
      updateSuccess: false,
      updateError: null,
      updateLoading: false
    }
  },

  computed: {
    ...mapGetters(['userData', 'isLoading']),

    user() {
      return this.userData || {}
    }
  },

  watch: {
    user: {
      immediate: true,
      handler(newUser) {
        if (newUser) {
          this.editForm = {
            first_name: newUser.first_name || '',
            last_name: newUser.last_name || '',
            phone: newUser.phone || ''
          }
        }
      }
    }
  },

  methods: {
    ...mapActions(['updateProfile']),

    async updateProfile() {
      this.updateSuccess = false
      this.updateError = null
      this.updateLoading = true

      try {
        const response = await axios.patch(`/auth/users/${this.user.id}/`, this.editForm)

        this.$store.commit('SET_USER', response.data)
        localStorage.setItem('user', JSON.stringify(response.data))

        this.updateSuccess = true

        setTimeout(() => {
          this.updateSuccess = false
        }, 3000)

      } catch (error) {
        console.error('Ошибка обновления профиля:', error)
        this.updateError = error.response?.data || {detail: 'Ошибка обновления'}
      } finally {
        this.updateLoading = false
      }
    },

    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU') + ' ' + date.toLocaleTimeString('ru-RU')
    }
  }
}
</script>