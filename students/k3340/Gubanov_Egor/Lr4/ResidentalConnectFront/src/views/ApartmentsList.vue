<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex align-center">
            <span>Квартиры</span>
            <v-spacer></v-spacer>
            <v-btn
              v-if="canCreate"
              color="primary"
              prepend-icon="mdi-plus"
              @click="$router.push('/apartments/new')"
            >
              Создать квартиру
            </v-btn>
          </v-card-title>
          <v-card-text>
            <!-- Фильтры -->
            <v-row class="mb-4">
              <v-col cols="12" md="3">
                <BuildingSelect
                  v-model="filters.building"
                  label="Дом"
                  :error-messages="[]"
                />
              </v-col>
              <v-col cols="12" md="3">
                <v-text-field
                  v-model="filters.floor"
                  label="Этаж"
                  type="number"
                  variant="outlined"
                  density="compact"
                  clearable
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="3">
                <v-text-field
                  v-model="filters.search"
                  label="Поиск"
                  prepend-inner-icon="mdi-magnify"
                  variant="outlined"
                  density="compact"
                  clearable
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="3" class="d-flex align-center">
                <v-btn
                  color="primary"
                  @click="loadApartments"
                  prepend-icon="mdi-refresh"
                >
                  Обновить
                </v-btn>
              </v-col>
            </v-row>

            <!-- Таблица квартир -->
            <v-data-table
              :headers="headers"
              :items="apartments"
              :loading="loading"
              :items-per-page="20"
              :items-per-page-options="[10, 20, 50, 100]"
              :server-items-length="totalCount"
              @update:options="handleOptionsUpdate"
            >
              <template v-slot:item.building="{ item }">
                {{ item.building?.address || '-' }}
              </template>
              <template v-slot:item.owner="{ item }">
                {{ item.owner ? `${item.owner.first_name || ''} ${item.owner.last_name || ''} (${item.owner.username})` : '-' }}
              </template>
              <template v-slot:item.area="{ item }">
                {{ item.area }} м²
              </template>
              <template v-slot:item.balance="{ item }">
                {{ item.balance }} ₽
              </template>
              <template v-slot:item.created_at="{ item }">
                {{ formatDateTime(item.created_at) }}
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn
                  icon="mdi-eye"
                  size="small"
                  variant="text"
                  @click="$router.push(`/apartments/${item.id}`)"
                ></v-btn>
                <v-btn
                  v-if="canEdit"
                  icon="mdi-pencil"
                  size="small"
                  variant="text"
                  @click="$router.push(`/apartments/${item.id}/edit`)"
                ></v-btn>
              </template>
              <template v-slot:no-data>
                <div class="text-center py-8">
                  <v-icon size="64" color="grey-lighten-1">mdi-home-off</v-icon>
                  <div class="text-h6 mt-4 text-grey">Нет квартир</div>
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
import { apartmentsService } from '@/services/apartmentsService'
import { useAuthStore } from '@/stores/auth'
import { isDispatcher } from '@/utils/roleUtils'
import { formatDateTime } from '@/utils/dateUtils'
import BuildingSelect from '@/components/BuildingSelect.vue'

export default {
  name: 'ApartmentsList',
  components: {
    BuildingSelect,
  },
  data() {
    return {
      apartments: [],
      loading: false,
      totalCount: 0,
      filters: {
        building: null,
        floor: null,
        search: null,
      },
      headers: [
        { title: 'ID', key: 'id', sortable: true },
        { title: 'Номер', key: 'number', sortable: true },
        { title: 'Дом', key: 'building', sortable: false },
        { title: 'Этаж', key: 'floor', sortable: true },
        { title: 'Площадь', key: 'area', sortable: true },
        { title: 'Комнат', key: 'rooms', sortable: true },
        { title: 'Владелец', key: 'owner', sortable: false },
        { title: 'Баланс', key: 'balance', sortable: true },
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
      return isDispatcher(this.user)
    },
    canEdit() {
      return isDispatcher(this.user)
    },
  },
  async mounted() {
    await this.loadApartments()
  },
  methods: {
    async loadApartments() {
      this.loading = true
      try {
        const params = {
          page: this.pagination.page,
          page_size: this.pagination.itemsPerPage,
        }
        
        if (this.filters.building) {
          params.building = this.filters.building
        }
        if (this.filters.floor) {
          params.floor = this.filters.floor
        }
        if (this.filters.search) {
          params.search = this.filters.search
        }
        if (this.pagination.sortBy.length > 0) {
          params.ordering = this.pagination.sortBy[0].key
          if (this.pagination.sortBy[0].order === 'desc') {
            params.ordering = `-${params.ordering}`
          }
        }

        const data = await apartmentsService.getApartments(params)
        this.apartments = data.results || []
        this.totalCount = data.count || 0
      } catch (error) {
        console.error('Error loading apartments:', error)
        this.apartments = []
      } finally {
        this.loading = false
      }
    },
    handleOptionsUpdate(options) {
      this.pagination.page = options.page
      this.pagination.itemsPerPage = options.itemsPerPage
      this.pagination.sortBy = options.sortBy || []
      this.loadApartments()
    },
    formatDateTime,
  },
}
</script>

