<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex align-center">
            <span>Мои заявки</span>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              prepend-icon="mdi-plus"
              @click="$router.push('/service-requests/new')"
            >
              Создать заявку
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="requests"
              :loading="loading"
              :items-per-page="20"
              :items-per-page-options="[10, 20, 50]"
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
                {{ item.apartment ? `Кв. ${item.apartment.number}` : '-' }}
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
                  <div class="text-h6 mt-4 text-grey">У вас пока нет заявок</div>
                  <v-btn
                    color="primary"
                    class="mt-4"
                    @click="$router.push('/service-requests/new')"
                  >
                    Создать первую заявку
                  </v-btn>
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
import { formatDateTime } from '@/utils/dateUtils'
import StatusChip from '@/components/StatusChip.vue'
import PriorityChip from '@/components/PriorityChip.vue'

export default {
  name: 'MyRequests',
  components: {
    StatusChip,
    PriorityChip,
  },
  data() {
    return {
      requests: [],
      loading: false,
      totalCount: 0,
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
      },
    }
  },
  async mounted() {
    await this.loadRequests()
  },
  methods: {
    async loadRequests() {
      this.loading = true
      try {
        const params = {
          page: this.pagination.page,
          page_size: this.pagination.itemsPerPage,
        }
        const data = await serviceRequestsService.getMyRequests(params)
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
      this.loadRequests()
    },
    formatDateTime,
  },
}
</script>

