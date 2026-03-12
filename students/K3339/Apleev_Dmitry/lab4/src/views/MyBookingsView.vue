<template>
  <v-row>
    <v-col cols="12">
      <v-card>
        <v-card-title class="text-h6">мои брони</v-card-title>
        <v-card-text>
          <v-alert v-if="error" type="error" density="compact" class="mb-2">
            {{ error }}
          </v-alert>
          <v-progress-linear v-if="loading" indeterminate color="primary" class="mb-2" />

          <div v-if="bookings.length === 0 && !loading" class="text-medium-emphasis">
            у вас пока нет бронирований
          </div>
          <v-table v-else-if="bookings.length > 0">
            <thead>
              <tr>
                <th>номер</th>
                <th>тип</th>
                <th>гость</th>
                <th>заезд — выезд</th>
                <th>цена/сутки</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="b in bookings" :key="b.id">
                <td>{{ b.room_number }}</td>
                <td>{{ b.room_type }}</td>
                <td>{{ b.guest_name }}</td>
                <td>{{ b.check_in_date }} — {{ b.check_out_date || '—' }}</td>
                <td>{{ b.price }} ₽</td>
                <td>
                  <v-btn variant="text" size="small" @click="$router.push('/my-bookings/' + b.id + '/edit')">
                    редактировать
                  </v-btn>
                  <v-btn variant="text" size="small" @click="$router.push('/rooms/' + b.room_id)">
                    к номеру
                  </v-btn>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { apiGetMyBookings } from '../api'

// список броней текущего пользователя
const bookings = ref([])
const loading = ref(false)
const error = ref('')

const loadBookings = async () => {
  loading.value = true
  error.value = ''
  try {
    const resp = await apiGetMyBookings()
    bookings.value = resp.data
  } catch (e) {
    error.value = 'не удалось загрузить список броней'
  } finally {
    loading.value = false
  }
}

onMounted(loadBookings)
</script>
