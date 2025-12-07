<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex align-center">
            <span>Заявки на обслуживание</span>
            <v-spacer></v-spacer>
            <v-btn
              v-if="canCreate"
              color="primary"
              prepend-icon="mdi-plus"
              @click="$router.push('/service-requests/new')"
            >
              Создать заявку
            </v-btn>
          </v-card-title>
          <v-card-text>
            <!-- Фильтры -->
            <v-row class="mb-4">
              <v-col cols="12" md="3">
                <v-select
                  v-model="filters.status"
                  :items="statusOptions"
                  label="Статус"
                  clearable
                  variant="outlined"
                  density="compact"
                ></v-select>
              </v-col>
              <v-col cols="12" md="3">
                <v-select
                  v-model="filters.category"
                  :items="categoryOptions"
                  label="Категория"
                  clearable
                  variant="outlined"
                  density="compact"
                ></v-select>
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
                  @click="loadRequests"
                  prepend-icon="mdi-refresh"
                >
                  Обновить
                </v-btn>
              </v-col>
            </v-row>

            <!-- Таблица заявок -->
            <v-data-table
              :headers="headers"
              :items="requests"
              :loading="loading"
              :items-per-page="20"
              :items-per-page-options="[10, 20, 50, 100]"
              :server-items-length="totalCount"
              @update:options="handleOptionsUpdate"
            >
              <template v-slot:item.status="{ item }">
                <StatusChip :status="item.status" />
              </template>
              <template v-slot:item.priority="{ item }">
                <PriorityChip :priority="item.priority" />
              </template>
              <template v-slot:item.category="{ item }">
                {{ item.category?.name || '-' }}
              </template>
              <template v-slot:item.apartment="{ item }">
                {{ item.apartment ? `Кв. ${item.apartment.number}, ${item.apartment.building?.address}` : '-' }}
              </template>
              <template v-slot:item.created_at="{ item }">
                {{ formatDateTime(item.created_at) }}
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn
                  icon="mdi-eye"
                  size="small"
                  variant="text"
                  @click="$router.push(`/service-requests/${item.id}`)"
                ></v-btn>
              </template>
              <template v-slot:no-data>
                <div class="text-center py-8">
                  <v-icon size="64" color="grey-lighten-1">mdi-clipboard-text-off</v-icon>
                  <div class="text-h6 mt-4 text-grey">Нет заявок</div>
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
import { serviceRequestsService } from '@/services/serviceRequestsService'
import { categoriesService } from '@/services/categoriesService'
import { useAuthStore } from '@/stores/auth'
import { isResident, isMaster, isDispatcher } from '@/utils/roleUtils'
import { formatDateTime } from '@/utils/dateUtils'
import { getRequestStatusOptions } from '@/utils/statusUtils'
import StatusChip from '@/components/StatusChip.vue'
import PriorityChip from '@/components/PriorityChip.vue'

export default {
  name: 'ServiceRequestsList',
  components: {
    StatusChip,
    PriorityChip,
  },
  data() {
    return {
      requests: [],
      categories: [],
      loading: false,
      totalCount: 0,
      filters: {
        status: null,
        category: null,
        search: null,
      },
      statusOptions: getRequestStatusOptions(),
      categoryOptions: [],
      headers: [
        { title: 'ID', key: 'id', sortable: true },
        { title: 'Тема', key: 'title', sortable: true },
        { title: 'Статус', key: 'status', sortable: true },
        { title: 'Приоритет', key: 'priority', sortable: true },
        { title: 'Категория', key: 'category', sortable: false },
        { title: 'Квартира', key: 'apartment', sortable: false },
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
    await this.loadCategories()
    await this.loadRequests()
  },
  methods: {
    async loadCategories() {
      try {
        const data = await categoriesService.getCategories()
        this.categories = Array.isArray(data) ? data : data.results || []
        this.categoryOptions = this.categories.map(cat => ({
          value: cat.id,
          title: cat.name,
        }))
      } catch (error) {
        console.error('Error loading categories:', error)
      }
    },
    async loadRequests() {
      this.loading = true
      try {
        const params = {
          page: this.pagination.page,
          page_size: this.pagination.itemsPerPage,
        }
        
        if (this.filters.status) {
          params.status = this.filters.status
        }
        if (this.filters.category) {
          params.category = this.filters.category
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

        const data = await serviceRequestsService.getServiceRequests(params)
        this.requests = data.results || []
        this.totalCount = data.count || 0
      } catch (error) {
        console.error('Error loading requests:', error)
        this.requests = []
      } finally {
        this.loading = false
      }
    },
    handleOptionsUpdate(options) {
      this.pagination.page = options.page
      this.pagination.itemsPerPage = options.itemsPerPage
      this.pagination.sortBy = options.sortBy || []
      this.loadRequests()
    },
    formatDateTime,
  },
}
</script>

