<template>
  <div>
    <!-- Заголовок и навигация по отчетам -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card color="teal-darken-3" dark>
          <v-card-title class="text-h4">
            <v-icon icon="mdi-chart-box" size="large" class="mr-3"></v-icon>
            Отчеты и аналитика
          </v-card-title>
          <v-card-subtitle class="text-h6">
            Анализ работы автопарка и статистика
          </v-card-subtitle>
          <v-card-actions>
            <v-btn
              v-for="tab in tabs"
              :key="tab.value"
              :color="activeTab === tab.value ? 'white' : 'grey-lighten-1'"
              :variant="activeTab === tab.value ? 'outlined' : 'text'"
              @click="activeTab = tab.value"
              class="mr-2"
            >
              <v-icon :icon="tab.icon" class="mr-2"></v-icon>
              {{ tab.title }}
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
              color="white"
              variant="text"
              @click="refreshReport"
              :loading="loading"
            >
              <v-icon icon="mdi-refresh" class="mr-2"></v-icon>
              Обновить
            </v-btn>
            <v-btn
              color="white"
              variant="outlined"
              @click="exportReport"
              :disabled="!hasReportData"
            >
              <v-icon icon="mdi-download" class="mr-2"></v-icon>
              Экспорт
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Статистика сверху -->
    <v-row class="mb-6">
      <v-col cols="12" sm="6" md="3">
        <v-card elevation="2">
          <v-card-text class="text-center py-4">
            <v-icon icon="mdi-bus" size="x-large" color="blue" class="mb-2"></v-icon>
            <div class="text-h4">{{ stats.totalBuses || 0 }}</div>
            <div class="text-subtitle-1">Всего автобусов</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card elevation="2">
          <v-card-text class="text-center py-4">
            <v-icon icon="mdi-account-group" size="x-large" color="green" class="mb-2"></v-icon>
            <div class="text-h4">{{ stats.totalDrivers || 0 }}</div>
            <div class="text-subtitle-1">Всего водителей</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card elevation="2">
          <v-card-text class="text-center py-4">
            <v-icon icon="mdi-map-marker-path" size="x-large" color="orange" class="mb-2"></v-icon>
            <div class="text-h4">{{ stats.totalRoutes || 0 }}</div>
            <div class="text-subtitle-1">Всего маршрутов</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card elevation="2">
          <v-card-text class="text-center py-4">
            <v-icon icon="mdi-garage" size="x-large" color="purple" class="mb-2"></v-icon>
            <div class="text-h4">{{ stats.totalDepots || 0 }}</div>
            <div class="text-subtitle-1">Всего депо</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>


    <!-- Контент по табам -->
    <!-- Отчет по депо -->
    <div v-if="activeTab === 'depots'">
      <v-row class="mb-4">
        <v-col cols="12">
          <v-card elevation="2">
            <v-card-title class="text-h6">
              <v-icon icon="mdi-garage" class="mr-2"></v-icon>
              Отчет по автопаркам (депо)
            </v-card-title>
            <v-card-text>
              <v-data-table
                :headers="depotHeaders"
                :items="depotReport"
                :loading="loadingDepots"
                class="elevation-1"
              >
                <template v-slot:item.name="{ item }">
                  <div class="d-flex align-center">
                    <v-avatar :color="getDepotColor(item.occupancy_percentage)" size="36" class="mr-3">
                      <v-icon icon="mdi-garage" color="white"></v-icon>
                    </v-avatar>
                    <div>
                      <strong>{{ item.name }}</strong>
                      <div class="text-caption text-medium-emphasis">
                        {{ item.address }}
                      </div>
                    </div>
                  </div>
                </template>

                <template v-slot:item.capacity="{ item }">
                  <div class="d-flex align-center">
                    <v-icon icon="mdi-bus-multiple" color="blue" class="mr-2"></v-icon>
                    <div>
                      <div class="text-subtitle-1 font-weight-bold">{{ item.capacity }}</div>
                      <div class="text-caption text-medium-emphasis">мест</div>
                    </div>
                  </div>
                </template>

                <template v-slot:item.occupancy="{ item }">
                  <div>
                    <div class="d-flex justify-space-between mb-1">
                      <span>{{ item.occupancy }} / {{ item.capacity }}</span>
                      <span>{{ item.occupancy_percentage.toFixed(1) }}%</span>
                    </div>
                    <v-progress-linear
                      :model-value="item.occupancy_percentage"
                      :color="getOccupancyColor(item.occupancy_percentage)"
                      height="8"
                      rounded
                    ></v-progress-linear>
                  </div>
                </template>

                <template v-slot:item.active_buses="{ item }">
                  <v-chip :color="item.active_buses > 0 ? 'green' : 'grey'" variant="flat">
                    {{ item.active_buses }}
                  </v-chip>
                </template>

                <template v-slot:no-data>
                  <v-alert type="info" variant="tonal" class="ma-4">
                    Нет данных по автопаркам. Проверьте подключение к API.
                  </v-alert>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- График загруженности депо -->
      <v-row v-if="depotReport.length > 0">
        <v-col cols="12">
          <v-card elevation="2">
            <v-card-title class="text-h6">
              <v-icon icon="mdi-chart-bar" class="mr-2"></v-icon>
              Загруженность автопарков
            </v-card-title>
            <v-card-text>
              <div class="d-flex flex-column" style="gap: 16px;">
                <div
                  v-for="depot in depotReport"
                  :key="depot.id"
                  class="d-flex align-center"
                >
                  <div style="width: 150px; min-width: 150px;">
                    <strong>{{ depot.name }}</strong>
                    <div class="text-caption">{{ depot.active_buses }} активных</div>
                  </div>
                  <v-progress-linear
                    :model-value="depot.occupancy_percentage"
                    :color="getOccupancyColor(depot.occupancy_percentage)"
                    height="20"
                    rounded
                    class="flex-grow-1"
                  >
                    <template v-slot:default="{ value }">
                      <div class="text-caption white--text font-weight-bold">
                        {{ Math.round(value) }}% ({{ depot.occupancy }}/{{ depot.capacity }})
                      </div>
                    </template>
                  </v-progress-linear>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Отчет по типам автобусов -->
    <div v-if="activeTab === 'bus-types'">
      <v-row class="mb-4">
        <v-col cols="12">
          <v-card elevation="2">
            <v-card-title class="text-h6">
              <v-icon icon="mdi-bus-double-decker" class="mr-2"></v-icon>
              Отчет по типам автобусов
            </v-card-title>
            <v-card-text>
              <v-data-table
                :headers="busTypeHeaders"
                :items="busTypeReport"
                :loading="loadingBusTypes"
                class="elevation-1"
              >
                <template v-slot:item.bus_type="{ item }">
                  <div class="d-flex align-center">
                    <v-avatar :color="getTypeColor(item.bus_type)" size="36" class="mr-3">
                      <v-icon icon="mdi-bus" color="white"></v-icon>
                    </v-avatar>
                    <div>
                      <strong>{{ item.bus_type }}</strong>
                      <div class="text-caption text-medium-emphasis">
                        {{ item.bus_count }} автобусов
                      </div>
                    </div>
                  </div>
                </template>

                <template v-slot:item.bus_count="{ item }">
                  <v-chip :color="getCountColor(item.bus_count)" variant="flat">
                    {{ item.bus_count }}
                  </v-chip>
                </template>

                <template v-slot:item.total_route_duration="{ item }">
                  <div>
                    <div class="text-subtitle-1">
                      {{ formatDuration(item.total_route_duration) }}
                    </div>
                    <div class="text-caption text-medium-emphasis">
                      общая протяженность
                    </div>
                  </div>
                </template>

                <template v-slot:item.drivers_avg_experience="{ item }">
                  <div>
                    <div class="text-subtitle-1">
                      {{ item.drivers_avg_experience?.toFixed(1) || '0.0' }} лет
                    </div>
                    <div class="text-caption text-medium-emphasis">
                      средний опыт
                    </div>
                  </div>
                </template>

                <template v-slot:item.routes="{ item }">
                  <div>
                    <div class="text-subtitle-1">{{ item.routes?.length || 0 }}</div>
                    <div class="text-caption text-medium-emphasis">
                      маршрутов
                    </div>
                  </div>
                </template>

                <template v-slot:item.drivers="{ item }">
                  <div>
                    <div class="text-subtitle-1">{{ item.drivers?.length || 0 }}</div>
                    <div class="text-caption text-medium-emphasis">
                      водителей
                    </div>
                  </div>
                </template>

                <template v-slot:no-data>
                  <v-alert type="info" variant="tonal" class="ma-4">
                    Нет данных по типам автобусов. Проверьте подключение к API.
                  </v-alert>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Распределение автобусов по типам -->
      <v-row v-if="busTypeReport.length > 0">
        <v-col cols="12" md="6">
          <v-card elevation="2">
            <v-card-title class="text-h6">
              <v-icon icon="mdi-chart-pie" class="mr-2"></v-icon>
              Распределение автобусов по типам
            </v-card-title>
            <v-card-text>
              <div class="d-flex flex-wrap justify-center gap-3 mb-4">
                <div
                  v-for="type in busTypeReport"
                  :key="type.bus_type"
                  class="text-center"
                  style="min-width: 120px;"
                >
                  <v-progress-circular
                    :model-value="(type.bus_count / totalBusCount) * 100"
                    :color="getTypeColor(type.bus_type)"
                    size="80"
                    width="8"
                  >
                    <strong>{{ type.bus_count }}</strong>
                  </v-progress-circular>
                  <div class="mt-2">
                    <div class="text-subtitle-2">{{ type.bus_type }}</div>
                    <div class="text-caption text-medium-emphasis">
                      {{ ((type.bus_count / totalBusCount) * 100).toFixed(1) }}%
                    </div>
                  </div>
                </div>
              </div>

              <div class="mt-4">
                <div class="d-flex flex-wrap justify-center gap-2">
                  <v-chip
                    v-for="type in busTypeReport"
                    :key="type.bus_type"
                    :color="getTypeColor(type.bus_type)"
                    size="small"
                  >
                    {{ type.bus_type }}: {{ type.bus_count }}
                  </v-chip>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="6">
          <v-card elevation="2">
            <v-card-title class="text-h6">
              <v-icon icon="mdi-account-clock" class="mr-2"></v-icon>
              Средний опыт водителей по типам
            </v-card-title>
            <v-card-text>
              <div class="d-flex flex-column" style="gap: 16px;">
                <div
                  v-for="type in busTypeReport"
                  :key="type.bus_type"
                  class="d-flex align-center"
                >
                  <div style="width: 150px; min-width: 150px;">
                    <strong>{{ type.bus_type }}</strong>
                    <div class="text-caption">{{ type.drivers?.length || 0 }} водителей</div>
                  </div>
                  <v-progress-linear
                    :model-value="(type.drivers_avg_experience || 0) * 10"
                    :color="getTypeColor(type.bus_type)"
                    height="20"
                    rounded
                    class="flex-grow-1"
                  >
                    <template v-slot:default="{ value }">
                      <div class="text-caption white--text font-weight-bold">
                        {{ type.drivers_avg_experience?.toFixed(1) || '0.0' }} лет
                      </div>
                    </template>
                  </v-progress-linear>
                </div>
              </div>

              <div class="mt-4">
                <v-alert type="info" variant="tonal">
                  <strong>Примечание:</strong> Максимальная шкала - 10 лет опыта
                </v-alert>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Отчет по классам водителей -->
    <div v-if="activeTab === 'driver-classes'">
      <v-row class="mb-4">
        <v-col cols="12">
          <v-card elevation="2">
            <v-card-title class="text-h6">
              <v-icon icon="mdi-license" class="mr-2"></v-icon>
              Распределение водителей по классам
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col
                  v-for="stat in driverClassesReport"
                  :key="stat.driver_class__name"
                  cols="12" sm="6" md="4" lg="3"
                >
                  <v-card :color="getClassColor(stat.driver_class__name)" dark>
                    <v-card-text class="text-center py-6">
                      <div class="text-h2">{{ stat.total || 0 }}</div>
                      <div class="text-h6">{{ stat.driver_class__name || 'Без класса' }}</div>
                      <div class="text-caption mt-2">водителей</div>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Детальная статистика по классам -->
      <v-row v-if="driverClassesReport.length > 0">
        <v-col cols="12">
          <v-card elevation="2">
            <v-card-title class="text-h6">
              <v-icon icon="mdi-chart-bar" class="mr-2"></v-icon>
              Детальная статистика по классам
            </v-card-title>
            <v-card-text>
              <v-data-table
                :headers="driverClassHeaders"
                :items="driverClassesWithDetails"
                class="elevation-1"
              >
                <template v-slot:item.class="{ item }">
                  <div class="d-flex align-center">
                    <v-avatar :color="getClassColor(item.class)" size="36" class="mr-3">
                      <v-icon icon="mdi-license" color="white"></v-icon>
                    </v-avatar>
                    <div>
                      <strong>{{ item.class }}</strong>
                      <div class="text-caption text-medium-emphasis">
                        {{ item.drivers }} водителей
                      </div>
                    </div>
                  </div>
                </template>

                <template v-slot:item.percentage="{ item }">
                  <div>
                    <div class="d-flex justify-space-between mb-1">
                      <span>{{ item.drivers }} из {{ stats.totalDrivers }}</span>
                      <span>{{ item.percentage.toFixed(1) }}%</span>
                    </div>
                    <v-progress-linear
                      :model-value="item.percentage"
                      :color="getClassColor(item.class)"
                      height="8"
                      rounded
                    ></v-progress-linear>
                  </div>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Общая статистика -->
    <div v-if="activeTab === 'overview'">
      <v-row>
        <!-- Распределение автобусов по активности -->
        <v-col cols="12" md="6">
          <v-card elevation="2" class="h-100">
            <v-card-title class="text-h6">
              <v-icon icon="mdi-bus-clock" class="mr-2"></v-icon>
              Статус автобусов
            </v-card-title>
            <v-card-text class="text-center">
              <div class="d-flex justify-center align-center mb-6">
                <div class="position-relative" style="width: 200px; height: 200px;">
                  <!-- Круговая диаграмма на Vuetify компонентах -->
                  <svg width="200" height="200" viewBox="0 0 200 200">
                    <!-- Активные автобусы -->
                    <circle
                      cx="100"
                      cy="100"
                      r="80"
                      fill="none"
                      :stroke="activePercentage > 0 ? '#4CAF50' : 'transparent'"
                      stroke-width="40"
                      :stroke-dasharray="`${activePercentage * 2.51} ${(100 - activePercentage) * 2.51}`"
                      stroke-dashoffset="0"
                      transform="rotate(-90 100 100)"
                    />
                    <!-- Неактивные автобусы -->
                    <circle
                      cx="100"
                      cy="100"
                      r="80"
                      fill="none"
                      :stroke="inactivePercentage > 0 ? '#F44336' : 'transparent'"
                      stroke-width="40"
                      :stroke-dasharray="`${inactivePercentage * 2.51} ${(100 - inactivePercentage) * 2.51}`"
                      :stroke-dashoffset="`${-activePercentage * 2.51}`"
                      transform="rotate(-90 100 100)"
                    />
                  </svg>

                  <div class="position-absolute top-50 start-50 translate-middle text-center">
                    <div class="text-h4">{{ stats.totalBuses || 0 }}</div>
                    <div class="text-caption">всего</div>
                  </div>
                </div>
              </div>

              <div class="mt-4">
                <v-row>
                  <v-col cols="6" class="text-center">
                    <v-chip color="green" variant="flat" class="mb-2">
                      <v-icon icon="mdi-check-circle" class="mr-1"></v-icon>
                      {{ stats.activeBuses || 0 }}
                    </v-chip>
                    <div class="text-subtitle-2">Активных</div>
                    <div class="text-caption text-medium-emphasis">
                      {{ activePercentage.toFixed(1) }}%
                    </div>
                  </v-col>
                  <v-col cols="6" class="text-center">
                    <v-chip color="red" variant="flat" class="mb-2">
                      <v-icon icon="mdi-close-circle" class="mr-1"></v-icon>
                      {{ stats.inactiveBuses || 0 }}
                    </v-chip>
                    <div class="text-subtitle-2">Неактивных</div>
                    <div class="text-caption text-medium-emphasis">
                      {{ inactivePercentage.toFixed(1) }}%
                    </div>
                  </v-col>
                </v-row>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Распределение по депо -->
        <v-col cols="12" md="6">
          <v-card elevation="2" class="h-100">
            <v-card-title class="text-h6">
              <v-icon icon="mdi-garage-variant" class="mr-2"></v-icon>
              Распределение по депо
            </v-card-title>
            <v-card-text>
              <v-list>
                <v-list-item
                  v-for="depot in depotReport.slice(0, 5)"
                  :key="depot.id"
                >
                  <template v-slot:prepend>
                    <v-avatar :color="getOccupancyColor(depot.occupancy_percentage)" size="36">
                      <v-icon icon="mdi-garage" color="white"></v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title>{{ depot.name }}</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ depot.active_buses }} автобусов • {{ depot.occupancy_percentage.toFixed(1) }}%
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
              <div v-if="depotReport.length > 5" class="text-center mt-2">
                <v-chip color="blue" variant="tonal">
                  +{{ depotReport.length - 5 }} еще
                </v-chip>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Сводная информация -->
      <v-row class="mt-4">
        <v-col cols="12">
          <v-card elevation="2">
            <v-card-title class="text-h6">
              <v-icon icon="mdi-information" class="mr-2"></v-icon>
              Сводная информация
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12" md="4">
                  <v-list density="compact">
                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon icon="mdi-bus-multiple"></v-icon>
                      </template>
                      <v-list-item-title>Всего автобусов</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">{{ stats.totalBuses || 0 }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon icon="mdi-bus-clock"></v-icon>
                      </template>
                      <v-list-item-title>На маршрутах</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">{{ stats.activeBuses || 0 }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon icon="mdi-account-group"></v-icon>
                      </template>
                      <v-list-item-title>Всего водителей</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">{{ stats.totalDrivers || 0 }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-col>

                <v-col cols="12" md="4">
                  <v-list density="compact">
                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon icon="mdi-map-marker-path"></v-icon>
                      </template>
                      <v-list-item-title>Маршрутов</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">{{ stats.totalRoutes || 0 }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon icon="mdi-clock-outline"></v-icon>
                      </template>
                      <v-list-item-title>Общая протяженность</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">{{ formatDuration(stats.totalDuration) }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon icon="mdi-calendar-clock"></v-icon>
                      </template>
                      <v-list-item-title>Активных смен</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">{{ stats.totalWorkShifts || 0 }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-col>

                <v-col cols="12" md="4">
                  <v-list density="compact">
                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon icon="mdi-garage"></v-icon>
                      </template>
                      <v-list-item-title>Депо</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">{{ stats.totalDepots || 0 }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon icon="mdi-bus-double-decker"></v-icon>
                      </template>
                      <v-list-item-title>Типов автобусов</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">{{ stats.totalBusTypes || 0 }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon icon="mdi-license"></v-icon>
                      </template>
                      <v-list-item-title>Классов водителей</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">{{ stats.totalDriverClasses || 0 }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Уведомления -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
      {{ snackbar.message }}
      <template v-slot:actions>
        <v-btn icon="mdi-close" @click="snackbar.show = false"></v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { ref, computed, onMounted, reactive } from 'vue'
import apiClient from '@/api/axios'

export default {
  setup() {
    // Состояние
    const activeTab = ref('overview')
    const loading = ref(false)
    const loadingDepots = ref(false)
    const loadingBusTypes = ref(false)
    const loadingDriverClasses = ref(false)
    const dateMenu = ref(false)
    const dateRange = ref([new Date().toISOString().split('T')[0], new Date().toISOString().split('T')[0]])

    // Данные
    const depotReport = ref([])
    const busTypeReport = ref([])
    const driverClassesReport = ref([])
    const depots = ref([])
    const busTypes = ref([])
    const stats = reactive({
      totalBuses: 0,
      activeBuses: 0,
      inactiveBuses: 0,
      totalDrivers: 0,
      totalRoutes: 0,
      totalDuration: 0,
      totalDepots: 0,
      totalBusTypes: 0,
      totalDriverClasses: 0,
      totalWorkShifts: 0
    })

    // Фильтры
    const filters = reactive({
      depot_id: null,
      bus_type_id: null,
      start_date: null,
      end_date: null
    })

    // Уведомления
    const snackbar = reactive({
      show: false,
      message: '',
      color: 'success'
    })

    // Вкладки
    const tabs = ref([
      { title: 'Обзор', value: 'overview', icon: 'mdi-home-analytics' },
      { title: 'Автопарки', value: 'depots', icon: 'mdi-garage' },
      { title: 'Типы автобусов', value: 'bus-types', icon: 'mdi-bus-double-decker' },
      { title: 'Классы водителей', value: 'driver-classes', icon: 'mdi-license' }
    ])

    // Заголовки таблиц
    const depotHeaders = ref([
      { title: 'Депо', key: 'name', sortable: false },
      { title: 'Вместимость', key: 'capacity', sortable: false, width: '120px' },
      { title: 'Загруженность', key: 'occupancy', sortable: false, width: '200px' },
      { title: 'Активных автобусов', key: 'active_buses', sortable: false, width: '140px', align: 'center' }
    ])

    const busTypeHeaders = ref([
      { title: 'Тип автобуса', key: 'bus_type', sortable: false },
      { title: 'Количество', key: 'bus_count', sortable: false, width: '100px', align: 'center' },
      { title: 'Маршруты', key: 'routes', sortable: false, width: '100px', align: 'center' },
      { title: 'Водители', key: 'drivers', sortable: false, width: '100px', align: 'center' },
      { title: 'Протяженность', key: 'total_route_duration', sortable: false, width: '140px' },
      { title: 'Средний опыт', key: 'drivers_avg_experience', sortable: false, width: '120px' }
    ])

    const driverClassHeaders = ref([
      { title: 'Класс', key: 'class', sortable: false },
      { title: 'Водителей', key: 'drivers', sortable: false, width: '100px', align: 'center' },
      { title: 'Доля от общего числа', key: 'percentage', sortable: false, width: '200px' }
    ])

    // Вычисляемые свойства
    const dateRangeText = computed(() => {
      if (!dateRange.value || dateRange.value.length < 2) return 'Выберите период'
      const start = formatDate(dateRange.value[0])
      const end = formatDate(dateRange.value[1])
      return `${start} - ${end}`
    })

    const hasReportData = computed(() => {
      return depotReport.value.length > 0 ||
             busTypeReport.value.length > 0 ||
             driverClassesReport.value.length > 0
    })

    const driverClassesWithDetails = computed(() => {
      const total = stats.totalDrivers || 1
      return driverClassesReport.value.map(stat => ({
        class: stat.driver_class__name || 'Без класса',
        drivers: stat.total || 0,
        percentage: (stat.total / total) * 100
      }))
    })

    const totalBusCount = computed(() => {
      return busTypeReport.value.reduce((sum, type) => sum + (type.bus_count || 0), 0)
    })

    const activePercentage = computed(() => {
      if (!stats.totalBuses) return 0
      return (stats.activeBuses / stats.totalBuses) * 100
    })

    const inactivePercentage = computed(() => {
      if (!stats.totalBuses) return 0
      return (stats.inactiveBuses / stats.totalBuses) * 100
    })

    // Вспомогательные функции
    const formatDate = (dateStr) => {
      if (!dateStr) return ''
      return new Date(dateStr).toLocaleDateString('ru-RU')
    }

    const formatDuration = (minutes) => {
      if (!minutes) return '0 мин'
      const hours = Math.floor(minutes / 60)
      const mins = minutes % 60

      if (hours === 0) return `${mins} мин`
      if (mins === 0) return `${hours} ч`
      return `${hours} ч ${mins} мин`
    }

    const getDepotColor = (percentage) => {
      if (percentage < 30) return 'green'
      if (percentage < 60) return 'blue'
      if (percentage < 80) return 'orange'
      return 'red'
    }

    const getOccupancyColor = (percentage) => {
      if (percentage < 30) return 'green'
      if (percentage < 60) return 'blue'
      if (percentage < 80) return 'orange'
      return 'red'
    }

    const getTypeColor = (typeName) => {
      const colors = {
        'Городской': 'blue',
        'Пригородный': 'green',
        'Туристический': 'orange',
        'Экспресс': 'purple',
        'Школьный': 'yellow',
        'default': 'teal'
      }
      return colors[typeName] || colors.default
    }

    const getCountColor = (count) => {
      if (!count || count === 0) return 'grey'
      if (count <= 3) return 'orange'
      if (count <= 10) return 'blue'
      return 'green'
    }

    const getClassColor = (className) => {
      const colors = {
        'Первый': 'green-darken-2',
        'Второй': 'blue-darken-2',
        'Третий': 'orange-darken-2',
        'Четвертый': 'red-darken-2',
        'default': 'indigo-darken-2'
      }
      return colors[className] || colors.default
    }

    const applyDateFilter = () => {
      dateMenu.value = false
      if (dateRange.value && dateRange.value.length === 2) {
        filters.start_date = dateRange.value[0]
        filters.end_date = dateRange.value[1]
      }
      refreshReport()
    }

    // API функции
    const fetchAllStats = async () => {
      try {
        const [
          busesRes,
          driversRes,
          routesRes,
          depotsRes,
          busTypesRes,
          driverClassesRes,
          workShiftsRes,
          totalDurationRes
        ] = await Promise.all([
          apiClient.get('buses/'),
          apiClient.get('drivers/'),
          apiClient.get('routes/'),
          apiClient.get('depots/'),
          apiClient.get('bus-types/'),
          apiClient.get('driverclasses/'),
          apiClient.get('workshifts/'),
          apiClient.get('routes/total_duration/').catch(() => ({ data: { total_duration_minutes: 0 } }))
        ])

        const buses = busesRes.data
        stats.totalBuses = buses.length
        stats.activeBuses = buses.filter(b => b.is_active).length
        stats.inactiveBuses = stats.totalBuses - stats.activeBuses
        stats.totalDrivers = driversRes.data.length
        stats.totalRoutes = routesRes.data.length
        stats.totalDepots = depotsRes.data.length
        stats.totalBusTypes = busTypesRes.data.length
        stats.totalDriverClasses = driverClassesRes.data.length
        stats.totalWorkShifts = workShiftsRes.data.length
        stats.totalDuration = totalDurationRes.data.total_duration_minutes ||
          routesRes.data.reduce((sum, route) => sum + (route.duration_minutes || 0), 0)
      } catch (error) {
        console.error('Ошибка загрузки статистики:', error)
      }
    }

    const fetchDepotReport = async () => {
      loadingDepots.value = true
      try {
        const response = await apiClient.get('depots/summary/')
        depotReport.value = response.data
        depots.value = response.data.map(depot => ({
          id: depot.id,
          name: depot.name,
          address: depot.address
        }))
      } catch (error) {
        console.error('Ошибка загрузки отчета по депо:', error)
        showSnackbar('Ошибка загрузки отчета по автопаркам', 'error')
      } finally {
        loadingDepots.value = false
      }
    }

    const fetchBusTypeReport = async () => {
      loadingBusTypes.value = true
      try {
        const response = await apiClient.get('bus-types/report/')
        busTypeReport.value = response.data
        busTypes.value = response.data.map(type => ({
          id: type.id,
          name: type.bus_type
        }))
      } catch (error) {
        console.error('Ошибка загрузки отчета по типам автобусов:', error)
        showSnackbar('Ошибка загрузки отчета по типам автобусов', 'error')
      } finally {
        loadingBusTypes.value = false
      }
    }

    const fetchDriverClassesReport = async () => {
      loadingDriverClasses.value = true
      try {
        const response = await apiClient.get('driverclasses/statistics/')
        driverClassesReport.value = response.data
      } catch (error) {
        console.error('Ошибка загрузки отчета по классам водителей:', error)
        showSnackbar('Ошибка загрузки отчета по классам водителей', 'error')
      } finally {
        loadingDriverClasses.value = false
      }
    }

    const refreshReport = async () => {
      loading.value = true
      try {
        await Promise.all([
          fetchAllStats(),
          fetchDepotReport(),
          fetchBusTypeReport(),
          fetchDriverClassesReport()
        ])
      } finally {
        loading.value = false
      }
    }

    const exportReport = () => {
      // Простая реализация экспорта в JSON
      const data = {
        timestamp: new Date().toISOString(),
        period: dateRangeText.value,
        stats: stats,
        depotReport: depotReport.value,
        busTypeReport: busTypeReport.value,
        driverClassesReport: driverClassesReport.value
      }

      const dataStr = JSON.stringify(data, null, 2)
      const dataBlob = new Blob([dataStr], { type: 'application/json' })
      const url = URL.createObjectURL(dataBlob)
      const link = document.createElement('a')
      link.href = url
      link.download = `bus-report-${new Date().toISOString().split('T')[0]}.json`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)

      showSnackbar('Отчет экспортирован в JSON', 'success')
    }

    const showSnackbar = (message, color = 'success') => {
      snackbar.message = message
      snackbar.color = color
      snackbar.show = true
    }

    // Инициализация
    onMounted(async () => {
      await refreshReport()
    })

    return {
      // Состояние
      activeTab,
      loading,
      loadingDepots,
      loadingBusTypes,
      loadingDriverClasses,
      dateMenu,
      dateRange,
      filters,
      snackbar,
      tabs,
      stats,
      depotReport,
      busTypeReport,
      driverClassesReport,
      depots,
      busTypes,
      hasReportData,
      driverClassesWithDetails,
      totalBusCount,
      activePercentage,
      inactivePercentage,

      // Вычисляемые свойства
      dateRangeText,

      // Заголовки таблиц
      depotHeaders,
      busTypeHeaders,
      driverClassHeaders,

      // Методы
      refreshReport,
      exportReport,
      applyDateFilter,

      // Вспомогательные методы
      formatDate,
      formatDuration,
      getDepotColor,
      getOccupancyColor,
      getTypeColor,
      getCountColor,
      getClassColor,
      showSnackbar
    }
  }
}
</script>

<style scoped>


.h-100 {
  height: 100%;
}

.position-relative {
  position: relative;
}

.position-absolute {
  position: absolute;
}

.top-50 {
  top: 50%;
}

.start-50 {
  left: 50%;
}

.translate-middle {
  transform: translate(-50%, -50%);
}






/* Стили для круговой диаграммы */
svg circle {
  transition: stroke-dasharray 0.5s ease;
}

/* Адаптивные стили */
@media (max-width: 960px) {

  .text-h4 {
    font-size: 1.8rem;
  }

  .text-h6 {
    font-size: 1.2rem;
  }
}

@media (max-width: 600px) {


  .d-flex.flex-wrap.justify-center.gap-3 .text-center {
    min-width: 100px;
  }
}
</style>
