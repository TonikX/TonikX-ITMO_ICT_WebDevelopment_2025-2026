<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8" offset-md="2">
        <v-card v-if="reading">
          <v-card-title class="d-flex align-center">
            <span>Показания счетчика #{{ reading.id }}</span>
            <v-spacer></v-spacer>
            <v-chip
              :color="getMeterTypeColor(reading.meter_type)"
              size="large"
            >
              {{ getMeterTypeLabel(reading.meter_type) }}
            </v-chip>
          </v-card-title>
          <v-card-text>
            <v-card variant="outlined" class="mb-4">
              <v-card-title>Информация о показаниях</v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <v-list-item-title>Квартира</v-list-item-title>
                    <v-list-item-subtitle>
                      {{ reading.apartment ? `Кв. ${reading.apartment.number}, ${reading.apartment.building?.address}` : '-' }}
                    </v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Тип счетчика</v-list-item-title>
                    <v-list-item-subtitle>
                      {{ getMeterTypeLabel(reading.meter_type) }}
                    </v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Значение</v-list-item-title>
                    <v-list-item-subtitle class="text-h6">
                      {{ reading.value }}
                    </v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Дата подачи</v-list-item-title>
                    <v-list-item-subtitle>
                      {{ formatDate(reading.date_recorded) }}
                    </v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Дата создания записи</v-list-item-title>
                    <v-list-item-subtitle>
                      {{ formatDateTime(reading.created_at) }}
                    </v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>

            <!-- Действия для диспетчера -->
            <div v-if="canEdit" class="d-flex gap-2">
              <v-btn
                color="primary"
                prepend-icon="mdi-pencil"
                @click="$router.push(`/meter-readings/${reading.id}/edit`)"
              >
                Редактировать
              </v-btn>
              <v-btn
                color="error"
                prepend-icon="mdi-delete"
                @click="confirmDelete"
              >
                Удалить
              </v-btn>
            </div>
          </v-card-text>
        </v-card>

        <v-card v-else-if="loading">
          <v-card-text>
            <v-skeleton-loader type="card"></v-skeleton-loader>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить эти показания?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="deleteDialog = false">Отмена</v-btn>
          <v-btn color="error" @click="deleteReading">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { meterReadingsService } from '@/services/meterReadingsService'
import { useAuthStore } from '@/stores/auth'
import { isDispatcher } from '@/utils/roleUtils'
import { formatDate, formatDateTime } from '@/utils/dateUtils'
import { getMeterTypeLabel, getMeterTypeColor } from '@/utils/statusUtils'

export default {
  name: 'MeterReadingDetail',
  data() {
    return {
      reading: null,
      loading: false,
      deleteDialog: false,
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
    await this.loadReading()
  },
  methods: {
    async loadReading() {
      this.loading = true
      try {
        this.reading = await meterReadingsService.getMeterReading(this.$route.params.id)
      } catch (error) {
        console.error('Error loading reading:', error)
        this.$router.push('/meter-readings')
      } finally {
        this.loading = false
      }
    },
    confirmDelete() {
      this.deleteDialog = true
    },
    async deleteReading() {
      this.loading = true
      try {
        await meterReadingsService.deleteMeterReading(this.reading.id)
        this.$router.push('/meter-readings')
      } catch (error) {
        console.error('Error deleting reading:', error)
      } finally {
        this.loading = false
        this.deleteDialog = false
      }
    },
    formatDate,
    formatDateTime,
    getMeterTypeLabel,
    getMeterTypeColor,
  },
}
</script>

