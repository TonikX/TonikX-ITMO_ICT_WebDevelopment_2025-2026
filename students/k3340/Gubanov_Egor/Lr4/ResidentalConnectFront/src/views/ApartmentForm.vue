<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8" offset-md="2">
        <v-card>
          <v-card-title>
            {{ isEdit ? 'Редактирование квартиры' : 'Создание квартиры' }}
          </v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleSubmit">
              <BuildingSelect
                v-model="formData.building_id"
                label="Дом *"
                required
                :error-messages="errors.building"
                class="mb-4"
              />

              <v-text-field
                v-model="formData.number"
                label="Номер квартиры *"
                prepend-inner-icon="mdi-numeric"
                variant="outlined"
                required
                :error-messages="errors.number"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="formData.floor"
                label="Этаж *"
                type="number"
                prepend-inner-icon="mdi-stairs"
                variant="outlined"
                required
                :error-messages="errors.floor"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="formData.area"
                label="Площадь (м²) *"
                type="number"
                step="0.01"
                prepend-inner-icon="mdi-ruler-square"
                variant="outlined"
                required
                :error-messages="errors.area"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="formData.rooms"
                label="Количество комнат"
                type="number"
                prepend-inner-icon="mdi-door"
                variant="outlined"
                :error-messages="errors.rooms"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="formData.balance"
                label="Баланс счета"
                type="number"
                step="0.01"
                prepend-inner-icon="mdi-currency-rub"
                variant="outlined"
                :error-messages="errors.balance"
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
import { apartmentsService } from '@/services/apartmentsService'
import BuildingSelect from '@/components/BuildingSelect.vue'

export default {
  name: 'ApartmentForm',
  components: {
    BuildingSelect,
  },
  data() {
    return {
      formData: {
        building_id: null,
        number: '',
        floor: null,
        area: '',
        rooms: null,
        balance: '0.00',
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
    apartmentId() {
      return this.$route.params.id
    },
  },
  async mounted() {
    if (this.isEdit) {
      await this.loadApartment()
    }
  },
  methods: {
    async loadApartment() {
      this.loading = true
      try {
        const apartment = await apartmentsService.getApartment(this.apartmentId)
        this.formData = {
          building_id: apartment.building?.id || null,
          number: apartment.number || '',
          floor: apartment.floor || null,
          area: apartment.area || '',
          rooms: apartment.rooms || null,
          balance: apartment.balance || '0.00',
        }
      } catch (error) {
        this.errorMessage = 'Ошибка загрузки квартиры'
        console.error('Error loading apartment:', error)
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
          building_id: this.formData.building_id,
          number: this.formData.number,
          floor: this.formData.floor,
          area: this.formData.area,
          rooms: this.formData.rooms || null,
          balance: this.formData.balance || '0.00',
        }

        if (this.isEdit) {
          await apartmentsService.updateApartment(this.apartmentId, data)
          this.successMessage = 'Квартира успешно обновлена'
        } else {
          await apartmentsService.createApartment(data)
          this.successMessage = 'Квартира успешно создана'
        }

        setTimeout(() => {
          this.$router.push('/apartments')
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
        this.errorMessage = 'Ошибка при сохранении квартиры'
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

