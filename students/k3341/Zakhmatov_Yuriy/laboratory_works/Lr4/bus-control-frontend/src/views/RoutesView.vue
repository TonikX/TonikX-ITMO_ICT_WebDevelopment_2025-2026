<template>
  <div>
    <!-- Заголовок и статистика -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card color="orange-darken-3" dark>
          <v-card-title class="text-h4">
            <v-icon icon="mdi-map-marker-path" size="large" class="mr-3"></v-icon>
            Маршруты
          </v-card-title>
          <v-card-subtitle class="text-h6">
            Управление маршрутами автобусов
          </v-card-subtitle>
          <v-card-actions>
            <v-btn color="white" variant="outlined" @click="openCreateDialog">
              <v-icon icon="mdi-plus-circle" class="mr-2"></v-icon>
              Добавить маршрут
            </v-btn>
            <v-btn color="white" variant="text" @click="fetchRoutes">
              <v-icon icon="mdi-refresh" class="mr-2"></v-icon>
              Обновить
            </v-btn>
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              label="Поиск маршрутов..."
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              density="compact"
              clearable
              hide-details
              style="max-width: 300px;"
              class="bg-white rounded"
            ></v-text-field>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Общая протяженность -->
    <v-row v-if="totalDuration !== null" class="mb-4">
      <v-col cols="12">
        <v-card elevation="2">
          <v-card-text class="text-center py-4">
            <div class="d-flex align-center justify-center">
              <v-icon icon="mdi-ruler" size="large" color="orange" class="mr-3"></v-icon>
              <div>
                <div class="text-h5">Общая протяженность всех маршрутов</div>
                <div class="text-h2 text-orange">{{ formatDuration(totalDuration) }}</div>
                <div class="text-caption text-medium-emphasis">
                  {{ totalDuration }} минут / {{ (totalDuration / 60).toFixed(1) }} часов
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Таблица маршрутов -->
    <v-card elevation="2">
      <v-data-table
        :headers="headers"
        :items="filteredRoutes"
        :loading="loading"
        :search="search"
        class="elevation-1"
      >
        <!-- Заголовок таблицы -->
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Список маршрутов</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>
            <v-chip color="orange" variant="tonal">
              Всего: {{ routes.length }}
            </v-chip>
          </v-toolbar>
        </template>

        <!-- Иконка загрузки -->
        <template v-slot:loading>
          <v-skeleton-loader type="table-row@10"></v-skeleton-loader>
        </template>

        <!-- Колонка ID -->
        <template v-slot:item.id="{ item }">
          <v-chip color="grey" variant="outlined" size="small">
            #{{ item.id }}
          </v-chip>
        </template>

        <!-- Колонка номера маршрута -->
        <template v-slot:item.number="{ item }">
          <div class="d-flex align-center">
            <v-avatar :color="getRouteColor(item.number)" size="36" class="mr-3">
              <span class="white--text text-h6">{{ getRouteIcon(item.number) }}</span>
            </v-avatar>
            <div>
              <strong class="text-h6">{{ item.number }}</strong>
              <div class="text-caption text-medium-emphasis">
                ID: {{ item.id }}
              </div>
            </div>
          </div>
        </template>

        <!-- Колонка маршрута -->
        <template v-slot:item.route_path="{ item }">
          <div>
            <div class="text-subtitle-1 font-weight-bold">{{ item.start_point }} → {{ item.end_point }}</div>
            <div class="text-caption text-medium-emphasis">
              {{ formatTime(item.start_time) }} - {{ formatTime(item.end_time) }}
            </div>
          </div>
        </template>

        <!-- Колонка времени -->
        <template v-slot:item.schedule="{ item }">
          <div>
            <div class="d-flex align-center">
              <v-icon icon="mdi-clock-outline" size="small" class="mr-1"></v-icon>
              <span>{{ formatTime(item.start_time) }}</span>
            </div>
            <div class="d-flex align-center">
              <v-icon icon="mdi-clock-end" size="small" class="mr-1"></v-icon>
              <span>{{ formatTime(item.end_time) }}</span>
            </div>
          </div>
        </template>

        <!-- Колонка интервала -->
        <template v-slot:item.interval_minutes="{ item }">
          <v-chip :color="getIntervalColor(item.interval_minutes)" variant="flat" size="small">
            {{ item.interval_minutes }} мин
          </v-chip>
        </template>

        <!-- Колонка длительности -->
        <template v-slot:item.duration_minutes="{ item }">
          <v-chip :color="getDurationColor(item.duration_minutes)" variant="outlined" size="small">
            {{ formatDurationShort(item.duration_minutes) }}
          </v-chip>
        </template>

        <!-- Колонка действий -->
        <template v-slot:item.actions="{ item }">
          <div class="d-flex" style="gap: 8px;">
            <v-btn
              icon="mdi-eye"
              size="small"
              color="info"
              variant="text"
              @click="viewRoute(item)"
              title="Просмотр"
            ></v-btn>
            <v-btn
              icon="mdi-calendar-clock"
              size="small"
              color="purple"
              variant="text"
              @click="showSchedule(item)"
              title="Расписание"
            ></v-btn>
            <v-btn
              icon="mdi-account-group"
              size="small"
              color="blue"
              variant="text"
              @click="showDriversSchedule(item)"
              title="Водители"
            ></v-btn>
            <v-btn
              icon="mdi-pencil"
              size="small"
              color="warning"
              variant="text"
              @click="editRoute(item)"
              title="Редактировать"
            ></v-btn>
            <v-btn
              icon="mdi-delete"
              size="small"
              color="error"
              variant="text"
              @click="deleteRoute(item)"
              title="Удалить"
            ></v-btn>
          </div>
        </template>

        <!-- Пустая таблица -->
        <template v-slot:no-data>
          <v-alert type="info" variant="tonal" class="ma-4">
            Нет данных о маршрутах. Нажмите "Добавить маршрут", чтобы создать первый.
          </v-alert>
        </template>
      </v-data-table>
    </v-card>

    <!-- Диалог создания/редактирования -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title class="text-h5">
          <v-icon :icon="editMode ? 'mdi-pencil' : 'mdi-plus-circle'" class="mr-2"></v-icon>
          {{ editMode ? 'Редактирование маршрута' : 'Новый маршрут' }}
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="localForm.number"
                  label="Номер маршрута*"
                  required
                  variant="outlined"
                  :rules="[v => !!v || 'Номер маршрута обязателен']"
                  hint="Пример: 101, 22А, Э40"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="localForm.start_point"
                  label="Начальная остановка*"
                  required
                  variant="outlined"
                  :rules="[v => !!v || 'Начальная остановка обязательна']"
                  hint="Пример: Вокзал, Метро Пушкинская"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="localForm.end_point"
                  label="Конечная остановка*"
                  required
                  variant="outlined"
                  :rules="[v => !!v || 'Конечная остановка обязательна']"
                  hint="Пример: Аэропорт, ТРЦ Европа"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="localForm.start_time"
                  label="Время начала*"
                  type="time"
                  required
                  variant="outlined"
                  :rules="[v => !!v || 'Время начала обязательно']"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="localForm.end_time"
                  label="Время окончания*"
                  type="time"
                  required
                  variant="outlined"
                  :rules="[v => !!v || 'Время окончания обязательно']"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model.number="localForm.interval_minutes"
                  label="Интервал (минут)*"
                  type="number"
                  required
                  variant="outlined"
                  :rules="[
                    v => !!v || 'Интервал обязателен',
                    v => v > 0 || 'Интервал должен быть больше 0',
                    v => v <= 120 || 'Интервал не может превышать 120 минут'
                  ]"
                  hint="Время между отправлениями"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model.number="localForm.duration_minutes"
                  label="Длительность (минут)*"
                  type="number"
                  required
                  variant="outlined"
                  :rules="[
                    v => !!v || 'Длительность обязательна',
                    v => v > 0 || 'Длительность должна быть больше 0',
                    v => v <= 600 || 'Длительность не может превышать 10 часов'
                  ]"
                  hint="Время в пути одного рейса"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-alert v-if="editMode" type="info" variant="tonal">
                  <div class="d-flex justify-space-between align-center">
                    <span>
                      <strong>Расписание:</strong>
                      {{ formatTime(localForm.start_time) }} - {{ formatTime(localForm.end_time) }}
                    </span>
                    <span class="text-h6">
                      {{ formatDurationShort(localForm.duration_minutes) }}
                    </span>
                  </div>
                  <div class="text-caption mt-2">
                    Интервал: {{ localForm.interval_minutes }} мин
                  </div>
                </v-alert>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="closeDialog">
            Отмена
          </v-btn>
          <v-btn color="primary" variant="flat" @click="saveRoute" :loading="saving">
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="deleteDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">Подтверждение удаления</v-card-title>
        <v-card-text>
          <p>
            Вы уверены, что хотите удалить маршрут
            <strong>{{ routeToDelete?.number }}: {{ routeToDelete?.start_point }} → {{ routeToDelete?.end_point }}</strong>?
          </p>
          <p class="text-error">
            Это действие нельзя отменить!
          </p>
          <v-alert v-if="hasSchedule(routeToDelete?.id)" type="warning" variant="tonal">
            У этого маршрута есть записи в графике водителей!
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="deleteDialog = false">
            Отмена
          </v-btn>
          <v-btn color="error" variant="flat" @click="confirmDelete" :loading="deleting">
            Удалить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог просмотра маршрута -->
    <v-dialog v-model="viewDialog" max-width="700px">
      <v-card v-if="viewingRoute">
        <v-card-title class="text-h5">
          <v-icon icon="mdi-map-marker-path" class="mr-2"></v-icon>
          Маршрут {{ viewingRoute.number }}
        </v-card-title>

        <v-card-text>
          <v-row class="mb-4">
            <v-col cols="12" class="text-center">
              <v-avatar :color="getRouteColor(viewingRoute.number)" size="120">
                <span class="white--text text-h2">{{ getRouteIcon(viewingRoute.number) }}</span>
              </v-avatar>
              <h2 class="mt-4">{{ viewingRoute.start_point }} → {{ viewingRoute.end_point }}</h2>
              <v-chip color="grey" variant="outlined" class="mt-2">
                ID: {{ viewingRoute.id }}
              </v-chip>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <v-row>
            <v-col cols="12" md="6">
              <v-list density="compact">
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-clock-start"></v-icon>
                  </template>
                  <v-list-item-title>Начало работы</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ formatTime(viewingRoute.start_time) }}
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-clock-end"></v-icon>
                  </template>
                  <v-list-item-title>Окончание работы</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ formatTime(viewingRoute.end_time) }}
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-timer-sand"></v-icon>
                  </template>
                  <v-list-item-title>Длительность рейса</v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip :color="getDurationColor(viewingRoute.duration_minutes)" size="small">
                      {{ formatDurationShort(viewingRoute.duration_minutes) }}
                    </v-chip>
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>

            <v-col cols="12" md="6">
              <v-list density="compact">
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-timer"></v-icon>
                  </template>
                  <v-list-item-title>Интервал движения</v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip :color="getIntervalColor(viewingRoute.interval_minutes)" size="small">
                      {{ viewingRoute.interval_minutes }} минут
                    </v-chip>
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-calendar-range"></v-icon>
                  </template>
                  <v-list-item-title>Рейсов в день</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ calculateTripsPerDay(viewingRoute) }}
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-bus-clock"></v-icon>
                  </template>
                  <v-list-item-title>Нужно автобусов</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ calculateBusesNeeded(viewingRoute) }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <!-- График работы -->
          <v-row>
            <v-col cols="12">
              <v-card variant="tonal" color="info">
                <v-card-title class="text-h6">
                  <v-icon icon="mdi-clock-outline" class="mr-2"></v-icon>
                  Расписание движения
                </v-card-title>
                <v-card-text>
                  <div class="text-body-1">
                    Автобусы отправляются каждые <strong>{{ viewingRoute.interval_minutes }} минут</strong>
                    с <strong>{{ formatTime(viewingRoute.start_time) }}</strong> до <strong>{{ formatTime(viewingRoute.end_time) }}</strong>
                  </div>
                  <div class="text-caption mt-2">
                    Время в пути одного рейса: {{ viewingRoute.duration_minutes }} минут
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="viewDialog = false">
            Закрыть
          </v-btn>
          <v-btn color="blue" variant="text" @click="showDriversSchedule(viewingRoute)">
            Водители
          </v-btn>
          <v-btn color="warning" variant="text" @click="editRoute(viewingRoute)">
            Редактировать
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог расписания -->
    <v-dialog v-model="scheduleDialog" max-width="600px">
      <v-card v-if="selectedRoute">
        <v-card-title class="text-h5">
          <v-icon icon="mdi-clock-outline" class="mr-2"></v-icon>
          Расписание маршрута {{ selectedRoute.number }}
        </v-card-title>

        <v-card-text>
          <div class="text-center mb-4">
            <v-chip size="large" :color="getRouteColor(selectedRoute.number)" class="mb-2">
              {{ selectedRoute.number }}: {{ selectedRoute.start_point }} → {{ selectedRoute.end_point }}
            </v-chip>
          </div>

          <v-alert type="info" variant="tonal" class="mb-4">
            <div class="d-flex justify-space-between align-center">
              <span>Начало: <strong>{{ formatTime(selectedRoute.start_time) }}</strong></span>
              <span>Конец: <strong>{{ formatTime(selectedRoute.end_time) }}</strong></span>
            </div>
          </v-alert>

          <v-list>
            <v-list-subheader>Интервалы отправления:</v-list-subheader>
            <v-list-item
              v-for="(time, index) in calculateScheduleTimes(selectedRoute)"
              :key="index"
            >
              <template v-slot:prepend>
                <v-icon :icon="index === 0 ? 'mdi-flag-checkered' : 'mdi-bus'" :color="index === 0 ? 'green' : 'blue'"></v-icon>
              </template>
              <v-list-item-title>Рейс {{ index + 1 }}</v-list-item-title>
              <v-list-item-subtitle>
                Отправление: {{ time }}
                <span v-if="index < calculateScheduleTimes(selectedRoute).length - 1">
                  • Следующий через {{ selectedRoute.interval_minutes }} мин
                </span>
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>

          <div class="mt-4 text-center">
            <v-chip color="orange" variant="tonal">
              Всего рейсов: {{ calculateScheduleTimes(selectedRoute).length }}
            </v-chip>
          </div>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="scheduleDialog = false">
            Закрыть
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог графика водителей -->
    <v-dialog v-model="driversScheduleDialog" max-width="800px">
      <v-card v-if="selectedRoute">
        <v-card-title class="text-h5">
          <v-icon icon="mdi-account-group" class="mr-2"></v-icon>
          Водители на маршруте {{ selectedRoute.number }}
        </v-card-title>

        <v-card-text>
          <div class="text-center mb-4">
            <v-chip size="large" :color="getRouteColor(selectedRoute.number)" class="mb-2">
              {{ selectedRoute.number }}: {{ selectedRoute.start_point }} → {{ selectedRoute.end_point }}
            </v-chip>
          </div>

          <v-alert v-if="driversSchedule.length === 0" type="info" variant="tonal">
            На этом маршруте пока нет записей в графике водителей.
          </v-alert>

          <v-data-table
            v-else
            :headers="driversHeaders"
            :items="driversSchedule"
            class="elevation-1"
          >
            <template v-slot:item.driver="{ item }">
              <div class="d-flex align-center">
                <v-avatar color="primary" size="36" class="mr-3">
                  <span class="white--text text-body-2">{{ getDriverInitials(item.driver) }}</span>
                </v-avatar>
                <div>
                  <strong>{{ item.driver }}</strong>
                </div>
              </div>
            </template>

            <template v-slot:item.date="{ item }">
              {{ formatDate(item.date) }}
            </template>

            <template v-slot:item.time="{ item }">
              {{ formatTime(item.start_time) }} - {{ formatTime(item.end_time) }}
            </template>

            <template v-slot:item.duration="{ item }">
              {{ calculateShiftDuration(item.start_time, item.end_time) }}
            </template>
          </v-data-table>

          <div class="mt-4 text-center">
            <v-chip color="blue" variant="tonal">
              Всего записей: {{ driversSchedule.length }}
            </v-chip>
            <v-chip color="green" variant="tonal" class="ml-2">
              Уникальных водителей: {{ uniqueDriversCount }}
            </v-chip>
          </div>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="driversScheduleDialog = false">
            Закрыть
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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
    const routes = ref([])
    const totalDuration = ref(null)
    const loading = ref(false)
    const loadingTotal = ref(false)
    const saving = ref(false)
    const deleting = ref(false)
    const dialog = ref(false)
    const deleteDialog = ref(false)
    const viewDialog = ref(false)
    const scheduleDialog = ref(false)
    const driversScheduleDialog = ref(false)
    const editMode = ref(false)
    const search = ref('')

    // Для диалогов
    const localForm = reactive({
      id: null,
      number: '',
      start_point: '',
      end_point: '',
      start_time: '06:00',
      end_time: '22:00',
      interval_minutes: 15,
      duration_minutes: 60
    })

    const routeToDelete = ref(null)
    const viewingRoute = ref(null)
    const selectedRoute = ref(null)
    const driversSchedule = ref([])

    // Уведомления
    const snackbar = reactive({
      show: false,
      message: '',
      color: 'success'
    })

    // Заголовки таблицы
    const headers = ref([
      { title: 'ID', key: 'id', sortable: false, width: '80px' },
      { title: 'Маршрут', key: 'number', sortable: false, width: '100px' },
      { title: 'Направление', key: 'route_path', sortable: false },
      { title: 'Время работы', key: 'schedule', sortable: false, width: '120px' },
      { title: 'Интервал', key: 'interval_minutes', sortable: false, width: '100px' },
      { title: 'Длительность', key: 'duration_minutes', sortable: false, width: '120px' },
      { title: 'Действия', key: 'actions', sortable: false, width: '180px', align: 'center' }
    ])

    // Заголовки для таблицы водителей
    const driversHeaders = ref([
      { title: 'Водитель', key: 'driver', sortable: false },
      { title: 'Дата', key: 'date', sortable: false, width: '120px' },
      { title: 'Время смены', key: 'time', sortable: false, width: '150px' },
      { title: 'Длительность', key: 'duration', sortable: false, width: '100px' }
    ])

    // Отфильтрованные маршруты
    const filteredRoutes = computed(() => {
      if (!search.value) return routes.value

      const searchLower = search.value.toLowerCase()
      return routes.value.filter(route =>
        route.number.toLowerCase().includes(searchLower) ||
        route.start_point.toLowerCase().includes(searchLower) ||
        route.end_point.toLowerCase().includes(searchLower) ||
        route.id.toString().includes(searchLower)
      )
    })

    // Уникальные водители
    const uniqueDriversCount = computed(() => {
      const drivers = driversSchedule.value.map(item => item.driver)
      return new Set(drivers).size
    })

    // Вспомогательные функции
    const formatTime = (timeStr) => {
      if (!timeStr) return ''
      const [hours, minutes] = timeStr.split(':')
      return `${hours.padStart(2, '0')}:${minutes.padStart(2, '0')}`
    }

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

    const formatDurationShort = (minutes) => {
      if (!minutes) return '0м'
      const hours = Math.floor(minutes / 60)
      const mins = minutes % 60

      if (hours === 0) return `${mins}м`
      return `${hours}ч ${mins}м`
    }

    const getRouteColor = (number) => {
      if (number.includes('Э') || number.includes('E')) return 'yellow-darken-2'
      if (number.includes('А') || number.includes('A')) return 'red-darken-2'
      if (number.includes('Т') || number.includes('T')) return 'green-darken-2'
      if (parseInt(number) <= 99) return 'blue-darken-2'
      return 'orange-darken-2'
    }

    const getRouteIcon = (number) => {
      if (number.includes('Э') || number.includes('E')) return 'Э'
      if (number.includes('А') || number.includes('A')) return 'А'
      if (number.includes('Т') || number.includes('T')) return 'Т'
      if (parseInt(number) <= 99) return number
      return 'М'
    }

    const getIntervalColor = (interval) => {
      if (interval <= 10) return 'green'
      if (interval <= 20) return 'blue'
      if (interval <= 30) return 'orange'
      return 'red'
    }

    const getDurationColor = (duration) => {
      if (duration <= 30) return 'green'
      if (duration <= 60) return 'blue'
      if (duration <= 120) return 'orange'
      return 'red'
    }

    const getDriverInitials = (driverName) => {
      if (!driverName) return '??'
      const parts = driverName.split(' ')
      if (parts.length >= 2) {
        return (parts[0][0] + parts[1][0]).toUpperCase()
      }
      return driverName.substring(0, 2).toUpperCase()
    }

    const calculateTripsPerDay = (route) => {
      const start = new Date(`2000-01-01T${route.start_time}`)
      const end = new Date(`2000-01-01T${route.end_time}`)
      let diff = end - start
      if (diff < 0) diff += 24 * 60 * 60 * 1000 // Если переходит через полночь
      const totalMinutes = diff / (60 * 1000)
      return Math.floor(totalMinutes / route.interval_minutes) + 1
    }

    const calculateBusesNeeded = (route) => {
      const tripsPerBus = Math.floor(route.duration_minutes / route.interval_minutes)
      if (tripsPerBus <= 0) return 1
      return Math.ceil(calculateTripsPerDay(route) / tripsPerBus)
    }

    const calculateScheduleTimes = (route) => {
      const times = []
      const start = new Date(`2000-01-01T${route.start_time}`)
      const end = new Date(`2000-01-01T${route.end_time}`)

      let current = start
      while (current <= end) {
        times.push(formatTime(current.toTimeString().substring(0, 5)))
        current = new Date(current.getTime() + route.interval_minutes * 60 * 1000)
      }

      return times
    }

    const calculateShiftDuration = (startTime, endTime) => {
      const start = new Date(`2000-01-01T${startTime}`)
      const end = new Date(`2000-01-01T${endTime}`)
      let diff = end - start
      if (diff < 0) diff += 24 * 60 * 60 * 1000
      const minutes = diff / (60 * 1000)
      return formatDurationShort(minutes)
    }

    const hasSchedule = (routeId) => {
      // Можно добавить проверку через API, если есть endpoint
      return false // временно
    }

    // API функции
    const fetchRoutes = async () => {
      loading.value = true
      try {
        const response = await apiClient.get('routes/')
        routes.value = response.data
      } catch (error) {
        console.error('Ошибка загрузки маршрутов:', error)
        showSnackbar('Ошибка загрузки данных', 'error')
      } finally {
        loading.value = false
      }
    }

    const fetchTotalDuration = async () => {
      loadingTotal.value = true
      try {
        const response = await apiClient.get('routes/total_duration/')
        totalDuration.value = response.data.total_duration_minutes
      } catch (error) {
        console.error('Ошибка загрузки общей протяженности:', error)
        // Если endpoint не работает, вычисляем на клиенте
        totalDuration.value = routes.value.reduce((sum, route) => sum + (route.duration_minutes || 0), 0)
      } finally {
        loadingTotal.value = false
      }
    }

    const fetchDriversSchedule = async (routeId) => {
      try {
        const response = await apiClient.get(`routes/${routeId}/drivers_schedule/`)
        driversSchedule.value = response.data
      } catch (error) {
        console.error('Ошибка загрузки графика водителей:', error)
        showSnackbar('Ошибка загрузки графика водителей', 'error')
      }
    }

    const fetchRouteSchedule = async (routeId) => {
      try {
        const response = await apiClient.get(`routes/${routeId}/schedule/`)
        return response.data
      } catch (error) {
        console.error('Ошибка загрузки расписания:', error)
        return null
      }
    }

    // CRUD операции
    const openCreateDialog = () => {
      editMode.value = false
      resetForm()
      dialog.value = true
    }

    const editRoute = (route) => {
      editMode.value = true
      localForm.id = route.id
      localForm.number = route.number || ''
      localForm.start_point = route.start_point || ''
      localForm.end_point = route.end_point || ''
      localForm.start_time = route.start_time || '06:00'
      localForm.end_time = route.end_time || '22:00'
      localForm.interval_minutes = route.interval_minutes || 15
      localForm.duration_minutes = route.duration_minutes || 60

      dialog.value = true
    }

    const viewRoute = (route) => {
      viewingRoute.value = route
      viewDialog.value = true
    }

    const showSchedule = async (route) => {
      selectedRoute.value = route
      const schedule = await fetchRouteSchedule(route.id)
      if (schedule) {
        selectedRoute.value = { ...route, ...schedule }
      }
      scheduleDialog.value = true
    }

    const showDriversSchedule = async (route) => {
      selectedRoute.value = route
      await fetchDriversSchedule(route.id)
      driversScheduleDialog.value = true
    }

    const saveRoute = async () => {
      // Валидация
      if (!localForm.number.trim()) {
        showSnackbar('Введите номер маршрута', 'error')
        return
      }
      if (!localForm.start_point.trim()) {
        showSnackbar('Введите начальную остановку', 'error')
        return
      }
      if (!localForm.end_point.trim()) {
        showSnackbar('Введите конечную остановку', 'error')
        return
      }
      if (!localForm.start_time || !localForm.end_time) {
        showSnackbar('Укажите время работы', 'error')
        return
      }
      if (!localForm.interval_minutes || localForm.interval_minutes <= 0) {
        showSnackbar('Введите корректный интервал', 'error')
        return
      }
      if (!localForm.duration_minutes || localForm.duration_minutes <= 0) {
        showSnackbar('Введите корректную длительность', 'error')
        return
      }

      saving.value = true
      try {
        const routeData = {
          number: localForm.number.trim(),
          start_point: localForm.start_point.trim(),
          end_point: localForm.end_point.trim(),
          start_time: localForm.start_time,
          end_time: localForm.end_time,
          interval_minutes: Number(localForm.interval_minutes),
          duration_minutes: Number(localForm.duration_minutes)
        }

        if (editMode.value) {
          await apiClient.put(`routes/${localForm.id}/`, routeData)
          showSnackbar('Маршрут успешно обновлен', 'success')
        } else {
          await apiClient.post('routes/', routeData)
          showSnackbar('Маршрут успешно создан', 'success')
        }

        await Promise.all([
          fetchRoutes(),
          fetchTotalDuration()
        ])
        closeDialog()
      } catch (error) {
        console.error('Ошибка сохранения:', error)
        const message = error.response?.data?.detail || error.response?.data || 'Ошибка сохранения'
        showSnackbar(message, 'error')
      } finally {
        saving.value = false
      }
    }

    const deleteRoute = (route) => {
      routeToDelete.value = route
      deleteDialog.value = true
    }

    const confirmDelete = async () => {
      if (!routeToDelete.value) return

      deleting.value = true
      try {
        await apiClient.delete(`routes/${routeToDelete.value.id}/`)

        showSnackbar('Маршрут успешно удален', 'success')
        await Promise.all([
          fetchRoutes(),
          fetchTotalDuration()
        ])
      } catch (error) {
        console.error('Ошибка удаления:', error)
        showSnackbar('Ошибка удаления', 'error')
      } finally {
        deleting.value = false
        deleteDialog.value = false
        routeToDelete.value = null
      }
    }

    const closeDialog = () => {
      dialog.value = false
      resetForm()
    }

    const resetForm = () => {
      localForm.id = null
      localForm.number = ''
      localForm.start_point = ''
      localForm.end_point = ''
      localForm.start_time = '06:00'
      localForm.end_time = '22:00'
      localForm.interval_minutes = 15
      localForm.duration_minutes = 60
      editMode.value = false
    }

    const showSnackbar = (message, color = 'success') => {
      snackbar.message = message
      snackbar.color = color
      snackbar.show = true
    }

    // Инициализация
    onMounted(async () => {
      await Promise.all([
        fetchRoutes(),
        fetchTotalDuration()
      ])
    })

    return {
      // Состояние
      routes,
      totalDuration,
      loading,
      loadingTotal,
      saving,
      deleting,
      dialog,
      deleteDialog,
      viewDialog,
      scheduleDialog,
      driversScheduleDialog,
      editMode,
      search,
      localForm,
      routeToDelete,
      viewingRoute,
      selectedRoute,
      driversSchedule,
      snackbar,

      // Данные таблиц
      headers,
      driversHeaders,
      filteredRoutes,
      uniqueDriversCount,

      // Методы
      fetchRoutes,
      fetchTotalDuration,
      openCreateDialog,
      editRoute,
      viewRoute,
      showSchedule,
      showDriversSchedule,
      saveRoute,
      deleteRoute,
      confirmDelete,
      closeDialog,

      // Вспомогательные методы
      formatTime,
      formatDate,
      formatDuration,
      formatDurationShort,
      getRouteColor,
      getRouteIcon,
      getIntervalColor,
      getDurationColor,
      getDriverInitials,
      calculateTripsPerDay,
      calculateBusesNeeded,
      calculateScheduleTimes,
      calculateShiftDuration,
      hasSchedule,
      showSnackbar
    }
  }
}
</script>

<style scoped>
.v-data-table {
  border-radius: 8px;
  overflow: hidden;
}

.text-success {
  color: #4CAF50;
}

.text-error {
  color: #F44336;
}

.text-orange {
  color: #FF9800;
}

/* Анимации для карточек */
.v-card {
  transition: transform 0.3s ease;
}

.v-card:hover {
  transform: translateY(-5px);
}

/* Стили для чипов */
.v-chip {
  transition: all 0.2s;
}

.v-chip:hover {
  transform: scale(1.05);
}

/* Стили для списка расписания */
.v-list-item {
  border-bottom: 1px solid rgba(0,0,0,0.1);
}

.v-list-item:last-child {
  border-bottom: none;
}
</style>
