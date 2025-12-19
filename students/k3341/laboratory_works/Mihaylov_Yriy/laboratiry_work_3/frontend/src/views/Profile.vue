<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8" offset-md="2">
        <!-- Карточка с данными пользователя -->
        <v-card class="mb-6">
          <v-card-title class="headline">
            <v-icon class="mr-2">mdi-account-circle</v-icon>
            Мой профиль
          </v-card-title>

          <v-card-text v-if="loading">
            <v-progress-linear indeterminate color="primary"></v-progress-linear>
            <div class="text-center mt-4">Загрузка данных профиля...</div>
          </v-card-text>

          <v-card-text v-else>
            <!-- Информация о пользователе в виде списка -->
            <v-list lines="two" density="comfortable">
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-identifier</v-icon>
                </template>
                <v-list-item-title>ID пользователя</v-list-item-title>
                <v-list-item-subtitle>{{ profileData.id }}</v-list-item-subtitle>
              </v-list-item>

              <v-divider></v-divider>

              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-account</v-icon>
                </template>
                <v-list-item-title>Логин</v-list-item-title>
                <v-list-item-subtitle>{{ profileData.username }}</v-list-item-subtitle>
              </v-list-item>

              <v-divider></v-divider>

              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-email</v-icon>
                </template>
                <v-list-item-title>Email</v-list-item-title>
                <v-list-item-subtitle>{{ profileData.email }}</v-list-item-subtitle>
              </v-list-item>

              <v-divider></v-divider>

              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-account-outline</v-icon>
                </template>
                <v-list-item-title>Имя</v-list-item-title>
                <v-list-item-subtitle>{{ profileData.first_name || 'Не указано' }}</v-list-item-subtitle>
              </v-list-item>

              <v-divider></v-divider>

              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-account-outline</v-icon>
                </template>
                <v-list-item-title>Фамилия</v-list-item-title>
                <v-list-item-subtitle>{{ profileData.last_name || 'Не указано' }}</v-list-item-subtitle>
              </v-list-item>

              <v-divider></v-divider>

              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-phone</v-icon>
                </template>
                <v-list-item-title>Телефон</v-list-item-title>
                <v-list-item-subtitle>{{ profileData.phone || 'Не указан' }}</v-list-item-subtitle>
              </v-list-item>

              <v-divider></v-divider>

              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-briefcase</v-icon>
                </template>
                <v-list-item-title>Должность</v-list-item-title>
                <v-list-item-subtitle>{{ profileData.position || 'Не указана' }}</v-list-item-subtitle>
              </v-list-item>

              <v-divider></v-divider>

              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-shield-account</v-icon>
                </template>
                <v-list-item-title>Статус</v-list-item-title>
                <v-list-item-subtitle>
                  <v-chip :color="profileData.is_staff ? 'green' : 'grey'" dark small>
                    {{ profileData.is_staff ? 'Персонал' : 'Пользователь' }}
                  </v-chip>
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>

            <!-- Кнопки действий -->
            <div class="d-flex flex-wrap gap-3 mt-6">
              <v-btn
                  color="warning"
                  @click="showEditProfileDialog"
                  prepend-icon="mdi-pencil"
              >
                Редактировать профиль
              </v-btn>

              <v-btn
                  color="primary"
                  @click="showChangePasswordDialog"
                  prepend-icon="mdi-lock-reset"
              >
                Сменить пароль
              </v-btn>

              <v-btn
                  color="secondary"
                  @click="$router.back()"
                  prepend-icon="mdi-arrow-left"
              >
                Назад
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалог редактирования профиля -->
    <v-dialog v-model="editProfileDialog" max-width="600">
      <v-card>
        <v-card-title>
          <v-icon class="mr-2">mdi-pencil</v-icon>
          Редактирование профиля
        </v-card-title>

        <v-card-text>
          <v-form ref="editProfileForm" v-model="editProfileValid">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                    v-model="editProfileForm.email"
                    label="Email"
                    type="email"
                    :rules="[v => /.+@.+\..+/.test(v) || 'Некорректный email']"
                    prepend-icon="mdi-email"
                    variant="outlined"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                    v-model="editProfileForm.phone"
                    label="Телефон"
                    prepend-icon="mdi-phone"
                    variant="outlined"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                    v-model="editProfileForm.first_name"
                    label="Имя"
                    prepend-icon="mdi-account-outline"
                    variant="outlined"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                    v-model="editProfileForm.last_name"
                    label="Фамилия"
                    prepend-icon="mdi-account-outline"
                    variant="outlined"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-text-field
                    v-model="editProfileForm.position"
                    label="Должность"
                    prepend-icon="mdi-briefcase"
                    variant="outlined"
                ></v-text-field>
              </v-col>
            </v-row>

            <v-alert v-if="editProfileSuccess" type="success" class="mt-4">
              <div class="d-flex align-center">
                <v-icon class="mr-2">mdi-check-circle</v-icon>
                Профиль успешно обновлен
              </div>
            </v-alert>

            <v-alert v-if="editProfileError" type="error" class="mt-4">
              <div class="d-flex align-center">
                <v-icon class="mr-2">mdi-alert-circle</v-icon>
                {{ editProfileErrorMessage }}
              </div>
            </v-alert>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="editProfileDialog = false" color="secondary">Отмена</v-btn>
          <v-btn
              @click="updateProfile"
              color="primary"
              :loading="editProfileLoading"
              :disabled="!editProfileValid || editProfileSuccess"
          >
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог смены пароля -->
    <v-dialog v-model="changePasswordDialog" max-width="600">
      <v-card>
        <v-card-title>
          <v-icon class="mr-2">mdi-lock-reset</v-icon>
          Смена пароля
        </v-card-title>

        <v-card-text>
          <v-form ref="changePasswordForm" v-model="changePasswordValid">
            <v-text-field
                v-model="changePasswordForm.current_password"
                label="Текущий пароль"
                type="password"
                :rules="[v => !!v || 'Обязательное поле']"
                required
                prepend-icon="mdi-lock"
                variant="outlined"
                class="mb-4"
            ></v-text-field>

            <v-text-field
                v-model="changePasswordForm.new_password"
                label="Новый пароль"
                type="password"
                :rules="[
                v => !!v || 'Обязательное поле'
              ]"
                required
                prepend-icon="mdi-lock-plus"
                variant="outlined"
                class="mb-4"
            ></v-text-field>

            <v-text-field
                v-model="changePasswordForm.re_new_password"
                label="Повторите новый пароль"
                type="password"
                :rules="[
                v => !!v || 'Обязательное поле',
                v => v === changePasswordForm.new_password || 'Пароли не совпадают'
              ]"
                required
                prepend-icon="mdi-lock-check"
                variant="outlined"
            ></v-text-field>

            <v-alert v-if="changePasswordSuccess" type="success" class="mt-4">
              <div class="d-flex align-center">
                <v-icon class="mr-2">mdi-check-circle</v-icon>
                Пароль успешно изменен
              </div>
            </v-alert>

            <v-alert v-if="changePasswordError" type="error" class="mt-4">
              <div class="d-flex align-center">
                <v-icon class="mr-2">mdi-alert-circle</v-icon>
                {{ changePasswordErrorMessage }}
              </div>
            </v-alert>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="changePasswordDialog = false" color="secondary">Отмена</v-btn>
          <v-btn
              @click="changePassword"
              color="primary"
              :loading="changePasswordLoading"
              :disabled="!changePasswordValid || changePasswordSuccess"
          >
            Сменить пароль
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Profile',
  data() {
    return {
      loading: true,

      // Данные пользователя
      profileData: {
        id: '',
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        phone: '',
        position: '',
        is_staff: false
      },

      // Диалог редактирования профиля
      editProfileDialog: false,
      editProfileLoading: false,
      editProfileValid: false,
      editProfileSuccess: false,
      editProfileError: false,
      editProfileErrorMessage: '',

      editProfileForm: {
        email: '',
        first_name: '',
        last_name: '',
        phone: '',
        position: ''
      },

      // Диалог смены пароля
      changePasswordDialog: false,
      changePasswordLoading: false,
      changePasswordValid: false,
      changePasswordSuccess: false,
      changePasswordError: false,
      changePasswordErrorMessage: '',

      changePasswordForm: {
        current_password: '',
        new_password: '',
        re_new_password: ''
      }
    }
  },
  methods: {
    async fetchUserProfile() {
      try {
        this.loading = true

        // Получаем данные пользователя с полным URL
        const response = await axios.get('http://localhost:8000/auth/users/me/')

        this.profileData = {
          id: response.data.id,
          username: response.data.username,
          email: response.data.email,
          first_name: response.data.first_name || '',
          last_name: response.data.last_name || '',
          phone: response.data.phone || '',
          position: response.data.position || '',
          is_staff: response.data.is_staff || false
        }

        console.log('Данные пользователя загружены:', this.profileData)

      } catch (error) {
        console.error('Ошибка загрузки профиля:', error)

        // Если 401, возможно токен истек
        if (error.response?.status === 401) {
          alert('Сессия истекла. Пожалуйста, войдите снова.')
          this.$router.push('/login')
        } else {
          alert('Не удалось загрузить данные профиля')
        }

      } finally {
        this.loading = false
      }
    },

    showEditProfileDialog() {
      // Заполняем форму текущими данными
      this.editProfileForm = {
        email: this.profileData.email,
        first_name: this.profileData.first_name,
        last_name: this.profileData.last_name,
        phone: this.profileData.phone,
        position: this.profileData.position
      }

      this.editProfileDialog = true
      this.editProfileError = false
      this.editProfileSuccess = false

      // Сбрасываем валидацию формы
      if (this.$refs.editProfileForm) {
        this.$refs.editProfileForm.resetValidation()
      }
    },

    showChangePasswordDialog() {
      this.changePasswordDialog = true
      this.changePasswordError = false
      this.changePasswordSuccess = false
      this.changePasswordForm = {
        current_password: '',
        new_password: '',
        re_new_password: ''
      }

      // Сбрасываем валидацию формы
      if (this.$refs.changePasswordForm) {
        this.$refs.changePasswordForm.resetValidation()
      }
    },

    async updateProfile() {
      if (!this.$refs.editProfileForm.validate()) return

      this.editProfileLoading = true
      this.editProfileSuccess = false
      this.editProfileError = false
      this.editProfileErrorMessage = ''

      try {
        // Подготавливаем данные для отправки
        const payload = {
          email: this.editProfileForm.email,
          first_name: this.editProfileForm.first_name,
          last_name: this.editProfileForm.last_name,
          phone: this.editProfileForm.phone,
          position: this.editProfileForm.position
        }

        console.log('Обновляем профиль:', payload)

        // Отправляем PATCH запрос с полным URL
        const response = await axios.patch('http://localhost:8000/auth/users/me/', payload)

        this.editProfileSuccess = true
        console.log('Профиль обновлен:', response.data)

        // Обновляем данные пользователя
        this.profileData.email = response.data.email
        this.profileData.first_name = response.data.first_name || ''
        this.profileData.last_name = response.data.last_name || ''
        this.profileData.phone = response.data.phone || ''
        this.profileData.position = response.data.position || ''

        // Закрываем диалог через 2 секунды
        setTimeout(() => {
          this.editProfileDialog = false
          this.editProfileSuccess = false
        }, 2000)

      } catch (error) {
        console.error('Ошибка обновления профиля:', error)
        this.editProfileError = true

        if (error.response?.status === 400) {
          // Ошибки валидации от Djoser
          const errors = Object.values(error.response.data).flat()
          this.editProfileErrorMessage = errors.join(', ') || 'Ошибка валидации данных'
        } else if (error.response?.data?.detail) {
          this.editProfileErrorMessage = error.response.data.detail
        } else if (error.response?.status === 401) {
          this.editProfileErrorMessage = 'Сессия истекла. Пожалуйста, войдите снова.'
          setTimeout(() => {
            this.$router.push('/login')
          }, 2000)
        } else {
          this.editProfileErrorMessage = 'Ошибка при обновлении профиля'
        }
      } finally {
        this.editProfileLoading = false
      }
    },

    async changePassword() {
      if (!this.$refs.changePasswordForm.validate()) return

      this.changePasswordLoading = true
      this.changePasswordSuccess = false
      this.changePasswordError = false
      this.changePasswordErrorMessage = ''

      try {
        // Подготавливаем данные для отправки
        const payload = {
          current_password: this.changePasswordForm.current_password,
          new_password: this.changePasswordForm.new_password,
          re_new_password: this.changePasswordForm.re_new_password
        }

        console.log('Меняем пароль:', {...payload, new_password: '***', re_new_password: '***'})

        // Отправляем POST запрос с полным URL
        const response = await axios.post('http://localhost:8000/auth/users/set_password/', payload)

        this.changePasswordSuccess = true
        console.log('Пароль изменен:', response.data)

        // Закрываем диалог через 2 секунды
        setTimeout(() => {
          this.changePasswordDialog = false
          this.changePasswordSuccess = false
        }, 2000)

      } catch (error) {
        console.error('Ошибка смены пароля:', error)
        this.changePasswordError = true

        if (error.response?.status === 400) {
          // Ошибки валидации от Djoser
          if (error.response.data.current_password) {
            this.changePasswordErrorMessage = error.response.data.current_password[0] || 'Неверный текущий пароль'
          } else if (error.response.data.new_password) {
            this.changePasswordErrorMessage = error.response.data.new_password[0] || 'Ошибка валидации нового пароля'
          } else {
            const errors = Object.values(error.response.data).flat()
            this.changePasswordErrorMessage = errors.join(', ') || 'Ошибка валидации данных'
          }
        } else if (error.response?.data?.detail) {
          this.changePasswordErrorMessage = error.response.data.detail
        } else if (error.response?.status === 401) {
          this.changePasswordErrorMessage = 'Сессия истекла. Пожалуйста, войдите снова.'
          setTimeout(() => {
            this.$router.push('/login')
          }, 2000)
        } else {
          this.changePasswordErrorMessage = 'Ошибка при смене пароля'
        }
      } finally {
        this.changePasswordLoading = false
      }
    }
  },
  mounted() {
    this.fetchUserProfile()
  }
}
</script>

<style scoped>
.gap-3 {
  gap: 12px;
}

.v-list-item {
  min-height: 56px;
}
</style>