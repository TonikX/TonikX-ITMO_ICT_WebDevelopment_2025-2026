<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">Добро пожаловать, {{ userName }}!</h1>
      </v-col>
    </v-row>

    <!-- Dashboard для жильца -->
    <template v-if="userRole === 'resident'">
      <v-row>
        <v-col cols="12" md="4">
          <v-card class="pa-4" color="primary" dark>
            <div class="d-flex align-center">
              <v-icon size="48" class="mr-4">mdi-clipboard-list</v-icon>
              <div>
                <div class="text-h5">{{ myRequestsCount }}</div>
                <div class="text-caption">Мои заявки</div>
              </div>
            </div>
            <v-btn
              class="mt-4"
              variant="outlined"
              color="white"
              block
              @click="$router.push('/service-requests/my')"
            >
              Просмотреть
            </v-btn>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card class="pa-4" color="success" dark>
            <div class="d-flex align-center">
              <v-icon size="48" class="mr-4">mdi-counter</v-icon>
              <div>
                <div class="text-h5">{{ meterReadingsCount }}</div>
                <div class="text-caption">Показания счетчиков</div>
              </div>
            </div>
            <v-btn
              class="mt-4"
              variant="outlined"
              color="white"
              block
              @click="$router.push('/meter-readings')"
            >
              Просмотреть
            </v-btn>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card class="pa-4" color="info" dark>
            <div class="d-flex align-center">
              <v-icon size="48" class="mr-4">mdi-home</v-icon>
              <div>
                <div class="text-h5">{{ apartmentsCount }}</div>
                <div class="text-caption">Мои квартиры</div>
              </div>
            </div>
            <v-btn
              class="mt-4"
              variant="outlined"
              color="white"
              block
              @click="$router.push('/apartments')"
            >
              Просмотреть
            </v-btn>
          </v-card>
        </v-col>
      </v-row>

      <v-row class="mt-4">
        <v-col cols="12">
          <v-card>
            <v-card-title>Быстрые действия</v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12" md="6">
                  <v-btn
                    color="primary"
                    size="large"
                    prepend-icon="mdi-plus-circle"
                    block
                    @click="$router.push('/service-requests/new')"
                  >
                    Подать заявку
                  </v-btn>
                </v-col>
                <v-col cols="12" md="6">
                  <v-btn
                    color="success"
                    size="large"
                    prepend-icon="mdi-plus"
                    block
                    @click="$router.push('/meter-readings/new')"
                  >
                    Подать показания
                  </v-btn>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Последние заявки -->
      <v-row class="mt-4">
        <v-col cols="12">
          <v-card>
            <v-card-title class="d-flex align-center">
              <span>Последние заявки</span>
              <v-spacer></v-spacer>
              <v-btn
                variant="text"
                size="small"
                @click="$router.push('/service-requests/my')"
              >
                Все заявки
              </v-btn>
            </v-card-title>
            <v-card-text>
              <v-list v-if="recentRequests.length > 0">
                <v-list-item
                  v-for="request in recentRequests"
                  :key="request.id"
                  @click="$router.push(`/service-requests/${request.id}`)"
                >
                  <template v-slot:prepend>
                    <StatusChip :status="request.status" size="small" />
                  </template>
                  <v-list-item-title>{{ request.title }}</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ formatDateTime(request.created_at) }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
              <div v-else class="text-center py-8 text-grey">
                Нет заявок
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>

    <!-- Dashboard для мастера -->
    <template v-if="userRole === 'master'">
      <v-row>
        <v-col cols="12" md="6">
          <v-card class="pa-4" color="warning" dark>
            <div class="d-flex align-center">
              <v-icon size="48" class="mr-4">mdi-clipboard-check</v-icon>
              <div>
                <div class="text-h5">{{ assignedRequestsCount }}</div>
                <div class="text-caption">Назначенные заявки</div>
              </div>
            </div>
            <v-btn
              class="mt-4"
              variant="outlined"
              color="white"
              block
              @click="$router.push('/service-requests/assigned')"
            >
              Просмотреть
            </v-btn>
          </v-card>
        </v-col>
        <v-col cols="12" md="6">
          <v-card class="pa-4" color="info" dark>
            <div class="d-flex align-center">
              <v-icon size="48" class="mr-4">mdi-clipboard-list</v-icon>
              <div>
                <div class="text-h5">{{ allRequestsCount }}</div>
                <div class="text-caption">Все заявки</div>
              </div>
            </div>
            <v-btn
              class="mt-4"
              variant="outlined"
              color="white"
              block
              @click="$router.push('/service-requests')"
            >
              Просмотреть
            </v-btn>
          </v-card>
        </v-col>
      </v-row>

      <!-- Назначенные заявки -->
      <v-row class="mt-4">
        <v-col cols="12">
          <v-card>
            <v-card-title class="d-flex align-center">
              <span>Назначенные мне заявки</span>
              <v-spacer></v-spacer>
              <v-btn
                variant="text"
                size="small"
                @click="$router.push('/service-requests/assigned')"
              >
                Все заявки
              </v-btn>
            </v-card-title>
            <v-card-text>
              <v-list v-if="assignedRequests.length > 0">
                <v-list-item
                  v-for="request in assignedRequests"
                  :key="request.id"
                  @click="$router.push(`/service-requests/${request.id}`)"
                >
                  <template v-slot:prepend>
                    <StatusChip :status="request.status" size="small" />
                  </template>
                  <v-list-item-title>{{ request.title }}</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ formatDateTime(request.created_at) }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
              <div v-else class="text-center py-8 text-grey">
                Нет назначенных заявок
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>

    <!-- Dashboard для диспетчера -->
    <template v-if="userRole === 'dispatcher'">
      <v-row>
        <v-col cols="12" md="3">
          <StatisticsCard
            title="Дома"
            :value="buildingsCount"
            icon="mdi-office-building"
            color="primary"
          />
        </v-col>
        <v-col cols="12" md="3">
          <StatisticsCard
            title="Квартиры"
            :value="apartmentsCount"
            icon="mdi-home"
            color="success"
          />
        </v-col>
        <v-col cols="12" md="3">
          <StatisticsCard
            title="Заявки"
            :value="allRequestsCount"
            icon="mdi-clipboard-list"
            color="warning"
          />
        </v-col>
        <v-col cols="12" md="3">
          <StatisticsCard
            title="Показания"
            :value="meterReadingsCount"
            icon="mdi-counter"
            color="info"
          />
        </v-col>
      </v-row>

      <v-row class="mt-4">
        <v-col cols="12">
          <v-card>
            <v-card-title>Быстрые действия</v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12" md="3">
                  <v-btn
                    color="primary"
                    prepend-icon="mdi-office-building-plus"
                    block
                    @click="$router.push('/buildings/new')"
                  >
                    Создать дом
                  </v-btn>
                </v-col>
                <v-col cols="12" md="3">
                  <v-btn
                    color="success"
                    prepend-icon="mdi-home-plus"
                    block
                    @click="$router.push('/apartments/new')"
                  >
                    Создать квартиру
                  </v-btn>
                </v-col>
                <v-col cols="12" md="3">
                  <v-btn
                    color="warning"
                    prepend-icon="mdi-chart-bar"
                    block
                    @click="$router.push('/service-requests/statistics')"
                  >
                    Статистика заявок
                  </v-btn>
                </v-col>
                <v-col cols="12" md="3">
                  <v-btn
                    color="info"
                    prepend-icon="mdi-chart-line"
                    block
                    @click="$router.push('/buildings/statistics')"
                  >
                    Статистика домов
                  </v-btn>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Последние заявки -->
      <v-row class="mt-4">
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title class="d-flex align-center">
              <span>Последние заявки</span>
              <v-spacer></v-spacer>
              <v-btn
                variant="text"
                size="small"
                @click="$router.push('/service-requests')"
              >
                Все заявки
              </v-btn>
            </v-card-title>
            <v-card-text>
              <v-list v-if="recentRequests.length > 0">
                <v-list-item
                  v-for="request in recentRequests"
                  :key="request.id"
                  @click="$router.push(`/service-requests/${request.id}`)"
                >
                  <template v-slot:prepend>
                    <StatusChip :status="request.status" size="small" />
                  </template>
                  <v-list-item-title>{{ request.title }}</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ formatDateTime(request.created_at) }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
              <div v-else class="text-center py-8 text-grey">
                Нет заявок
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Статистика -->
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title>Краткая статистика</v-card-title>
            <v-card-text>
              <v-list>
                <v-list-item>
                  <v-list-item-title>Новых заявок</v-list-item-title>
                  <template v-slot:append>
                    <v-chip color="info">{{ newRequestsCount }}</v-chip>
                  </template>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title>В работе</v-list-item-title>
                  <template v-slot:append>
                    <v-chip color="warning">{{ inProgressRequestsCount }}</v-chip>
                  </template>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title>Выполнено</v-list-item-title>
                  <template v-slot:append>
                    <v-chip color="success">{{ doneRequestsCount }}</v-chip>
                  </template>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </v-container>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { serviceRequestsService } from '@/services/serviceRequestsService'
import { apartmentsService } from '@/services/apartmentsService'
import { buildingsService } from '@/services/buildingsService'
import { meterReadingsService } from '@/services/meterReadingsService'
import { formatDateTime } from '@/utils/dateUtils'
import StatusChip from '@/components/StatusChip.vue'
import StatisticsCard from '@/components/StatisticsCard.vue'

export default {
  name: 'Home',
  components: {
    StatusChip,
    StatisticsCard,
  },
  data() {
    return {
      myRequestsCount: 0,
      assignedRequestsCount: 0,
      allRequestsCount: 0,
      apartmentsCount: 0,
      buildingsCount: 0,
      meterReadingsCount: 0,
      newRequestsCount: 0,
      inProgressRequestsCount: 0,
      doneRequestsCount: 0,
      recentRequests: [],
      assignedRequests: [],
      loading: false,
    }
  },
  computed: {
    user() {
      return useAuthStore().user
    },
    userRole() {
      return useAuthStore().userRole
    },
    userName() {
      return useAuthStore().userName
    },
  },
  async mounted() {
    await this.loadDashboardData()
  },
  methods: {
    async loadDashboardData() {
      this.loading = true
      try {
        if (this.userRole === 'resident') {
          await Promise.all([
            this.loadMyRequests(),
            this.loadMyApartments(),
            this.loadMeterReadings(),
            this.loadRecentRequests(),
          ])
        } else if (this.userRole === 'master') {
          await Promise.all([
            this.loadAssignedRequests(),
            this.loadAllRequests(),
            this.loadRecentAssignedRequests(),
          ])
        } else if (this.userRole === 'dispatcher') {
          await Promise.all([
            this.loadAllRequests(),
            this.loadAllApartments(),
            this.loadAllBuildings(),
            this.loadAllMeterReadings(),
            this.loadRecentRequests(),
            this.loadRequestsStatistics(),
          ])
        }
      } catch (error) {
        console.error('Error loading dashboard data:', error)
      } finally {
        this.loading = false
      }
    },
    async loadMyRequests() {
      try {
        const data = await serviceRequestsService.getMyRequests({ page_size: 1 })
        this.myRequestsCount = data.count || 0
      } catch (error) {
        console.error('Error loading my requests:', error)
      }
    },
    async loadAssignedRequests() {
      try {
        const data = await serviceRequestsService.getAssignedToMe({ page_size: 1 })
        this.assignedRequestsCount = data.count || 0
      } catch (error) {
        console.error('Error loading assigned requests:', error)
      }
    },
    async loadAllRequests() {
      try {
        const data = await serviceRequestsService.getServiceRequests({ page_size: 1 })
        this.allRequestsCount = data.count || 0
      } catch (error) {
        console.error('Error loading all requests:', error)
      }
    },
    async loadMyApartments() {
      try {
        const data = await apartmentsService.getApartments({ page_size: 1 })
        this.apartmentsCount = data.count || 0
      } catch (error) {
        console.error('Error loading apartments:', error)
      }
    },
    async loadAllApartments() {
      try {
        const data = await apartmentsService.getApartments({ page_size: 1 })
        this.apartmentsCount = data.count || 0
      } catch (error) {
        console.error('Error loading apartments:', error)
      }
    },
    async loadAllBuildings() {
      try {
        const data = await buildingsService.getBuildings({ page_size: 1 })
        this.buildingsCount = data.count || 0
      } catch (error) {
        console.error('Error loading buildings:', error)
      }
    },
    async loadMeterReadings() {
      try {
        const data = await meterReadingsService.getMeterReadings({ page_size: 1 })
        this.meterReadingsCount = data.count || 0
      } catch (error) {
        console.error('Error loading meter readings:', error)
      }
    },
    async loadAllMeterReadings() {
      try {
        const data = await meterReadingsService.getMeterReadings({ page_size: 1 })
        this.meterReadingsCount = data.count || 0
      } catch (error) {
        console.error('Error loading meter readings:', error)
      }
    },
    async loadRecentRequests() {
      try {
        const data = await serviceRequestsService.getServiceRequests({ page_size: 5 })
        this.recentRequests = data.results || []
      } catch (error) {
        console.error('Error loading recent requests:', error)
      }
    },
    async loadRecentAssignedRequests() {
      try {
        const data = await serviceRequestsService.getAssignedToMe({ page_size: 5 })
        this.assignedRequests = data.results || []
      } catch (error) {
        console.error('Error loading assigned requests:', error)
      }
    },
    async loadRequestsStatistics() {
      try {
        const stats = await serviceRequestsService.getStatistics()
        this.newRequestsCount = stats.new_requests || 0
        this.inProgressRequestsCount = stats.in_progress_requests || 0
        this.doneRequestsCount = stats.completed_requests || 0
      } catch (error) {
        console.error('Error loading requests statistics:', error)
      }
    },
    formatDateTime,
  },
}
</script>
