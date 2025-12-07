<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>Статистика по домам и квартирам</v-card-title>
          <v-card-text>
            <v-row v-if="statistics">
              <!-- Общая статистика -->
              <v-col cols="12" md="3">
                <StatisticsCard
                  title="Всего домов"
                  :value="statistics.total_buildings"
                  icon="mdi-office-building"
                  color="primary"
                />
              </v-col>
              <v-col cols="12" md="3">
                <StatisticsCard
                  title="Всего квартир"
                  :value="statistics.total_apartments"
                  icon="mdi-home"
                  color="success"
                />
              </v-col>
              <v-col cols="12" md="3">
                <StatisticsCard
                  title="Заселено"
                  :value="statistics.occupied_apartments"
                  icon="mdi-account-check"
                  color="info"
                />
              </v-col>
              <v-col cols="12" md="3">
                <StatisticsCard
                  title="Свободно"
                  :value="statistics.vacant_apartments"
                  icon="mdi-home-remove"
                  color="warning"
                />
              </v-col>

              <!-- Процент заселенности -->
              <v-col cols="12" md="6">
                <v-card variant="outlined">
                  <v-card-title>Процент заселенности</v-card-title>
                  <v-card-text>
                    <div class="text-h3 text-center">
                      {{ statistics.occupancy_rate?.toFixed(2) || 0 }}%
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Общая площадь -->
              <v-col cols="12" md="6">
                <v-card variant="outlined">
                  <v-card-title>Общая площадь</v-card-title>
                  <v-card-text>
                    <div class="text-h3 text-center">
                      {{ statistics.total_area?.toFixed(2) || 0 }} м²
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Статистика по домам -->
              <v-col cols="12">
                <v-card variant="outlined">
                  <v-card-title>Статистика по домам</v-card-title>
                  <v-card-text>
                    <v-data-table
                      :headers="buildingHeaders"
                      :items="statistics.buildings_statistics || []"
                    >
                      <template v-slot:item.apartment_count="{ item }">
                        {{ item.apartment_count }}
                      </template>
                      <template v-slot:item.total_area="{ item }">
                        {{ item.total_area?.toFixed(2) || 0 }} м²
                      </template>
                      <template v-slot:item.avg_area="{ item }">
                        {{ item.avg_area?.toFixed(2) || 0 }} м²
                      </template>
                    </v-data-table>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Распределение по этажам -->
              <v-col cols="12" md="6">
                <v-card variant="outlined">
                  <v-card-title>Распределение по этажам</v-card-title>
                  <v-card-text>
                    <v-list>
                      <v-list-item
                        v-for="item in statistics.floor_distribution"
                        :key="item.floor"
                      >
                        <v-list-item-title>
                          {{ item.floor }} этаж
                        </v-list-item-title>
                        <template v-slot:append>
                          <v-chip color="primary">{{ item.count }} квартир</v-chip>
                        </template>
                      </v-list-item>
                    </v-list>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Распределение по комнатам -->
              <v-col cols="12" md="6">
                <v-card variant="outlined">
                  <v-card-title>Распределение по комнатам</v-card-title>
                  <v-card-text>
                    <v-list>
                      <v-list-item
                        v-for="item in statistics.rooms_distribution"
                        :key="item.rooms"
                      >
                        <v-list-item-title>
                          {{ item.rooms }} {{ pluralizeRooms(item.rooms) }}
                        </v-list-item-title>
                        <template v-slot:append>
                          <v-chip color="primary">{{ item.count }} квартир</v-chip>
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
import { buildingsService } from '@/services/buildingsService'
import StatisticsCard from '@/components/StatisticsCard.vue'

export default {
  name: 'BuildingsStatistics',
  components: {
    StatisticsCard,
  },
  data() {
    return {
      statistics: null,
      loading: false,
      buildingHeaders: [
        { title: 'Адрес', key: 'address' },
        { title: 'Этажей', key: 'total_floors' },
        { title: 'Квартир', key: 'apartment_count' },
        { title: 'Общая площадь', key: 'total_area' },
        { title: 'Средняя площадь', key: 'avg_area' },
        { title: 'Заселено', key: 'occupied_count' },
        { title: 'Свободно', key: 'vacant_count' },
      ],
    }
  },
  async mounted() {
    await this.loadStatistics()
  },
  methods: {
    async loadStatistics() {
      this.loading = true
      try {
        this.statistics = await buildingsService.getStatistics()
      } catch (error) {
        console.error('Error loading statistics:', error)
      } finally {
        this.loading = false
      }
    },
    pluralizeRooms(count) {
      if (count === 1) return 'комната'
      if (count >= 2 && count <= 4) return 'комнаты'
      return 'комнат'
    },
  },
}
</script>

