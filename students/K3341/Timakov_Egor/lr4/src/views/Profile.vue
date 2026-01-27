<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8" offset-md="2">
        <v-card>
          <v-card-title class="text-h5">Профиль пользователя</v-card-title>
          <v-card-text>
            <v-tabs v-model="tab">
              <v-tab value="profile">Личные данные</v-tab>
              <v-tab value="password">Смена пароля</v-tab>
            </v-tabs>

            <v-window v-model="tab">
              <!-- Личные данные -->
              <v-window-item value="profile">
                <v-form @submit.prevent="updateProfile" class="mt-4">
                  <v-text-field
                    v-model="profileForm.username"
                    label="Имя пользователя"
                    variant="outlined"
                    disabled
                  ></v-text-field>

                  <v-text-field
                    v-model="profileForm.email"
                    label="Email"
                    type="email"
                    variant="outlined"
                    :error-messages="errors.email"
                  ></v-text-field>

                  <v-text-field
                    v-model="profileForm.first_name"
                    label="Имя"
                    variant="outlined"
                    :error-messages="errors.first_name"
                  ></v-text-field>

                  <v-text-field
                    v-model="profileForm.last_name"
                    label="Фамилия"
                    variant="outlined"
                    :error-messages="errors.last_name"
                  ></v-text-field>

                  <v-alert v-if="profileMessage" :type="profileMessageType" class="mb-4">
                    {{ profileMessage }}
                  </v-alert>

                  <v-btn type="submit" color="primary" :loading="profileLoading">
                    Сохранить изменения
                  </v-btn>
                </v-form>
              </v-window-item>

              <!-- Смена пароля -->
              <v-window-item value="password">
                <v-form @submit.prevent="changePassword" class="mt-4">
                  <v-text-field
                    v-model="passwordForm.current_password"
                    label="Текущий пароль"
                    type="password"
                    variant="outlined"
                    :error-messages="errors.current_password"
                    required
                  ></v-text-field>

                  <v-text-field
                    v-model="passwordForm.new_password"
                    label="Новый пароль"
                    type="password"
                    variant="outlined"
                    :error-messages="errors.new_password"
                    required
                  ></v-text-field>

                  <v-text-field
                    v-model="passwordForm.re_new_password"
                    label="Подтверждение нового пароля"
                    type="password"
                    variant="outlined"
                    :error-messages="errors.re_new_password"
                    required
                  ></v-text-field>

                  <v-alert v-if="passwordMessage" :type="passwordMessageType" class="mb-4">
                    {{ passwordMessage }}
                  </v-alert>

                  <v-btn type="submit" color="primary" :loading="passwordLoading">
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
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Profile',
  setup() {
    const authStore = useAuthStore()
    const tab = ref('profile')
    
    const profileForm = reactive({
      username: '',
      email: '',
      first_name: '',
      last_name: ''
    })
    
    const passwordForm = reactive({
      current_password: '',
      new_password: '',
      re_new_password: ''
    })
    
    const errors = reactive({})
    const profileMessage = ref('')
    const profileMessageType = ref('success')
    const passwordMessage = ref('')
    const passwordMessageType = ref('success')
    const profileLoading = ref(false)
    const passwordLoading = ref(false)

    onMounted(() => {
      if (authStore.user) {
        profileForm.username = authStore.user.username || ''
        profileForm.email = authStore.user.email || ''
        profileForm.first_name = authStore.user.first_name || ''
        profileForm.last_name = authStore.user.last_name || ''
      }
    })

    const updateProfile = async () => {
      Object.keys(errors).forEach(key => errors[key] = '')
      profileMessage.value = ''
      profileLoading.value = true

      const result = await authStore.updateUser({
        email: profileForm.email,
        first_name: profileForm.first_name,
        last_name: profileForm.last_name
      })

      if (result.success) {
        profileMessage.value = 'Данные успешно обновлены'
        profileMessageType.value = 'success'
      } else {
        if (result.error) {
          Object.keys(result.error).forEach(key => {
            if (Array.isArray(result.error[key])) {
              errors[key] = result.error[key].join(', ')
            } else {
              errors[key] = result.error[key]
            }
          })
        }
        profileMessage.value = 'Ошибка обновления данных'
        profileMessageType.value = 'error'
      }
      
      profileLoading.value = false
    }

    const changePassword = async () => {
      Object.keys(errors).forEach(key => errors[key] = '')
      passwordMessage.value = ''
      passwordLoading.value = true

      const result = await authStore.changePassword({
        current_password: passwordForm.current_password,
        new_password: passwordForm.new_password,
        re_new_password: passwordForm.re_new_password
      })

      if (result.success) {
        passwordMessage.value = 'Пароль успешно изменён'
        passwordMessageType.value = 'success'
        passwordForm.current_password = ''
        passwordForm.new_password = ''
        passwordForm.re_new_password = ''
      } else {
        if (result.error) {
          Object.keys(result.error).forEach(key => {
            if (Array.isArray(result.error[key])) {
              errors[key] = result.error[key].join(', ')
            } else {
              errors[key] = result.error[key]
            }
          })
        }
        passwordMessage.value = 'Ошибка смены пароля'
        passwordMessageType.value = 'error'
      }
      
      passwordLoading.value = false
    }

    return {
      tab,
      profileForm,
      passwordForm,
      errors,
      profileMessage,
      profileMessageType,
      passwordMessage,
      passwordMessageType,
      profileLoading,
      passwordLoading,
      updateProfile,
      changePassword
    }
  }
}
</script>
