<template>
  <div>
    <v-alert
        v-if="error"
        type="error"
        class="mb-4"
        @click:close="error = null"
        closable
    >
      {{ error }}
    </v-alert>

    <v-form @submit.prevent="saveCompanyInfo" ref="companyForm">
      <v-row>
        <!-- Логотип -->
        <v-col cols="12" md="4" class="text-center">
          <div class="mb-4">
            <v-avatar size="200" class="mb-4">
              <v-img
                  v-if="companyFormData.logo && isValidLogo(companyFormData.logo)"
                  :src="companyFormData.logo"
                  cover
              >
                <template v-slot:placeholder>
                  <v-icon size="100" color="grey-lighten-1">mdi-office-building</v-icon>
                </template>
              </v-img>
              <div v-else class="no-logo">
                <v-icon size="100" color="grey-lighten-1">mdi-office-building</v-icon>
                <div class="text-caption mt-2">Нет логотипа</div>
              </div>
            </v-avatar>
          </div>

          <v-text-field
              v-model="companyFormData.logo"
              label="URL логотипа"
              placeholder="https://example.com/logo.png"
              :rules="[rules.url]"
              class="mb-2"
              :disabled="loading"
          ></v-text-field>

          <v-btn
              @click="companyFormData.logo = ''"
              variant="text"
              size="small"
              color="error"
              :disabled="!companyFormData.logo || loading"
          >
            <v-icon start icon="mdi-delete"></v-icon>
            Удалить логотип
          </v-btn>
        </v-col>

        <!-- Основная информация -->
        <v-col cols="12" md="8">
          <v-text-field
              v-model="companyFormData.name"
              label="Название компании"
              :rules="[rules.required, rules.maxLength(100)]"
              class="mb-3"
              :disabled="loading"
          ></v-text-field>

          <v-textarea
              v-model="companyFormData.description"
              label="Описание компании"
              :rules="[rules.required, rules.maxLength(1000)]"
              rows="4"
              class="mb-3"
              :disabled="loading"
          ></v-textarea>

          <v-text-field
              v-model="companyFormData.website"
              label="Веб-сайт"
              placeholder="https://example.com"
              :rules="[rules.url, rules.maxLength(200)]"
              class="mb-3"
              :disabled="loading"
          ></v-text-field>

          <!-- Статистика (без отзывов) -->
          <v-card variant="outlined" class="mb-4">
            <v-card-text>
              <div class="text-h6 mb-2">Статистика компании</div>
              <v-row>
                <v-col cols="4" class="text-center">
                  <div class="text-h4 font-weight-bold">{{ company.services?.length || 0 }}</div>
                  <div class="text-caption">Услуг</div>
                </v-col>
                <v-col cols="4" class="text-center">
                  <div class="text-h4 font-weight-bold">{{ company.service_requests?.length || 0 }}</div>
                  <div class="text-caption">Заявок</div>
                </v-col>
                <v-col cols="4" class="text-center">
                  <div class="text-h4 font-weight-bold" :class="{'text-amber': company.average_rating}">
                    {{ company.average_rating?.toFixed(1) || '0.0' }}
                  </div>
                  <div class="text-caption">Рейтинг</div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <div class="d-flex justify-space-between">
            <div>
              <v-btn
                  @click="$emit('company-updated')"
                  variant="outlined"
                  color="primary"
                  :loading="loading"
                  :disabled="loading"
                  class="mr-2"
              >
                <v-icon start icon="mdi-refresh"></v-icon>
                Обновить данные
              </v-btn>

              <!-- Кнопка удаления компании -->
              <v-btn
                  @click="openDeleteDialog"
                  variant="outlined"
                  color="error"
                  :disabled="loading"
              >
                <v-icon start icon="mdi-delete"></v-icon>
                Удалить компанию
              </v-btn>
            </div>

            <v-btn
                type="submit"
                color="primary"
                :loading="loading"
                :disabled="loading"
            >
              <v-icon start icon="mdi-content-save"></v-icon>
              Сохранить изменения
            </v-btn>
          </div>
        </v-col>
      </v-row>
    </v-form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import apiClient from '@/api'

const props = defineProps({
  company: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['company-updated', 'open-delete-dialog'])

// Состояния
const loading = ref(false)
const error = ref(null)

// Данные формы
const companyFormData = reactive({
  name: '',
  description: '',
  logo: '',
  website: ''
})

// Правила валидации
const rules = {
  required: value => !!value?.trim() || 'Обязательное поле',
  maxLength: (max) => value => !value || value.length <= max || `Максимум ${max} символов`,
  url: value => !value || /^https?:\/\/.+\..+/.test(value) || 'Некорректный URL'
}

// Проверка валидности логотипа
const isValidLogo = (logoUrl) => {
  if (!logoUrl || typeof logoUrl !== 'string') return false
  const lowerUrl = logoUrl.toLowerCase()
  const invalidPatterns = ['via.placeholder.com', 'example.com', 'string', 'test']
  return !invalidPatterns.some(pattern => lowerUrl.includes(pattern))
}

// Инициализация формы
const initializeForm = () => {
  companyFormData.name = props.company.name || ''
  companyFormData.description = props.company.description || ''
  companyFormData.logo = props.company.logo || ''
  companyFormData.website = props.company.website || ''
}

// Открытие диалога удаления
const openDeleteDialog = () => {
  emit('open-delete-dialog')
}

// Сохранение информации о компании
const saveCompanyInfo = async () => {
  loading.value = true
  error.value = null

  try {
    // Подготавливаем данные для отправки
    const formData = {
      name: companyFormData.name.trim(),
      description: companyFormData.description.trim(),
      website: companyFormData.website.trim()
    }

    // Добавляем логотип только если он валидный
    if (companyFormData.logo.trim() && isValidLogo(companyFormData.logo.trim())) {
      formData.logo = companyFormData.logo.trim()
    } else {
      formData.logo = ''
    }

    await apiClient.put('companies/update_my/', formData)

    // Обновляем данные
    emit('company-updated')
  } catch (err) {
    console.error('Error saving company info:', err)
    error.value = err.response?.data?.detail || 'Ошибка сохранения данных компании'
  } finally {
    loading.value = false
  }
}

// Инициализация при монтировании и изменении данных компании
onMounted(initializeForm)
watch(() => props.company, initializeForm, { deep: true })
</script>

<style scoped>
.no-logo {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
  color: #9e9e9e;
}

.v-avatar {
  border: 2px dashed #e0e0e0;
}
</style>