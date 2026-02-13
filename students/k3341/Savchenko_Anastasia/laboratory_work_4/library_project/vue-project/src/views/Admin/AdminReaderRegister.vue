<template>
  <div class="admin-reader-register">
    <v-container class="register-container">
      <v-row justify="center">
        <v-col cols="12" md="10" lg="8">
          <v-card>
            <v-card-title class="text-h5">
              <v-icon left size="28" color="primary">mdi-account-plus</v-icon>
              Регистрация нового читателя
            </v-card-title>

            <v-card-text>
              <v-form ref="formRef" v-model="valid">
                <v-row>
                  <v-col cols="12">
                    <h4 class="text-subtitle-1 mb-2">📋 Основная информация</h4>
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="formData.full_name"
                      :rules="[v => !!v || 'ФИО обязательно']"
                      label="ФИО *"
                      placeholder="Иванов Иван Иванович"
                      required
                      density="comfortable"
                      variant="outlined"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="formData.passport"
                      :rules="[v => !!v || 'Паспорт обязателен']"
                      label="Номер паспорта *"
                      placeholder="1234 567890"
                      required
                      density="comfortable"
                      variant="outlined"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="formData.birth_date"
                      :rules="[v => !!v || 'Дата рождения обязательна']"
                      label="Дата рождения *"
                      placeholder="YYYY-MM-DD"
                      type="date"
                      required
                      density="comfortable"
                      variant="outlined"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-select
                      v-model="formData.education_level"
                      :items="educationLevels"
                      :rules="[v => !!v || 'Образование обязательно']"
                      label="Образование *"
                      required
                      density="comfortable"
                      variant="outlined"
                    ></v-select>
                  </v-col>

                  <v-col cols="12">
                    <v-divider class="my-4"></v-divider>
                    <h4 class="text-subtitle-1 mb-2">📞 Контактные данные</h4>
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="formData.phone_number"
                      :rules="[v => !!v || 'Телефон обязателен']"
                      label="Телефон *"
                      placeholder="+7 (999) 123-45-67"
                      required
                      density="comfortable"
                      variant="outlined"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-select
                      v-model="formData.hall_id"
                      :items="halls"
                      :rules="[v => !!v || 'Зал обязателен']"
                      item-title="name"
                      item-value="hall_id"
                      label="Зал *"
                      required
                      density="comfortable"
                      variant="outlined"
                    ></v-select>
                  </v-col>

                  <v-col cols="12">
                    <v-textarea
                      v-model="formData.home_address"
                      :rules="[v => !!v || 'Адрес обязателен']"
                      label="Адрес *"
                      placeholder="г. Москва, ул. Пушкина, д. 10, кв. 5"
                      rows="2"
                      required
                      density="comfortable"
                      variant="outlined"
                    ></v-textarea>
                  </v-col>
                </v-row>
              </v-form>

              <v-alert
                v-if="error"
                type="error"
                variant="tonal"
                class="mt-4"
                closable
                @click:close="error = ''"
              >
                {{ error }}
              </v-alert>

              <v-alert
                v-if="success"
                type="success"
                variant="tonal"
                class="mt-4"
              >
                ✅ Читатель успешно зарегистрирован!
                <div class="mt-2" v-if="newReader">
                  <strong>Номер билета:</strong> {{ newReader.library_card_id }}
                </div>
              </v-alert>
            </v-card-text>

            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn
                color="grey-darken-1"
                variant="text"
                @click="$router.push('/admin/readers')"
              >
                Отмена
              </v-btn>
              <v-btn
                color="primary"
                :loading="loading"
                @click="registerReader"
              >
                Зарегистрировать читателя
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../../api/client'

const router = useRouter()
const formRef = ref(null)
const valid = ref(false)
const loading = ref(false)
const error = ref('')
const success = ref(false)
const newReader = ref(null)
const halls = ref([])

const formData = reactive({
  full_name: '',
  passport: '',
  birth_date: '',
  education_level: '',
  phone_number: '',
  home_address: '',
  hall_id: null
})

const educationLevels = [
  { title: 'Начальное', value: 'primary' },
  { title: 'Среднее', value: 'secondary' },
  { title: 'Высшее', value: 'higher' },
  { title: 'Ученая степень', value: 'degree' }
]

const loadHalls = async () => {
  try {
    const response = await apiClient.get('halls/')
    halls.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки залов:', error)
  }
}

const registerReader = async () => {
  if (!formRef.value?.validate()) return

  loading.value = true
  error.value = ''
  success.value = false

  try {
    const response = await apiClient.post('reader/register/', {
      full_name: formData.full_name,
      passport: formData.passport,
      birth_date: formData.birth_date,
      education_level: formData.education_level,
      phone_number: formData.phone_number,
      home_address: formData.home_address,
      hall_id: formData.hall_id
    })

    newReader.value = response.data
    success.value = true

    // Сброс формы
    formData.full_name = ''
    formData.passport = ''
    formData.birth_date = ''
    formData.education_level = ''
    formData.phone_number = ''
    formData.home_address = ''
    formData.hall_id = null

    setTimeout(() => {
      router.push('/admin/readers')
    }, 3000)

  } catch (error) {
    console.error('Ошибка регистрации:', error)
    error.value = error.response?.data?.error || 'Ошибка регистрации'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadHalls()
})
</script>

<style scoped>
.admin-reader-register {
  width: 100%;
  min-height: 100%;
}

.register-container {
  max-width: 1200px !important;
  padding: 20px !important;
}

/* Убираем возможные конфликты с отступами */
.v-main .register-container {
  padding-left: 20px !important;
  padding-right: 20px !important;
}

/* Стили для карточки */
.v-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
}

.v-card-title {
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
  border-bottom: 1px solid #ddd;
}

/* Адаптивность */
@media (max-width: 768px) {
  .register-container {
    padding: 10px !important;
  }
}

@media (max-width: 480px) {
  .register-container {
    padding: 5px !important;
  }
}
</style>