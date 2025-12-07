<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8" offset-md="2">
        <v-card>
          <v-card-title>
            {{ isEdit ? 'Редактирование заявки' : 'Создание заявки' }}
          </v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleSubmit">
              <v-text-field
                v-model="formData.title"
                label="Тема обращения *"
                prepend-inner-icon="mdi-format-title"
                variant="outlined"
                required
                :error-messages="errors.title"
                class="mb-4"
              ></v-text-field>

              <v-textarea
                v-model="formData.description"
                label="Описание проблемы *"
                prepend-inner-icon="mdi-text"
                variant="outlined"
                required
                rows="4"
                :error-messages="errors.description"
                class="mb-4"
              ></v-textarea>

              <CategorySelect
                v-model="formData.category_id"
                label="Категория услуги *"
                required
                :error-messages="errors.category"
                class="mb-4"
              />

              <ApartmentSelect
                v-model="formData.apartment_id"
                label="Квартира *"
                required
                :error-messages="errors.apartment"
                class="mb-4"
              />

              <v-select
                v-model="formData.priority"
                :items="priorityOptions"
                label="Приоритет"
                prepend-inner-icon="mdi-alert"
                variant="outlined"
                :error-messages="errors.priority"
                class="mb-4"
              ></v-select>

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

              <div class="d-flex justify-end gap-2">
                <v-btn
                  variant="text"
                  @click="$router.back()"
                >
                  Отмена
                </v-btn>
                <v-btn
                  type="submit"
                  color="primary"
                  :loading="loading"
                >
                  {{ isEdit ? 'Сохранить' : 'Создать' }}
                </v-btn>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { serviceRequestsService } from '@/services/serviceRequestsService'
import { useAuthStore } from '@/stores/auth'
import { getRequestPriorityOptions } from '@/utils/statusUtils'
import CategorySelect from '@/components/CategorySelect.vue'
import ApartmentSelect from '@/components/ApartmentSelect.vue'

export default {
  name: 'ServiceRequestForm',
  components: {
    CategorySelect,
    ApartmentSelect,
  },
  data() {
    return {
      formData: {
        title: '',
        description: '',
        category_id: null,
        apartment_id: null,
        priority: 'medium',
      },
      errors: {},
      errorMessage: '',
      successMessage: '',
      loading: false,
      priorityOptions: getRequestPriorityOptions(),
    }
  },
  computed: {
    isEdit() {
      return !!this.$route.params.id
    },
    requestId() {
      return this.$route.params.id
    },
    user() {
      return useAuthStore().user
    },
  },
  async mounted() {
    if (this.isEdit) {
      await this.loadRequest()
    }
  },
  methods: {
    async loadRequest() {
      this.loading = true
      try {
        const request = await serviceRequestsService.getServiceRequest(this.requestId)
        this.formData = {
          title: request.title || '',
          description: request.description || '',
          category_id: request.category?.id || null,
          apartment_id: request.apartment?.id || null,
          priority: request.priority || 'medium',
        }
      } catch (error) {
        this.errorMessage = 'Ошибка загрузки заявки'
        console.error('Error loading request:', error)
      } finally {
        this.loading = false
      }
    },
    async handleSubmit() {
      this.errors = {}
      this.errorMessage = ''
      this.successMessage = ''
      this.loading = true

      try {
        const data = {
          title: this.formData.title,
          description: this.formData.description,
          category_id: this.formData.category_id,
          apartment_id: this.formData.apartment_id,
          priority: this.formData.priority,
        }

        if (this.isEdit) {
          await serviceRequestsService.updateServiceRequest(this.requestId, data)
          this.successMessage = 'Заявка успешно обновлена'
        } else {
          await serviceRequestsService.createServiceRequest(data)
          this.successMessage = 'Заявка успешно создана'
        }

        setTimeout(() => {
          this.$router.push('/service-requests')
        }, 1500)
      } catch (error) {
        if (error.response?.data) {
          const errorData = error.response.data
          Object.keys(errorData).forEach((key) => {
            const messages = errorData[key]
            if (Array.isArray(messages)) {
              this.errors[key] = messages
            } else {
              this.errors[key] = [messages]
            }
          })
        }
        this.errorMessage = 'Ошибка при сохранении заявки'
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

