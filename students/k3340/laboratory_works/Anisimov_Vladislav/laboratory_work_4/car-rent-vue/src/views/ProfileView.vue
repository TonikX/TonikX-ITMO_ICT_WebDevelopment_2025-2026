<template>
  <v-container class="py-8">
    <v-row>
      <v-col cols="12">
        <v-breadcrumbs :items="breadcrumbs" class="px-0">
          <template v-slot:divider>
            <v-icon icon="mdi-chevron-right"></v-icon>
          </template>
        </v-breadcrumbs>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title class="d-flex align-center">
            <v-icon icon="mdi-account-circle" size="32" class="mr-3"></v-icon>
            <span class="text-h5 font-weight-bold">Личные данные</span>
          </v-card-title>

          <v-card-text>
            <v-form ref="profileForm" @submit.prevent="updateProfile">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="profile.first_name"
                    label="Имя"
                    variant="outlined"
                    :rules="[rules.required]"
                    prepend-inner-icon="mdi-account"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="profile.last_name"
                    label="Фамилия"
                    variant="outlined"
                    :rules="[rules.required]"
                    prepend-inner-icon="mdi-account"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="profile.username"
                    label="Логин"
                    variant="outlined"
                    :rules="[rules.required]"
                    prepend-inner-icon="mdi-account"
                    readonly
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="profile.phone"
                    label="Телефон"
                    variant="outlined"
                    :rules="[rules.required, rules.phone]"
                    prepend-inner-icon="mdi-phone"
                  ></v-text-field>
                </v-col>

                <v-col cols="12">
                  <v-text-field
                    v-model="profile.passport"
                    label="Паспортные данные"
                    variant="outlined"
                    :rules="[rules.required, rules.passport]"
                    prepend-inner-icon="mdi-card-account-details"
                  ></v-text-field>
                </v-col>

                <v-col cols="12">
                  <div class="d-flex justify-end gap-2">
                    <v-btn
                      type="submit"
                      color="primary"
                    >
                      Сохранить изменения
                    </v-btn>
                  </div>
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <!-- Изменение пароля -->
        <v-card class="mb-6">
          <v-card-title class="d-flex align-center">
            <v-icon icon="mdi-lock" size="24" class="mr-2"></v-icon>
            <span class="text-h6 font-weight-bold">Смена пароля</span>
          </v-card-title>

          <v-card-text>
            <v-form ref="passwordForm" @submit.prevent="changePassword">
              <v-text-field
                v-model="password.old_password"
                label="Текущий пароль"
                type="password"
                variant="outlined"
                :rules="[rules.required]"
                prepend-inner-icon="mdi-lock"
                class="mb-3"
              ></v-text-field>

              <v-text-field
                v-model="password.new_password1"
                label="Новый пароль"
                type="password"
                variant="outlined"
                :rules="[rules.required, rules.minLength(8)]"
                prepend-inner-icon="mdi-lock-plus"
                class="mb-3"
              ></v-text-field>

              <v-text-field
                v-model="password.new_password2"
                label="Подтверждение пароля"
                type="password"
                variant="outlined"
                :rules="[rules.required, passwordMatch]"
                prepend-inner-icon="mdi-lock-check"
                class="mb-4"
              ></v-text-field>

              <v-btn
                type="submit"
                color="primary"
                block
                :loading="passwordLoading"
              >
                Изменить пароль
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { format } from 'date-fns'
import { ru } from 'date-fns/locale'
import axios from 'axios'

const authStore = useAuthStore()


const profileForm = ref(null)
const passwordForm = ref(null)
const loading = ref(false)
const passwordLoading = ref(false)


const profile = ref({
  first_name: '',
  last_name: '',
  email: '',
  username: '',
  phone: '',
  passport: '',
  date_joined: ''
})


const password = ref({
  old_password: '',
  new_password1: '',
  new_password2: ''
})


const rules = {
  required: value => !!value || 'Обязательное поле',
  email: value => {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return pattern.test(value) || 'Неверный формат email'
  },
  phone: value => {
    const pattern = /^[\d\s\-\+\(\)]+$/
    return pattern.test(value) || 'Неверный формат телефона'
  },
  passport: value => value.length >= 10 || 'Неверные паспортные данные',
  minLength: (min) => (value) => 
    value.length >= min || `Минимум ${min} символов`,
  password_confirm: value => form.value.password === value || 'Пароли не совпадают'
}


const passwordMatch = (value) => {
  return value === password.value.new_password1 || 'Пароли не совпадают'
}


const isClient = computed(() => {
  return authStore.user?.role === 'client' || 
         authStore.user?.is_client === true
})

const isWorker = computed(() => {
  return authStore.user?.role === 'worker' || 
         authStore.user?.position
})

const workerPosition = computed(() => {
  return authStore.user?.position || 'Не указано'
})

const formattedDate = computed(() => {
  if (!profile.value.date_joined) return ''
  return format(new Date(profile.value.date_joined), 'dd MMMM yyyy', { locale: ru })
})

const breadcrumbs = ref([
  {
    title: 'Главная',
    disabled: false,
    href: '/'
  },
  {
    title: 'Профиль',
    disabled: true,
    href: '/profile'
  }
])


const loadProfile = async () => {
  try {
    axios.defaults.headers.common['Authorization'] = `Token ${localStorage.getItem('token')}`;
    const response = await axios.get('http://localhost:8000/auth/users/me/');

    if (response.statusText == "OK") {
      const data = response.data;
      profile.value = {
        first_name: data.first_name || '',
        last_name: data.last_name || '',
        username: data.username || '',
        phone: data.phone || '',
        passport: data.passport || '',
      }
    }
  } catch (error) {
    console.error('Ошибка загрузки профиля:', error)
    showError('Не удалось загрузить данные профиля')
  }
}


const updateProfile = async () => {
  const { valid } = await profileForm.value.validate()
  
  if (!valid) return

  loading.value = true

    try {
    const userData = {
      username: profile.value.username,
      first_name: profile.value.first_name,
      last_name: profile.value.last_name,
      phone: profile.value.phone,
      passport: profile.value.passport
    }
    console.log(userData);
    axios.defaults.headers.common['Authorization'] = `Token ${localStorage.getItem('token')}`;
    const response = await axios.patch('http://localhost:8000/auth/users/me/', userData);

    if (response.statusText == "OK") {
      const data = response.data;
      profile.value = {
        first_name: data.first_name || '',
        last_name: data.last_name || '',
        username: data.username || '',
        phone: data.phone || '',
        passport: data.passport || '',
      }
    }
  } catch (error) {
    console.error('Ошибка загрузки профиля:', error)
    showError('Не удалось загрузить данные профиля')
  }
}

const changePassword = async () => {
  const { valid } = await passwordForm.value.validate()
  
  if (!valid) return

  passwordLoading.value = true

   try {
    const password_update = {
      new_password: password.value.new_password1,
      current_password: password.value.old_password,
    }
    //console.log(userData);
    axios.defaults.headers.common['Authorization'] = `Token ${localStorage.getItem('token')}`;
    const response = await axios.post('http://localhost:8000/auth/users/set_password/', password_update);

      password.value = {
        old_password: '',
        new_password1: '',
        new_password2: ''
      }
      passwordForm.value.reset()
      
  passwordLoading.value = false
  } catch (error) {
    console.error('Ошибка загрузки профиля:', error)
    showError('Не удалось загрузить данные профиля')
  }
}


const resetForm = () => {
  loadProfile()
}


onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}

/* Анимация для успешного обновления */
.v-card {
  transition: all 0.3s ease;
}

.v-card:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1) !important;
}
</style>