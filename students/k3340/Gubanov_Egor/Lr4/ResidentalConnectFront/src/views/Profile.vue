<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-toolbar color="primary" dark>
            <v-toolbar-title>Мой профиль</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-tabs v-model="tab" class="mb-4">
              <v-tab value="profile">Профиль</v-tab>
              <v-tab value="password">Смена пароля</v-tab>
            </v-tabs>

            <v-window v-model="tab">
              <v-window-item value="profile">
                <v-form @submit.prevent="handleUpdateProfile">
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="formData.username"
                        label="Имя пользователя"
                        prepend-inner-icon="mdi-account"
                        variant="outlined"
                        disabled
                      ></v-text-field>
                    </v-col>

                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="formData.email"
                        label="Email"
                        prepend-inner-icon="mdi-email"
                        type="email"
                        variant="outlined"
                        required
                        :error-messages="errors.email"
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
                        label="Роль"
                        prepend-inner-icon="mdi-account-tie"
                        :items="roleOptions"
                        variant="outlined"
                        disabled
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

                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="formData.birth_date"
                        label="Дата рождения"
                        prepend-inner-icon="mdi-calendar"
                        type="date"
                        variant="outlined"
                        :error-messages="errors.birth_date"
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

                  <v-alert
                    v-if="successMessage"
                    type="success"
                    class="mb-4"
                    closable
                    @click:close="successMessage = ''"
                  >
                    {{ successMessage }}
                  </v-alert>

                  <v-btn
                    type="submit"
                    color="primary"
                    :loading="loading"
                    class="mt-4"
                  >
                    Сохранить изменения
                  </v-btn>
                </v-form>
              </v-window-item>

              <v-window-item value="password">
                <v-form @submit.prevent="handleChangePassword">
                  <v-text-field
                    v-model="passwordData.current_password"
                    label="Текущий пароль"
                    prepend-inner-icon="mdi-lock"
                    type="password"
                    variant="outlined"
                    required
                    :error-messages="passwordErrors.current_password"
                    class="mb-4"
                  ></v-text-field>

                  <v-text-field
                    v-model="passwordData.new_password"
                    label="Новый пароль"
                    prepend-inner-icon="mdi-lock"
                    type="password"
                    variant="outlined"
                    required
                    :error-messages="passwordErrors.new_password"
                    class="mb-4"
                  ></v-text-field>

                  <v-text-field
                    v-model="passwordData.confirm_password"
                    label="Подтвердите новый пароль"
                    prepend-inner-icon="mdi-lock-check"
                    type="password"
                    variant="outlined"
                    required
                    :error-messages="passwordErrors.confirm_password"
                    class="mb-4"
                  ></v-text-field>

                  <v-alert
                    v-if="passwordErrorMessage"
                    type="error"
                    class="mb-4"
                    closable
                    @click:close="passwordErrorMessage = ''"
                  >
                    {{ passwordErrorMessage }}
                  </v-alert>

                  <v-alert
                    v-if="passwordSuccessMessage"
                    type="success"
                    class="mb-4"
                    closable
                    @click:close="passwordSuccessMessage = ''"
                  >
                    {{ passwordSuccessMessage }}
                  </v-alert>

                  <v-btn
                    type="submit"
                    color="primary"
                    :loading="passwordLoading"
                    class="mt-4"
                  >
                    Изменить пароль
                  </v-btn>
                </v-form>
              </v-window-item>
            </v-window>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'Profile',
  data() {
    return {
      tab: 'profile',
      formData: {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        role: '',
        phone_number: '',
        address: '',
        birth_date: '',
      },
      roleOptions: [
        { title: 'Жилец', value: 'resident' },
        { title: 'Мастер', value: 'master' },
        { title: 'Диспетчер', value: 'dispatcher' },
      ],
      passwordData: {
        current_password: '',
        new_password: '',
        confirm_password: '',
      },
      errors: {},
      passwordErrors: {},
      errorMessage: '',
      passwordErrorMessage: '',
      successMessage: '',
      passwordSuccessMessage: '',
      loading: false,
      passwordLoading: false,
    }
  },
  async mounted() {
    await this.loadUserData()
  },
  methods: {
    async loadUserData() {
      const authStore = useAuthStore()
      await authStore.fetchUser()
      
      if (authStore.user) {
        this.formData = {
          username: authStore.user.username || '',
          email: authStore.user.email || '',
          first_name: authStore.user.first_name || '',
          last_name: authStore.user.last_name || '',
          role: authStore.user.role || '',
          phone_number: authStore.user.phone_number || '',
          address: authStore.user.address || '',
          birth_date: authStore.user.birth_date || '',
        }
      }
    },

    async handleUpdateProfile() {
      this.errors = {}
      this.errorMessage = ''
      this.successMessage = ''
      this.loading = true

      const authStore = useAuthStore()
      const result = await authStore.updateProfile(this.formData)

      if (result.success) {
        this.successMessage = 'Профиль успешно обновлён'
        await this.loadUserData()
      } else {
        this.errorMessage = result.error || 'Ошибка обновления профиля'
      }

      this.loading = false
    },

    async handleChangePassword() {
      this.passwordErrors = {}
      this.passwordErrorMessage = ''
      this.passwordSuccessMessage = ''
      this.passwordLoading = true

      if (!this.passwordData.current_password) {
        this.passwordErrors.current_password = 'Введите текущий пароль'
        this.passwordLoading = false
        return
      }

      if (!this.passwordData.new_password) {
        this.passwordErrors.new_password = 'Введите новый пароль'
        this.passwordLoading = false
        return
      }

      if (this.passwordData.new_password !== this.passwordData.confirm_password) {
        this.passwordErrors.confirm_password = 'Пароли не совпадают'
        this.passwordLoading = false
        return
      }

      const authStore = useAuthStore()
      const result = await authStore.changePassword(
        this.passwordData.current_password,
        this.passwordData.new_password
      )

      if (result.success) {
        this.passwordSuccessMessage = 'Пароль успешно изменён'
        this.passwordData = {
          current_password: '',
          new_password: '',
          confirm_password: '',
        }
      } else {
        this.passwordErrorMessage = result.error || 'Ошибка смены пароля'
      }

      this.passwordLoading = false
    },
  },
}
</script>

