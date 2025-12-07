<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex align-center">
            <span>Показания счетчиков</span>
            <v-spacer></v-spacer>
            <v-btn
              v-if="canCreate"
              color="primary"
              prepend-icon="mdi-plus"
              @click="$router.push('/meter-readings/new')"
            >
              Подать показания
            </v-btn>
          </v-card-title>
          <v-card-text>
            <!-- Фильтры -->
            <v-row class="mb-4">
              <v-col cols="12" md="3">
                <v-select
                  v-model="filters.meter_type"
                  :items="meterTypeOptions"
                  label="Тип счетчика"
                  clearable
                  variant="outlined"
                  density="compact"
                ></v-select>
              </v-col>
              <v-col cols="12" md="3">
                <ApartmentSelect
                  v-model="filters.apartment"
                  label="Квартира"
                  :error-messages="[]"
                />
              </v-col>
              <v-col cols="12" md="3">
                <v-text-field
                  v-model="filters.date_recorded"
                  label="Дата подачи"
                  type="date"
                  variant="outlined"
                  density="compact"
                  clearable
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="3" class="d-flex align-center">
                <v-btn
                  color="primary"
                  @click="loadReadings"
                  prepend-icon="mdi-refresh"
                >
                  Обновить
                </v-btn>
              </v-col>
            </v-row>

            <!-- Таблица показаний -->
            <v-data-table
              :headers="headers"
              :items="readings"
              :loading="loading"
              :items-per-page="20"
              :items-per-page-options="[10, 20, 50, 100]"
              :server-items-length="totalCount"
              @update:options="handleOptionsUpdate"
            >
              <template v-slot:item.meter_type="{ item }">
                <v-chip
                  :color="getMeterTypeColor(item.meter_type)"
                  size="small"
                >
                  {{ getMeterTypeLabel(item.meter_type) }}
                </v-chip>
              </template>
              <template v-slot:item.apartment="{ item }">
                {{ item.apartment ? `Кв. ${item.apartment.number}, ${item.apartment.building?.address}` : '-' }}
              </template>
              <template v-slot:item.value="{ item }">
                {{ item.value }}
              </template>
              <template v-slot:item.date_recorded="{ item }">
                {{ formatDate(item.date_recorded) }}
              </template>
              <template v-slot:item.created_at="{ item }">
                {{ formatDateTime(item.created_at) }}
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn
                  icon="mdi-eye"
                  size="small"
                  variant="text"
                  @click="$router.push(`/meter-readings/${item.id}`)"
                ></v-btn>
              </template>
              <template v-slot:no-data>
                <div class="text-center py-8">
                  <v-icon size="64" color="grey-lighten-1">mdi-counter</v-icon>
                  <div class="text-h6 mt-4 text-grey">Нет показаний</div>
                </div>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { meterReadingsService } from '@/services/meterReadingsService'
import { useAuthStore } from '@/stores/auth'
import { isResident, isDispatcher } from '@/utils/roleUtils'
import { formatDate, formatDateTime } from '@/utils/dateUtils'
import { getMeterTypeOptions, getMeterTypeLabel, getMeterTypeColor } from '@/utils/statusUtils'
import ApartmentSelect from '@/components/ApartmentSelect.vue'

export default {
  name: 'MeterReadingsList',
  components: {
    ApartmentSelect,
  },
  data() {
    return {
      readings: [],
      loading: false,
      totalCount: 0,
      filters: {
        meter_type: null,
        apartment: null,
        date_recorded: null,
      },
      meterTypeOptions: getMeterTypeOptions(),
      headers: [
        { title: 'ID', key: 'id', sortable: true },
        { title: 'Тип счетчика', key: 'meter_type', sortable: true },
        { title: 'Квартира', key: 'apartment', sortable: false },
        { title: 'Значение', key: 'value', sortable: true },
        { title: 'Дата подачи', key: 'date_recorded', sortable: true },
        { title: 'Дата создания', key: 'created_at', sortable: true },
        { title: 'Действия', key: 'actions', sortable: false },
      ],
      pagination: {
        page: 1,
        itemsPerPage: 20,
        sortBy: [],
      },
    }
  },
  computed: {
    user() {
      return useAuthStore().user
    },
    canCreate() {
      return isResident(this.user) || isDispatcher(this.user)
    },
  },
  async mounted() {
    await this.loadReadings()
  },
  methods: {
    async loadReadings() {
      this.loading = true
      try {
        const params = {
          page: this.pagination.page,
          page_size: this.pagination.itemsPerPage,
        }
        
        if (this.filters.meter_type) {
          params.meter_type = this.filters.meter_type
        }
        if (this.filters.apartment) {
          params.apartment = this.filters.apartment
        }
        if (this.filters.date_recorded) {
          params.date_recorded = this.filters.date_recorded
        }
        if (this.pagination.sortBy.length > 0) {
          params.ordering = this.pagination.sortBy[0].key
          if (this.pagination.sortBy[0].order === 'desc') {
            params.ordering = `-${params.ordering}`
          }
        }

        const data = await meterReadingsService.getMeterReadings(params)
        this.readings = data.results || []
        this.totalCount = data.count || 0
      } catch (error) {
        console.error('Error loading readings:', error)
        this.readings = []
      } finally {
        this.loading = false
      }
    },
    handleOptionsUpdate(options) {
      this.pagination.page = options.page
      this.pagination.itemsPerPage = options.itemsPerPage
      this.pagination.sortBy = options.sortBy || []
      this.loadReadings()
    },
    formatDate,
    formatDateTime,
    getMeterTypeLabel,
    getMeterTypeColor,
  },
}
</script>

