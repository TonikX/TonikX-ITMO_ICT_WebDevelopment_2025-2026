<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8" offset-md="2">
        <v-card>
          <v-card-title>
            {{ isEdit ? 'Редактирование дома' : 'Создание дома' }}
          </v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleSubmit">
              <v-text-field
                v-model="formData.address"
                label="Адрес *"
                prepend-inner-icon="mdi-map-marker"
                variant="outlined"
                required
                :error-messages="errors.address"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="formData.total_floors"
                label="Количество этажей *"
                type="number"
                prepend-inner-icon="mdi-stairs"
                variant="outlined"
                required
                :error-messages="errors.total_floors"
                class="mb-4"
              ></v-text-field>

              <v-textarea
                v-model="formData.description"
                label="Описание"
                prepend-inner-icon="mdi-text"
                variant="outlined"
                rows="4"
                :error-messages="errors.description"
                class="mb-4"
              ></v-textarea>

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
import { buildingsService } from '@/services/buildingsService'

export default {
  name: 'BuildingForm',
  data() {
    return {
      formData: {
        address: '',
        total_floors: null,
        description: '',
      },
      errors: {},
      errorMessage: '',
      successMessage: '',
      loading: false,
    }
  },
  computed: {
    isEdit() {
      return !!this.$route.params.id
    },
    buildingId() {
      return this.$route.params.id
    },
  },
  async mounted() {
    if (this.isEdit) {
      await this.loadBuilding()
    }
  },
  methods: {
    async loadBuilding() {
      this.loading = true
      try {
        const building = await buildingsService.getBuilding(this.buildingId)
        this.formData = {
          address: building.address || '',
          total_floors: building.total_floors || null,
          description: building.description || '',
        }
      } catch (error) {
        this.errorMessage = 'Ошибка загрузки дома'
        console.error('Error loading building:', error)
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
          address: this.formData.address,
          total_floors: this.formData.total_floors,
          description: this.formData.description || '',
        }

        if (this.isEdit) {
          await buildingsService.updateBuilding(this.buildingId, data)
          this.successMessage = 'Дом успешно обновлён'
        } else {
          await buildingsService.createBuilding(data)
          this.successMessage = 'Дом успешно создан'
        }

        setTimeout(() => {
          this.$router.push('/buildings')
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
        this.errorMessage = 'Ошибка при сохранении дома'
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

