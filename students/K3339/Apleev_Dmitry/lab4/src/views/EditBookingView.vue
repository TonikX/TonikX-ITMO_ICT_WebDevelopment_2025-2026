<template>
  <v-row justify="center">
    <v-col cols="12" md="6">
      <v-card>
        <v-card-title class="text-h6">
          редактирование брони
        </v-card-title>
        <v-card-text>
          <v-alert v-if="error" type="error" density="compact" class="mb-2">
            {{ error }}
          </v-alert>
          <v-alert v-if="success" type="success" density="compact" class="mb-2">
            бронь сохранена
          </v-alert>
          <v-progress-linear v-if="loadBooking && !booking" indeterminate color="primary" class="mb-2" />

          <v-form v-if="booking" @submit.prevent="onSubmit">
            <v-text-field
              v-model="form.passport_number"
              label="номер паспорта"
              variant="outlined"
              density="comfortable"
              required
            />
            <v-text-field
              v-model="form.last_name"
              label="фамилия"
              variant="outlined"
              density="comfortable"
              required
            />
            <v-text-field
              v-model="form.first_name"
              label="имя"
              variant="outlined"
              density="comfortable"
              required
            />
            <v-text-field
              v-model="form.middle_name"
              label="отчество"
              variant="outlined"
              density="comfortable"
            />
            <v-text-field
              v-model="form.city_of_origin"
              label="город проживания"
              variant="outlined"
              density="comfortable"
              required
            />
            <v-text-field
              v-model="form.check_in_date"
              label="дата заезда"
              type="date"
              variant="outlined"
              density="comfortable"
              required
            />
            <v-text-field
              v-model="form.check_out_date"
              label="дата выезда"
              type="date"
              variant="outlined"
              density="comfortable"
            />

            <v-btn :loading="loading" type="submit" color="primary" class="mt-2">
              сохранить
            </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiGetClient, apiUpdateBooking } from '../api'

// страница редактирования брони
const route = useRoute()
const router = useRouter()

const booking = ref(null)
const loadBooking = ref(true)
const loading = ref(false)
const error = ref('')
const success = ref(false)

const form = reactive({
  passport_number: '',
  first_name: '',
  last_name: '',
  middle_name: '',
  city_of_origin: '',
  check_in_date: '',
  check_out_date: ''
})

onMounted(async () => {
  try {
    const resp = await apiGetClient(route.params.id)
    booking.value = resp.data
    form.passport_number = resp.data.passport_number || ''
    form.first_name = resp.data.first_name || ''
    form.last_name = resp.data.last_name || ''
    form.middle_name = resp.data.middle_name || ''
    form.city_of_origin = resp.data.city_of_origin || ''
    form.check_in_date = resp.data.check_in_date || ''
    form.check_out_date = resp.data.check_out_date || ''
  } catch (e) {
    error.value = 'не удалось загрузить бронь'
  } finally {
    loadBooking.value = false
  }
})

const onSubmit = async () => {
  error.value = ''
  success.value = false

  if (
    !form.passport_number ||
    !form.first_name ||
    !form.last_name ||
    !form.city_of_origin ||
    !form.check_in_date
  ) {
    error.value = 'заполните обязательные поля'
    return
  }

  loading.value = true
  try {
    await apiUpdateBooking(route.params.id, {
      passport_number: form.passport_number,
      first_name: form.first_name,
      last_name: form.last_name,
      middle_name: form.middle_name || null,
      city_of_origin: form.city_of_origin,
      check_in_date: form.check_in_date,
      check_out_date: form.check_out_date || null
    })
    success.value = true
    setTimeout(() => router.push('/my-bookings'), 800)
  } catch (e) {
    error.value = e.response?.status === 403 ? 'нельзя редактировать эту бронь' : 'не удалось сохранить'
  } finally {
    loading.value = false
  }
}
</script>
