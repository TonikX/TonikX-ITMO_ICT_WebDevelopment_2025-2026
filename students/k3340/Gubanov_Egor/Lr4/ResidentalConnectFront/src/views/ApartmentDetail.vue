<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8" offset-md="2">
        <v-card v-if="apartment">
          <v-card-title class="d-flex align-center">
            <span>Квартира #{{ apartment.id }}</span>
            <v-spacer></v-spacer>
            <v-btn
              v-if="canEdit"
              color="primary"
              prepend-icon="mdi-pencil"
              @click="$router.push(`/apartments/${apartment.id}/edit`)"
            >
              Редактировать
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-card variant="outlined" class="mb-4">
              <v-card-title>Основная информация</v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <v-list-item-title>Номер квартиры</v-list-item-title>
                    <v-list-item-subtitle class="text-h6">{{ apartment.number }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Дом</v-list-item-title>
                    <v-list-item-subtitle>{{ apartment.building?.address || '-' }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Этаж</v-list-item-title>
                    <v-list-item-subtitle>{{ apartment.floor }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Площадь</v-list-item-title>
                    <v-list-item-subtitle>{{ apartment.area }} м²</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item v-if="apartment.rooms">
                    <v-list-item-title>Количество комнат</v-list-item-title>
                    <v-list-item-subtitle>{{ apartment.rooms }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Баланс счета</v-list-item-title>
                    <v-list-item-subtitle class="text-h6">{{ apartment.balance }} ₽</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item v-if="apartment.owner">
                    <v-list-item-title>Владелец</v-list-item-title>
                    <v-list-item-subtitle>
                      {{ apartment.owner.first_name }} {{ apartment.owner.last_name }} ({{ apartment.owner.username }})
                    </v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Дата создания</v-list-item-title>
                    <v-list-item-subtitle>{{ formatDateTime(apartment.created_at) }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>

            <!-- Связанные заявки -->
            <v-card variant="outlined" class="mb-4">
              <v-card-title>Заявки по этой квартире</v-card-title>
              <v-card-text>
                <v-btn
                  color="primary"
                  prepend-icon="mdi-clipboard-list"
                  @click="$router.push(`/service-requests?apartment=${apartment.id}`)"
                >
                  Просмотреть заявки
                </v-btn>
              </v-card-text>
            </v-card>

            <!-- Показания счетчиков -->
            <v-card variant="outlined">
              <v-card-title>Показания счетчиков</v-card-title>
              <v-card-text>
                <v-btn
                  color="primary"
                  prepend-icon="mdi-counter"
                  @click="$router.push(`/meter-readings?apartment=${apartment.id}`)"
                >
                  Просмотреть показания
                </v-btn>
              </v-card-text>
            </v-card>
          </v-card-text>
        </v-card>

        <v-card v-else-if="loading">
          <v-card-text>
            <v-skeleton-loader type="card"></v-skeleton-loader>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { apartmentsService } from '@/services/apartmentsService'
import { useAuthStore } from '@/stores/auth'
import { isDispatcher } from '@/utils/roleUtils'
import { formatDateTime } from '@/utils/dateUtils'

export default {
  name: 'ApartmentDetail',
  data() {
    return {
      apartment: null,
      loading: false,
    }
  },
  computed: {
    user() {
      return useAuthStore().user
    },
    canEdit() {
      return isDispatcher(this.user)
    },
  },
  async mounted() {
    await this.loadApartment()
  },
  methods: {
    async loadApartment() {
      this.loading = true
      try {
        this.apartment = await apartmentsService.getApartment(this.$route.params.id)
      } catch (error) {
        console.error('Error loading apartment:', error)
        this.$router.push('/apartments')
      } finally {
        this.loading = false
      }
    },
    formatDateTime,
  },
}
</script>

