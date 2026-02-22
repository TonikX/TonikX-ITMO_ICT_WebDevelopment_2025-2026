<template>
  <v-container class="my-8">
    <!-- Кнопка назад -->
    <v-btn
        @click="goBack"
        color="primary"
        variant="text"
        class="mb-4"
    >
      <v-icon start>mdi-arrow-left</v-icon>
      Назад
    </v-btn>

    <v-card class="pa-6" max-width="800" style="margin: 0 auto;">
      <v-card-title class="text-h4 mb-6">
        {{ isEdit ? 'Редактирование услуги' : 'Создание услуги' }}
      </v-card-title>

      <v-form @submit.prevent="saveService">
        <v-card-text>
          <v-row>
            <!-- Название -->
            <v-col cols="12">
              <v-text-field
                  v-model="form.name"
                  label="Название услуги"
                  variant="outlined"
                  :rules="[v => !!v || 'Обязательное поле']"
                  required
              />
            </v-col>

            <!-- Категория -->
            <v-col cols="12" md="6">
              <v-text-field
                  v-model="form.category"
                  label="Категория"
                  variant="outlined"
                  :rules="[v => !!v || 'Обязательное поле']"
                  required
              />
            </v-col>

            <!-- Цена -->
            <v-col cols="12" md="6">
              <v-text-field
                  v-model="form.price"
                  label="Цена (руб.)"
                  variant="outlined"
                  type="number"
                  step="0.01"
                  :rules="[v => !!v || 'Обязательное поле', v => v >= 0 || 'Цена не может быть отрицательной']"
                  required
              />
            </v-col>

            <!-- Длительность -->
            <v-col cols="12" md="6">
              <v-text-field
                  v-model="form.duration"
                  label="Длительность (минут)"
                  variant="outlined"
                  type="number"
                  :rules="[v => !!v || 'Обязательное поле', v => v > 0 || 'Длительность должна быть больше 0']"
                  required
              />
            </v-col>

            <!-- Активность (только при редактировании) -->
            <v-col cols="12" md="6" v-if="isEdit">
              <v-checkbox
                  v-model="form.is_active"
                  label="Активна"
                  color="primary"
              />
            </v-col>

            <!-- Описание -->
            <v-col cols="12">
              <v-textarea
                  v-model="form.description"
                  label="Описание"
                  variant="outlined"
                  rows="4"
                  :rules="[v => !!v || 'Обязательное поле']"
                  required
              />
            </v-col>
          </v-row>

          <!-- Ошибки -->
          <v-alert
              v-if="error"
              type="error"
              class="mb-4"
          >
            <div v-for="(value, key) in error" :key="key">
              {{ Array.isArray(value) ? value[0] : value }}
            </div>
          </v-alert>

          <!-- Кнопки -->
          <div class="d-flex justify-end gap-4">
            <v-btn
                @click="goBack"
                variant="outlined"
                color="primary"
            >
              Отмена
            </v-btn>

            <v-btn
                type="submit"
                color="primary"
                :loading="loading"
                :disabled="loading"
            >
              {{ isEdit ? 'Сохранить' : 'Создать' }}
            </v-btn>
          </div>
        </v-card-text>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminServiceEditView',

  data() {
    return {
      form: {
        name: '',
        description: '',
        price: '',
        duration: '',
        category: '',
        is_active: true
      },
      loading: false,
      error: null,
      isEdit: false
    }
  },

  async mounted() {
    const serviceId = this.$route.params.id
    this.isEdit = !!serviceId

    if (this.isEdit) {
      await this.loadService(serviceId)
    }
  },

  methods: {
    async loadService(serviceId) {
      this.loading = true
      try {
        const response = await axios.get(`/api/admin/services/${serviceId}/`)
        this.form = {
          name: response.data.name,
          description: response.data.description,
          price: response.data.price,
          duration: response.data.duration,
          category: response.data.category,
          is_active: response.data.is_active
        }
      } catch (error) {
        console.error('Ошибка загрузки услуги:', error)
        this.error = 'Не удалось загрузить услугу'
      } finally {
        this.loading = false
      }
    },

    goBack() {
      if (this.isEdit) {
        this.$router.push(`/admin/services/${this.$route.params.id}`)
      } else {
        this.$router.push('/admin/services')
      }
    },

    async saveService() {
      this.loading = true
      this.error = null

      try {
        if (this.isEdit) {
          const response = await axios.patch(
              `/api/admin/services/${this.$route.params.id}/`,
              this.form
          )
          alert('Услуга обновлена')
          this.$router.push(`/admin/services/${this.$route.params.id}`)
        } else {
          const response = await axios.post('/api/admin/services/', this.form)
          alert('Услуга создана')
          this.$router.push('/admin/services')
        }
      } catch (error) {
        console.error('Ошибка сохранения:', error)
        this.error = error.response?.data || { detail: 'Ошибка при сохранении' }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>