<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8" offset-md="2">
        <v-card>
          <v-card-title>
            {{ isEdit ? 'Редактирование показаний' : 'Подача показаний счетчика' }}
          </v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleSubmit">
              <ApartmentSelect
                v-model="formData.apartment_id"
                label="Квартира *"
                required
                :error-messages="errors.apartment"
                :disabled="isEdit"
                class="mb-4"
              />

              <v-select
                v-model="formData.meter_type"
                :items="meterTypeOptions"
                label="Тип счетчика *"
                prepend-inner-icon="mdi-counter"
                variant="outlined"
                required
                :error-messages="errors.meter_type"
                :disabled="isEdit"
                class="mb-4"
              ></v-select>

              <v-text-field
                v-model="formData.value"
                label="Значение *"
                prepend-inner-icon="mdi-numeric"
                type="number"
                step="0.001"
                variant="outlined"
                required
                :error-messages="errors.value"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="formData.date_recorded"
                label="Дата подачи"
                type="date"
                prepend-inner-icon="mdi-calendar"
                variant="outlined"
                :error-messages="errors.date_recorded"
                class="mb-4"
              ></v-text-field>

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
                  {{ isEdit ? 'Сохранить' : 'Подать показания' }}
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
import { meterReadingsService } from '@/services/meterReadingsService'
import { getMeterTypeOptions } from '@/utils/statusUtils'
import ApartmentSelect from '@/components/ApartmentSelect.vue'

export default {
  name: 'MeterReadingForm',
  components: {
    ApartmentSelect,
  },
  data() {
    return {
      formData: {
        apartment_id: null,
        meter_type: null,
        value: '',
        date_recorded: new Date().toISOString().split('T')[0],
      },
      errors: {},
      errorMessage: '',
      successMessage: '',
      loading: false,
      meterTypeOptions: getMeterTypeOptions(),
    }
  },
  computed: {
    isEdit() {
      return !!this.$route.params.id
    },
    readingId() {
      return this.$route.params.id
    },
  },
  async mounted() {
    if (this.isEdit) {
      await this.loadReading()
    }
  },
  methods: {
    async loadReading() {
      this.loading = true
      try {
        const reading = await meterReadingsService.getMeterReading(this.readingId)
        this.formData = {
          apartment_id: reading.apartment?.id || null,
          meter_type: reading.meter_type || null,
          value: reading.value || '',
          date_recorded: reading.date_recorded || new Date().toISOString().split('T')[0],
        }
      } catch (error) {
        this.errorMessage = 'Ошибка загрузки показаний'
        console.error('Error loading reading:', error)
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
          apartment_id: this.formData.apartment_id,
          meter_type: this.formData.meter_type,
          value: this.formData.value,
          date_recorded: this.formData.date_recorded || new Date().toISOString().split('T')[0],
        }

        if (this.isEdit) {
          await meterReadingsService.updateMeterReading(this.readingId, data)
          this.successMessage = 'Показания успешно обновлены'
        } else {
          await meterReadingsService.createMeterReading(data)
          this.successMessage = 'Показания успешно поданы'
        }

        setTimeout(() => {
          this.$router.push('/meter-readings')
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
        this.errorMessage = 'Ошибка при сохранении показаний'
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

