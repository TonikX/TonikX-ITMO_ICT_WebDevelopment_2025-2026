<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>Статистика по показаниям счетчиков</v-card-title>
          <v-card-text>
            <v-row v-if="statistics">
              <!-- Общая статистика -->
              <v-col cols="12" md="4">
                <StatisticsCard
                  title="Всего показаний"
                  :value="statistics.total_readings"
                  icon="mdi-counter"
                  color="primary"
                />
              </v-col>
              <v-col cols="12" md="4">
                <StatisticsCard
                  title="Общий расход"
                  :value="statistics.total_consumption?.toFixed(2) || 0"
                  icon="mdi-chart-line"
                  color="success"
                />
              </v-col>
              <v-col cols="12" md="4">
                <StatisticsCard
                  title="Средний расход"
                  :value="(statistics.total_consumption / statistics.total_readings || 0).toFixed(2)"
                  icon="mdi-calculator"
                  color="info"
                />
              </v-col>

              <!-- Расход по типам счетчиков -->
              <v-col cols="12">
                <v-card variant="outlined">
                  <v-card-title>Расход по типам счетчиков</v-card-title>
                  <v-card-text>
                    <v-list>
                      <v-list-item
                        v-for="item in statistics.consumption_by_type"
                        :key="item.meter_type"
                      >
                        <v-list-item-title>
                          {{ item.meter_type_display }}
                        </v-list-item-title>
                        <template v-slot:append>
                          <div class="text-right">
                            <div class="text-h6">{{ item.total_consumption?.toFixed(2) || 0 }}</div>
                            <div class="text-caption">Количество: {{ item.count }}</div>
                            <div class="text-caption">Среднее: {{ item.avg_consumption?.toFixed(2) || 0 }}</div>
                          </div>
                        </template>
                      </v-list-item>
                    </v-list>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Средние значения по типам -->
              <v-col cols="12" md="6">
                <v-card variant="outlined">
                  <v-card-title>Средние значения по типам</v-card-title>
                  <v-card-text>
                    <v-list>
                      <v-list-item
                        v-for="item in statistics.avg_values_by_type"
                        :key="item.meter_type"
                      >
                        <v-list-item-title>
                          {{ item.meter_type_display }}
                        </v-list-item-title>
                        <template v-slot:append>
                          <v-chip color="primary">
                            {{ item.avg_value?.toFixed(2) || 0 }}
                          </v-chip>
                        </template>
                      </v-list-item>
                    </v-list>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Топ квартир по расходу -->
              <v-col cols="12" md="6">
                <v-card variant="outlined">
                  <v-card-title>Топ квартир по расходу</v-card-title>
                  <v-card-text>
                    <v-list>
                      <v-list-item
                        v-for="(item, index) in statistics.top_apartments_by_consumption"
                        :key="index"
                      >
                        <v-list-item-title>
                          {{ item.apartment__building__address }}, кв. {{ item.apartment__number }}
                        </v-list-item-title>
                        <template v-slot:append>
                          <div class="text-right">
                            <div class="text-h6">{{ item.total_consumption?.toFixed(2) || 0 }}</div>
                            <div class="text-caption">Показаний: {{ item.reading_count }}</div>
                          </div>
                        </template>
                      </v-list-item>
                    </v-list>
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
import { meterReadingsService } from '@/services/meterReadingsService'
import StatisticsCard from '@/components/StatisticsCard.vue'

export default {
  name: 'MeterReadingsStatistics',
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
        this.statistics = await meterReadingsService.getStatistics()
      } catch (error) {
        console.error('Error loading statistics:', error)
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

