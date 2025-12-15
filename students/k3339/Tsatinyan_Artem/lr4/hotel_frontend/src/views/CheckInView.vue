<template>
  <div>
    <h1>Заселение клиента</h1>

    <v-form
      @submit.prevent="onSubmit"
      style="max-width: 600px;"
    >
      <v-text-field v-model="form.passport_number" label="Паспорт" required />
      <v-text-field v-model="form.last_name" label="Фамилия" required />
      <v-text-field v-model="form.first_name" label="Имя" required />
      <v-text-field v-model="form.patronymic" label="Отчество" />
      <v-text-field v-model="form.city" label="Город" required />

      <v-select
        v-model="form.room_number"
        :items="roomsOptions"
        label="Номер комнаты"
        item-title="label"
        item-value="value"
        required
        class="mt-4"
      />

      <v-text-field
        v-model="form.check_in"
        label="Дата заезда (YYYY-MM-DD)"
        required
        class="mt-4"
      />
      <v-text-field
        v-model="form.check_out"
        label="Дата выезда (YYYY-MM-DD, можно пусто)"
        class="mt-2"
      />

      <v-btn :loading="loading" type="submit" color="primary" class="mt-4">
        Заселить
      </v-btn>
    </v-form>

    <v-alert v-if="successMsg" type="success" class="mt-4">
      {{ successMsg }}
    </v-alert>
    <v-alert v-if="errorMsg" type="error" class="mt-2">
      {{ errorMsg }}
    </v-alert>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '../api/api'

const form = reactive({
  passport_number: '',
  last_name: '',
  first_name: '',
  patronymic: '',
  city: '',
  room_number: '',
  check_in: '',
  check_out: '',
})

const roomsOptions = ref([])
const loading = ref(false)
const successMsg = ref('')
const errorMsg = ref('')

onMounted(async () => {
  try {
    const { data } = await api.get('/api/rooms/')
    roomsOptions.value = data.map(r => ({
      label: `${r.number} (этаж ${r.floor}, ${r.room_type})`,
      value: r.number,
    }))
  } catch (e) {
    errorMsg.value = 'Не удалось загрузить список номеров'
  }
})

const onSubmit = async () => {
  loading.value = true
  successMsg.value = ''
  errorMsg.value = ''

  try {
    const payload = {
      passport_number: form.passport_number,
      last_name: form.last_name,
      first_name: form.first_name,
      patronymic: form.patronymic || '',
      city: form.city,
      room_number: form.room_number,
      check_in: form.check_in,
      check_out: form.check_out || null,
    }

    const { data } = await api.post('/api/actions/check-in/', payload)

    successMsg.value = `Клиент ${data.client.last_name} заселён в номер ${data.room.number}. Итоговая стоимость: ${data.total_price} ₽`
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || 'Ошибка заселения'
  } finally {
    loading.value = false
  }
}
</script>
