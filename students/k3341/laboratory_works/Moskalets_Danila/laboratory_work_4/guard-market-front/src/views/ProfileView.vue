<template>
  <v-row>
    <v-col cols="12">
      <v-card class="pa-6">
        <v-card-title class="text-h4 mb-4">
          Мой профиль
        </v-card-title>

        <v-alert
            v-if="error"
            type="error"
            class="mb-4"
            closable
            @close="error = null"
        >
          {{ error }}
        </v-alert>

        <v-alert
            v-if="successMessage"
            type="success"
            class="mb-4"
            closable
            @close="successMessage = null"
        >
          {{ successMessage }}
        </v-alert>

        <v-form @submit.prevent="updateProfile" v-if="authStore.user">
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                  v-model="form.email"
                  label="Email"
                  type="email"
                  required
                  :rules="[rules.required, rules.email]"
                  :disabled="isLoading"
              ></v-text-field>
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                  v-model="form.name"
                  label="Имя"
                  required
                  :rules="[rules.required]"
                  :disabled="isLoading"
              ></v-text-field>
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                  v-model="form.surname"
                  label="Фамилия"
                  required
                  :rules="[rules.required]"
                  :disabled="isLoading"
              ></v-text-field>
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                  v-model="form.patronymic"
                  label="Отчество"
                  :disabled="isLoading"
              ></v-text-field>
            </v-col>
          </v-row>

          <div class="d-flex justify-end mt-4">
            <v-btn
                type="submit"
                color="primary"
                :loading="isLoading"
            >
              Сохранить изменения
            </v-btn>
          </div>
        </v-form>

        <v-divider class="my-6"></v-divider>

        <div v-if="authStore.user">
          <h3 class="text-h6 mb-4">Дополнительная информация</h3>
          <v-list>
            <v-list-item>
              <template v-slot:prepend>
                <v-icon icon="mdi-account-check"></v-icon>
              </template>
              <v-list-item-title>Статус</v-list-item-title>
              <v-list-item-subtitle>
                {{ authStore.isAdmin ? 'Администратор' : 'Пользователь' }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon icon="mdi-office-building"></v-icon>
              </template>
              <v-list-item-title>Компания</v-list-item-title>
              <v-list-item-subtitle>
                <template v-if="authStore.hasCompany">
                  <div class="d-flex align-center">
                    <v-avatar size="40" class="mr-3">
                      <v-img
                          v-if="authStore.company?.logo && isValidLogo(authStore.company.logo)"
                          :src="authStore.company.logo"
                          cover
                      ></v-img>
                      <v-icon v-else color="grey">
                        mdi-office-building
                      </v-icon>
                    </v-avatar>
                    <div>
                      <div class="font-weight-bold">
                        {{ authStore.company?.name || 'Без названия' }}
                      </div>
                      <div class="text-caption">
                        {{ authStore.company?.website || 'Нет сайта' }}
                      </div>
                    </div>
                  </div>
                </template>
                <span v-else class="text-grey">
                  Нет компании
                </span>
              </v-list-item-subtitle>
            </v-list-item>

            <v-list-item v-if="authStore.hasCompany">
              <template v-slot:append>
                <v-btn
                    :to="`/companies/${authStore.company.id}`"
                    color="primary"
                    variant="outlined"
                    size="small"
                    class="mr-2"
                >
                  Страница компании
                </v-btn>
                <v-btn
                    to="/company"
                    color="primary"
                    size="small"
                >
                  Управление
                </v-btn>
              </template>
            </v-list-item>

            <v-list-item v-else>
              <template v-slot:append>
                <v-btn
                    @click="openCreateCompanyDialog"
                    color="primary"
                    variant="outlined"
                    size="small"
                >
                  Создать компанию
                </v-btn>
              </template>
            </v-list-item>

            <!-- Статистика -->
            <v-list-item v-if="authStore.user.favorites?.length > 0">
              <template v-slot:prepend>
                <v-icon icon="mdi-heart"></v-icon>
              </template>
              <v-list-item-title>Избранное</v-list-item-title>
              <v-list-item-subtitle>
                {{ authStore.user.favorites.length }} услуг
              </v-list-item-subtitle>
              <template v-slot:append>
                <v-btn
                    to="/favorites"
                    variant="text"
                    size="small"
                >
                  Посмотреть
                </v-btn>
              </template>
            </v-list-item>

            <v-list-item v-if="authStore.user.service_requests?.length > 0">
              <template v-slot:prepend>
                <v-icon icon="mdi-format-list-bulleted"></v-icon>
              </template>
              <v-list-item-title>Мои заявки</v-list-item-title>
              <v-list-item-subtitle>
                {{ authStore.user.service_requests.length }} заявок
              </v-list-item-subtitle>
              <template v-slot:append>
                <v-btn
                    to="/requests"
                    variant="text"
                    size="small"
                >
                  Посмотреть
                </v-btn>
              </template>
            </v-list-item>

            <v-list-item v-if="authStore.user.reviews?.length > 0">
              <template v-slot:prepend>
                <v-icon icon="mdi-star"></v-icon>
              </template>
              <v-list-item-title>Мои отзывы</v-list-item-title>
              <v-list-item-subtitle>
                {{ authStore.user.reviews.length }} отзывов
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </div>
      </v-card>
    </v-col>
  </v-row>

  <!-- Диалог создания компании -->
  <v-dialog v-model="showCreateCompanyDialog" max-width="600">
    <v-card>
      <v-card-title>Создание компании</v-card-title>
      <v-card-text>
        <p class="mb-4">
          После создания компании вы станете её администратором и сможете добавлять услуги.
        </p>

        <v-alert
            v-if="companyError"
            type="error"
            class="mb-4"
            closable
            @close="companyError = null"
        >
          {{ companyError }}
        </v-alert>

        <v-form @submit.prevent="createCompany" ref="companyFormRef">
          <v-text-field
              v-model="companyForm.name"
              label="Название компании *"
              required
              :rules="[rules.required, rules.minLength(2), rules.maxLength(100)]"
              :error-messages="companyErrors.name"
              :disabled="isCreatingCompany"
              class="mb-3"
              counter="100"
          ></v-text-field>

          <v-textarea
              v-model="companyForm.description"
              label="Описание компании"
              :rules="[rules.maxLength(500)]"
              :error-messages="companyErrors.description"
              :disabled="isCreatingCompany"
              class="mb-3"
              rows="3"
              counter="500"
          ></v-textarea>

          <v-text-field
              v-model="companyForm.website"
              label="Веб-сайт"
              type="url"
              placeholder="https://example.com"
              :rules="[rules.url]"
              :error-messages="companyErrors.website"
              :disabled="isCreatingCompany"
              class="mb-3"
          ></v-text-field>

          <v-text-field
              v-model="companyForm.logo"
              label="URL логотипа"
              type="url"
              placeholder="https://example.com/logo.png"
              :rules="[rules.url]"
              :error-messages="companyErrors.logo"
              :disabled="isCreatingCompany"
              class="mb-4"
          ></v-text-field>

          <div class="text-caption text-grey mb-4">
            * - обязательные поля
          </div>

          <div class="d-flex justify-end">
            <v-btn
                @click="closeCreateCompanyDialog"
                :disabled="isCreatingCompany"
                class="mr-2"
                variant="outlined"
            >
              Отмена
            </v-btn>
            <v-btn
                type="submit"
                color="primary"
                :loading="isCreatingCompany"
                :disabled="!isCompanyFormValid"
            >
              Создать компанию
            </v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/api'

const authStore = useAuthStore()

const isLoading = ref(false)
const error = ref(null)
const successMessage = ref(null)

const form = reactive({
  email: '',
  name: '',
  surname: '',
  patronymic: ''
})

const showCreateCompanyDialog = ref(false)
const isCreatingCompany = ref(false)
const companyError = ref(null)
const companyFormRef = ref(null)

const companyForm = reactive({
  name: '',
  description: '',
  website: '',
  logo: ''
})

const companyErrors = reactive({
  name: [],
  description: [],
  website: [],
  logo: []
})

const rules = {
  required: value => !!value || 'Обязательное поле',
  email: value => {
    const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    return pattern.test(value) || 'Некорректный email'
  },
  url: value => {
    if (!value) return true
    const pattern = /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/
    return pattern.test(value) || 'Некорректный URL'
  },
  minLength: (min) => value => (value && value.length >= min) || `Минимум ${min} символа`,
  maxLength: (max) => value => (!value || value.length <= max) || `Максимум ${max} символов`
}

// Проверка валидности логотипа
const isValidLogo = (logoUrl) => {
  if (!logoUrl || typeof logoUrl !== 'string') return false
  const lowerUrl = logoUrl.toLowerCase()
  const invalidPatterns = [
    'via.placeholder.com',
    'example.com',
    'string',
    'test',
    'localhost',
    'placeholder.com'
  ]
  return !invalidPatterns.some(pattern => lowerUrl.includes(pattern))
}

// Проверка валидности формы компании
const isCompanyFormValid = computed(() => {
  return companyForm.name.trim().length >= 2 &&
      companyForm.name.trim().length <= 100
})

onMounted(() => {
  if (authStore.user) {
    form.email = authStore.user.email
    form.name = authStore.user.name
    form.surname = authStore.user.surname
    form.patronymic = authStore.user.patronymic || ''
  }
})

const updateProfile = async () => {
  isLoading.value = true
  error.value = null
  successMessage.value = null

  try {
    await authStore.updateProfile(form)
    successMessage.value = 'Профиль успешно обновлен'
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка обновления профиля'
    console.error('Update profile error:', err)
  } finally {
    isLoading.value = false
  }
}

const openCreateCompanyDialog = () => {
  // Сбрасываем форму
  Object.keys(companyForm).forEach(key => {
    companyForm[key] = ''
  })

  Object.keys(companyErrors).forEach(key => {
    companyErrors[key] = []
  })

  companyError.value = null
  showCreateCompanyDialog.value = true
}

const closeCreateCompanyDialog = () => {
  showCreateCompanyDialog.value = false

  // Чистим форму через короткий таймаут
  setTimeout(() => {
    Object.keys(companyForm).forEach(key => {
      companyForm[key] = ''
    })
    Object.keys(companyErrors).forEach(key => {
      companyErrors[key] = []
    })
    companyError.value = null
  }, 300)
}

const createCompany = async () => {
  if (!companyFormRef.value) return

  // Проверяем валидацию формы
  const { valid } = await companyFormRef.value.validate()
  if (!valid) {
    companyError.value = 'Пожалуйста, исправьте ошибки в форме'
    return
  }

  isCreatingCompany.value = true
  companyError.value = null

  // Очищаем ошибки валидации
  Object.keys(companyErrors).forEach(key => {
    companyErrors[key] = []
  })

  try {
    // Подготавливаем данные для отправки
    const companyData = {
      name: companyForm.name.trim(),
      description: companyForm.description?.trim() || '',
      website: companyForm.website?.trim() || '',
      logo: companyForm.logo?.trim() || ''
    }

    // Проверяем URL поля
    if (companyData.website && !companyData.website.startsWith('http')) {
      companyData.website = 'https://' + companyData.website
    }

    if (companyData.logo && !companyData.logo.startsWith('http')) {
      companyData.logo = 'https://' + companyData.logo
    }

    // Отправляем данные для создания компании
    const response = await apiClient.post('companies/', companyData)

    // Обновляем данные пользователя
    await authStore.fetchUser()

    successMessage.value = 'Компания успешно создана!'
    showCreateCompanyDialog.value = false

    // Очищаем форму
    Object.keys(companyForm).forEach(key => {
      companyForm[key] = ''
    })

  } catch (err) {
    console.error('Create company error response:', err.response)

    if (err.response?.status === 400) {
      // Ошибки валидации от сервера
      const errors = err.response.data

      if (typeof errors === 'object') {
        // Заполняем ошибки для конкретных полей
        Object.keys(errors).forEach(field => {
          if (companyErrors.hasOwnProperty(field)) {
            const messages = errors[field]
            companyErrors[field] = Array.isArray(messages) ? messages : [messages]
          }
        })

        // Общие ошибки (не привязанные к полям)
        const generalErrors = []
        for (const [field, messages] of Object.entries(errors)) {
          if (!companyErrors.hasOwnProperty(field)) {
            if (Array.isArray(messages)) {
              generalErrors.push(...messages)
            } else {
              generalErrors.push(messages)
            }
          }
        }

        if (generalErrors.length > 0) {
          companyError.value = generalErrors.join(', ')
        } else if (Object.keys(errors).length === 0 && errors.detail) {
          companyError.value = errors.detail
        }
      } else if (typeof errors === 'string') {
        companyError.value = errors
      } else if (errors.detail) {
        companyError.value = errors.detail
      } else {
        companyError.value = 'Ошибка создания компании'
      }
    } else if (err.response?.data?.detail) {
      companyError.value = err.response.data.detail
    } else if (err.message) {
      companyError.value = err.message
    } else {
      companyError.value = 'Ошибка соединения с сервером'
    }
  } finally {
    isCreatingCompany.value = false
  }
}
</script>

<style scoped>
.v-avatar {
  border: 2px solid #e0e0e0;
}

/* Стили для обязательных полей */
:deep(.v-label.v-field-label--required)::after {
  content: " *";
  color: #f44336;
}
</style>