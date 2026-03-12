<template>
  <v-row justify="center">
    <v-col cols="12" md="6">
      <v-card>
        <v-card-title class="text-h6">
          бронирование номера {{ room?.number || $route.params.id }}
        </v-card-title>
        <v-card-text>
          <v-alert v-if="error" type="error" density="compact" class="mb-2">
            {{ error }}
          </v-alert>
          <v-alert v-if="success" type="success" density="compact" class="mb-2">
            бронь успешно создана
          </v-alert>

          <v-form @submit.prevent="onSubmit">
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
              required
            />

            <v-btn :loading="loading" type="submit" color="primary" class="mt-2">
              забронировать
            </v-btn>
            <v-btn class="mt-2" variant="text" @click="$router.push('/rooms/' + $route.params.id)">
              к номеру
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
import { apiCreateBooking, apiGetRoom } from '../api'

// страница оформления бронирования
const route = useRoute()
const router = useRouter()

const room = ref(null)
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
    const resp = await apiGetRoom(route.params.id)
    room.value = resp.data
  } catch (e) {
    // если не удалось, просто оставим room null
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
    !form.check_in_date ||
    !form.check_out_date
  ) {
    error.value = 'заполните обязательные поля'
    return
  }

  loading.value = true
  try {
    await apiCreateBooking({
      ...form,
      room: route.params.id
    })
    success.value = true
    // после успешной брони отправим на страницу номера
    router.push('/rooms/' + route.params.id)
  } catch (e) {
    error.value = 'не удалось создать бронь'
  } finally {
    loading.value = false
  }
}
</script>

