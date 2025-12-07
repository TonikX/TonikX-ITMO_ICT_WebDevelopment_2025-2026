<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>Статистика по заявкам</v-card-title>
          <v-card-text>
            <v-row v-if="statistics">
              <!-- Общая статистика -->
              <v-col cols="12" md="3">
                <StatisticsCard
                  title="Всего заявок"
                  :value="statistics.total_requests"
                  icon="mdi-clipboard-list"
                  color="primary"
                />
              </v-col>
              <v-col cols="12" md="3">
                <StatisticsCard
                  title="Выполнено"
                  :value="statistics.completed_requests"
                  icon="mdi-check-circle"
                  color="success"
                />
              </v-col>
              <v-col cols="12" md="3">
                <StatisticsCard
                  title="В работе"
                  :value="statistics.in_progress_requests"
                  icon="mdi-progress-wrench"
                  color="warning"
                />
              </v-col>
              <v-col cols="12" md="3">
                <StatisticsCard
                  title="Новых"
                  :value="statistics.new_requests"
                  icon="mdi-new-box"
                  color="info"
                />
              </v-col>

              <!-- Распределение по статусам -->
              <v-col cols="12" md="6">
                <v-card variant="outlined">
                  <v-card-title>Распределение по статусам</v-card-title>
                  <v-card-text>
                    <v-list>
                      <v-list-item
                        v-for="item in statistics.status_distribution"
                        :key="item.status"
                      >
                        <v-list-item-title>
                          {{ getRequestStatusLabel(item.status) }}
                        </v-list-item-title>
                        <template v-slot:append>
                          <v-chip color="primary">{{ item.count }}</v-chip>
                        </template>
                      </v-list-item>
                    </v-list>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Распределение по приоритетам -->
              <v-col cols="12" md="6">
                <v-card variant="outlined">
                  <v-card-title>Распределение по приоритетам</v-card-title>
                  <v-card-text>
                    <v-list>
                      <v-list-item
                        v-for="item in statistics.priority_distribution"
                        :key="item.priority"
                      >
                        <v-list-item-title>
                          {{ getRequestPriorityLabel(item.priority) }}
                        </v-list-item-title>
                        <template v-slot:append>
                          <v-chip color="primary">{{ item.count }}</v-chip>
                        </template>
                      </v-list-item>
                    </v-list>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Распределение по категориям -->
              <v-col cols="12" md="6">
                <v-card variant="outlined">
                  <v-card-title>Распределение по категориям</v-card-title>
                  <v-card-text>
                    <v-list>
                      <v-list-item
                        v-for="item in statistics.category_distribution"
                        :key="item.category__name"
                      >
                        <v-list-item-title>{{ item.category__name }}</v-list-item-title>
                        <template v-slot:append>
                          <v-chip color="primary">{{ item.count }}</v-chip>
                        </template>
                      </v-list-item>
                    </v-list>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Среднее время решения -->
              <v-col cols="12" md="6">
                <v-card variant="outlined">
                  <v-card-title>Среднее время решения</v-card-title>
                  <v-card-text>
                    <div class="text-h4">
                      {{ statistics.average_resolution_time_days?.toFixed(1) || 0 }} дней
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>

            <v-skeleton-loader v-else type="card"></v-skeleton-loader>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { serviceRequestsService } from '@/services/serviceRequestsService'
import { getRequestStatusLabel, getRequestPriorityLabel } from '@/utils/statusUtils'
import StatisticsCard from '@/components/StatisticsCard.vue'

export default {
  name: 'ServiceRequestsStatistics',
  components: {
    StatisticsCard,
  },
  data() {
    return {
      statistics: null,
      loading: false,
    }
  },
  async mounted() {
    await this.loadStatistics()
  },
  methods: {
    async loadStatistics() {
      this.loading = true
      try {
        this.statistics = await serviceRequestsService.getStatistics()
      } catch (error) {
        console.error('Error loading statistics:', error)
      } finally {
        this.loading = false
      }
    },
    getRequestStatusLabel,
    getRequestPriorityLabel,
  },
}
</script>

