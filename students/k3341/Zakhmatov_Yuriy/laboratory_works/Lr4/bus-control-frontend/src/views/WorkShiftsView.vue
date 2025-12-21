<template>
  <div>
    <!-- Заголовок и кнопки -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card color="red-darken-3" dark>
          <v-card-title class="text-h4">
            <v-icon icon="mdi-calendar-clock" size="large" class="mr-3"></v-icon>
            Рабочие смены
          </v-card-title>
          <v-card-subtitle class="text-h6">
            Управление графиком работы водителей
          </v-card-subtitle>
          <v-card-actions>
            <v-btn color="white" variant="outlined" @click="openCreateDialog">
              <v-icon icon="mdi-plus-circle" class="mr-2"></v-icon>
              Добавить смену
            </v-btn>
            <v-btn color="white" variant="text" @click="fetchWorkShifts">
              <v-icon icon="mdi-refresh" class="mr-2"></v-icon>
              Обновить
            </v-btn>
            <v-btn color="white" variant="text" @click="openMissedDialog">
              <v-icon icon="mdi-bus-alert" class="mr-2"></v-icon>
              Пропущенные рейсы
            </v-btn>
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              label="Поиск смен..."
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

    <!-- Фильтры -->
    <v-row class="mb-4">
      <v-col cols="12">
        <v-card elevation="2">
          <v-card-text>
            <v-row>
              <v-col cols="12" md="3">
                <v-text-field
                  v-model="filters.date"
                  label="Дата"
                  type="date"
                  variant="outlined"
                  density="compact"
                  clearable
                  @update:model-value="applyFilters"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="3">
                <v-autocomplete
                  v-model="filters.driver_id"
                  :items="drivers"
                  item-title="full_name"
                  item-value="id"
                  label="Водитель"
                  variant="outlined"
                  density="compact"
                  clearable
                  @update:model-value="applyFilters"
                ></v-autocomplete>
              </v-col>
              <v-col cols="12" md="3">
                <v-autocomplete
                  v-model="filters.bus_id"
                  :items="buses"
                  item-title="registration_number"
                  item-value="id"
                  label="Автобус"
                  variant="outlined"
                  density="compact"
                  clearable
                  @update:model-value="applyFilters"
                ></v-autocomplete>
              </v-col>
              <v-col cols="12" md="3">
                <v-autocomplete
                  v-model="filters.route_id"
                  :items="routes"
                  item-title="number"
                  item-value="id"
                  label="Маршрут"
                  variant="outlined"
                  density="compact"
                  clearable
                  @update:model-value="applyFilters"
                ></v-autocomplete>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>


    <!-- Таблица смен -->
    <v-card elevation="2">
      <v-data-table
        :headers="headers"
        :items="filteredShifts"
        :loading="loading"
        class="elevation-1"
      >
        <!-- Заголовок таблицы -->
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Список рабочих смен</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>
            <v-chip color="red" variant="tonal">
              Показано: {{ filteredShifts.length }}
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

        <!-- Колонка даты -->
        <template v-slot:item.date="{ item }">
          <div class="d-flex align-center">
            <v-icon icon="mdi-calendar" color="blue" class="mr-2"></v-icon>
            <div>
              <strong>{{ formatDate(item.date) }}</strong>
              <div class="text-caption text-medium-emphasis">
                {{ getDayOfWeek(item.date) }}
              </div>
            </div>
          </div>
        </template>

        <!-- Колонка времени -->
        <template v-slot:item.time="{ item }">
          <div class="d-flex align-center">
            <v-icon icon="mdi-clock-outline" color="orange" class="mr-2"></v-icon>
            <div>
              <div>{{ formatTime(item.start_time) }} - {{ formatTime(item.end_time) }}</div>
              <div class="text-caption text-medium-emphasis">
                {{ calculateDuration(item.start_time, item.end_time) }}
              </div>
            </div>
          </div>
        </template>

        <!-- Колонка водителя -->
        <template v-slot:item.driver="{ item }">
          <div class="d-flex align-center">
            <v-avatar color="primary" size="36" class="mr-3">
              <span class="white--text text-body-2">{{ getDriverInitials(item.driver) }}</span>
            </v-avatar>
            <div>
              <strong>{{ item.driver.last_name }} {{ item.driver.first_name }}</strong>
              <div class="text-caption text-medium-emphasis">
                Класс: {{ item.driver.driver_class?.name }}
              </div>
            </div>
          </div>
        </template>

        <!-- Колонка автобуса -->
        <template v-slot:item.bus="{ item }">
          <div class="d-flex align-center">
            <v-avatar :color="item.bus.is_active ? 'green' : 'red'" size="36" class="mr-3">
              <v-icon icon="mdi-bus" color="white"></v-icon>
            </v-avatar>
            <div>
              <strong>{{ item.bus.registration_number }}</strong>
              <div class="text-caption text-medium-emphasis">
                {{ item.bus.bus_type?.name }}
              </div>
            </div>
          </div>
        </template>

        <!-- Колонка маршрута -->
        <template v-slot:item.route="{ item }">
          <div>
            <v-chip :color="getRouteColor(item.route)" size="small" class="mb-1">
              {{ item.route.number }}
            </v-chip>
            <div class="text-caption text-medium-emphasis">
              {{ item.route.start_point }} → {{ item.route.end_point }}
            </div>
          </div>
        </template>

        <!-- Колонка причины отсутствия -->
        <template v-slot:item.absence_reason="{ item }">
          <div v-if="item.absence_reason">
            <v-chip color="red" variant="outlined" size="small">
              <v-icon icon="mdi-alert" class="mr-1"></v-icon>
              Не вышел
            </v-chip>
            <div class="text-caption text-red mt-1">
              {{ item.absence_reason }}
            </div>
          </div>
          <v-chip v-else color="green" variant="outlined" size="small">
            <v-icon icon="mdi-check" class="mr-1"></v-icon>
            Вышел на линию
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
              @click="viewShift(item)"
              title="Просмотр"
            ></v-btn>
            <v-btn
              icon="mdi-pencil"
              size="small"
              color="warning"
              variant="text"
              @click="editShift(item)"
              title="Редактировать"
            ></v-btn>
            <v-btn
              icon="mdi-delete"
              size="small"
              color="error"
              variant="text"
              @click="deleteShift(item)"
              title="Удалить"
            ></v-btn>
          </div>
        </template>

        <!-- Пустая таблица -->
        <template v-slot:no-data>
          <v-alert type="info" variant="tonal" class="ma-4">
            Нет данных о рабочих сменах. Нажмите "Добавить смену", чтобы создать первую.
          </v-alert>
        </template>
      </v-data-table>
    </v-card>

    <!-- Диалог создания/редактирования -->
    <v-dialog v-model="dialog" max-width="800px">
      <v-card>
        <v-card-title class="text-h5">
          <v-icon :icon="editMode ? 'mdi-pencil' : 'mdi-plus-circle'" class="mr-2"></v-icon>
          {{ editMode ? 'Редактирование смены' : 'Новая рабочая смена' }}
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="localForm.date"
                  label="Дата*"
                  type="date"
                  required
                  variant="outlined"
                  :rules="[v => !!v || 'Дата обязательна']"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="3">
                <v-text-field
                  v-model="localForm.start_time"
                  label="Начало смены*"
                  type="time"
                  required
                  variant="outlined"
                  :rules="[v => !!v || 'Время начала обязательно']"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="3">
                <v-text-field
                  v-model="localForm.end_time"
                  label="Конец смены*"
                  type="time"
                  required
                  variant="outlined"
                  :rules="[v => !!v || 'Время окончания обязательно']"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="4">
                <v-autocomplete
                  v-model="localForm.driver_id"
                  :items="drivers"
                  item-title="full_name"
                  item-value="id"
                  label="Водитель*"
                  :rules="[v => !!v || 'Водитель обязателен']"
                  required
                  variant="outlined"
                  :loading="loadingDrivers"
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props">
                      <template v-slot:title>
                        {{ item.raw.last_name }} {{ item.raw.first_name }}
                      </template>
                      <template v-slot:subtitle>
                        Класс: {{ item.raw.driver_class?.name }} | Опыт: {{ item.raw.experience_years }} лет
                      </template>
                    </v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>

              <v-col cols="12" md="4">
                <v-autocomplete
                  v-model="localForm.bus_id"
                  :items="activeBuses"
                  item-title="registration_number"
                  item-value="id"
                  label="Автобус*"
                  :rules="[v => !!v || 'Автобус обязателен']"
                  required
                  variant="outlined"
                  :loading="loadingBuses"
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props">
                      <template v-slot:title>
                        {{ item.raw.registration_number }}
                      </template>
                      <template v-slot:subtitle>
                        {{ item.raw.bus_type?.name }} | Депо: {{ item.raw.depot?.name }}
                      </template>
                    </v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>

              <v-col cols="12" md="4">
                <v-autocomplete
                  v-model="localForm.route_id"
                  :items="routes"
                  item-title="number"
                  item-value="id"
                  label="Маршрут*"
                  :rules="[v => !!v || 'Маршрут обязателен']"
                  required
                  variant="outlined"
                  :loading="loadingRoutes"
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props">
                      <template v-slot:title>
                        Маршрут {{ item.raw.number }}
                      </template>
                      <template v-slot:subtitle>
                        {{ item.raw.start_point }} → {{ item.raw.end_point }}
                      </template>
                    </v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>

              <v-col cols="12">
                <v-textarea
                  v-model="localForm.absence_reason"
                  label="Причина отсутствия"
                  variant="outlined"
                  rows="2"
                  hint="Заполните, если автобус не вышел на линию"
                  :disabled="!localForm.date || !localForm.driver_id"
                ></v-textarea>
                <div v-if="localForm.absence_reason" class="text-caption text-orange">
                  Если указана причина отсутствия, это будет считаться пропущенным рейсом
                </div>
              </v-col>

              <!-- Информация о конфликтах -->
              <v-col v-if="hasConflicts" cols="12">
                <v-alert type="warning" variant="tonal">
                  <template v-slot:title>
                    <strong>Возможный конфликт расписания!</strong>
                  </template>
                  У выбранного водителя уже есть смена в это время.
                  <div class="mt-2">
                    <v-btn size="small" @click="checkConflicts" variant="outlined">
                      Проверить конфликты
                    </v-btn>
                  </div>
                </v-alert>
              </v-col>

              <!-- Предпросмотр смены -->
              <v-col cols="12">
                <v-alert v-if="localForm.date && localForm.start_time && localForm.end_time"
                        type="info" variant="tonal">
                  <div class="d-flex justify-space-between align-center">
                    <div>
                      <strong>Смена:</strong> {{ formatDate(localForm.date) }}
                      <br>
                      <strong>Время:</strong> {{ formatTime(localForm.start_time) }} - {{ formatTime(localForm.end_time) }}
                      <br>
                      <strong>Длительность:</strong> {{ calculateDuration(localForm.start_time, localForm.end_time) }}
                    </div>
                    <v-chip :color="localForm.absence_reason ? 'red' : 'green'">
                      {{ localForm.absence_reason ? 'Пропущенный рейс' : 'Обычная смена' }}
                    </v-chip>
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
          <v-btn color="primary" variant="flat" @click="saveShift" :loading="saving">
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
            Вы уверены, что хотите удалить смену
            <strong>{{ shiftToDelete?.driver?.last_name }} {{ shiftToDelete?.driver?.first_name }}</strong>
            от {{ formatDate(shiftToDelete?.date) }}?
          </p>
          <p class="text-error">
            Это действие нельзя отменить!
          </p>
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

    <!-- Диалог просмотра -->
    <v-dialog v-model="viewDialog" max-width="700px">
      <v-card v-if="viewingShift">
        <v-card-title class="text-h5">
          <v-icon icon="mdi-calendar-clock" class="mr-2"></v-icon>
          Рабочая смена
        </v-card-title>

        <v-card-text>
          <v-row class="mb-4">
            <v-col cols="12" class="text-center">
              <v-avatar :color="viewingShift.absence_reason ? 'red' : 'green'" size="120">
                <v-icon icon="mdi-calendar-clock" size="x-large" color="white"></v-icon>
              </v-avatar>
              <h2 class="mt-4">{{ formatDate(viewingShift.date) }}</h2>
              <div class="text-h5">
                {{ formatTime(viewingShift.start_time) }} - {{ formatTime(viewingShift.end_time) }}
              </div>
              <v-chip color="grey" variant="outlined" class="mt-2">
                ID: {{ viewingShift.id }}
              </v-chip>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <v-row>
            <v-col cols="12" md="4">
              <v-card variant="tonal" color="blue">
                <v-card-title class="text-h6">
                  <v-icon icon="mdi-account" class="mr-2"></v-icon>
                  Водитель
                </v-card-title>
                <v-card-text>
                  <div class="text-center">
                    <v-avatar color="primary" size="80" class="mb-3">
                      <span class="white--text text-h4">{{ getDriverInitials(viewingShift.driver) }}</span>
                    </v-avatar>
                    <h3>{{ viewingShift.driver.last_name }} {{ viewingShift.driver.first_name }}</h3>
                    <v-chip size="small" class="mt-2">
                      {{ viewingShift.driver.driver_class?.name }}
                    </v-chip>
                    <div class="text-caption mt-2">
                      Опыт: {{ viewingShift.driver.experience_years }} лет
                    </div>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>

            <v-col cols="12" md="4">
              <v-card variant="tonal" color="green">
                <v-card-title class="text-h6">
                  <v-icon icon="mdi-bus" class="mr-2"></v-icon>
                  Автобус
                </v-card-title>
                <v-card-text>
                  <div class="text-center">
                    <v-avatar :color="viewingShift.bus.is_active ? 'green' : 'red'" size="80" class="mb-3">
                      <v-icon icon="mdi-bus" size="x-large" color="white"></v-icon>
                    </v-avatar>
                    <h3>{{ viewingShift.bus.registration_number }}</h3>
                    <v-chip size="small" class="mt-2">
                      {{ viewingShift.bus.bus_type?.name }}
                    </v-chip>
                    <div class="text-caption mt-2">
                      Депо: {{ viewingShift.bus.depot?.name || 'Не указано' }}
                    </div>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>

            <v-col cols="12" md="4">
              <v-card variant="tonal" color="orange">
                <v-card-title class="text-h6">
                  <v-icon icon="mdi-map-marker-path" class="mr-2"></v-icon>
                  Маршрут
                </v-card-title>
                <v-card-text>
                  <div class="text-center">
                    <v-avatar :color="getRouteColor(viewingShift.route)" size="80" class="mb-3">
                      <span class="white--text text-h4">{{ getRouteIcon(viewingShift.route) }}</span>
                    </v-avatar>
                    <h3>Маршрут {{ viewingShift.route.number }}</h3>
                    <div class="text-caption mt-2">
                      {{ viewingShift.route.start_point }} → {{ viewingShift.route.end_point }}
                    </div>
                    <div class="text-caption">
                      {{ formatTime(viewingShift.route.start_time) }} - {{ formatTime(viewingShift.route.end_time) }}
                    </div>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Причина отсутствия -->
          <v-row v-if="viewingShift.absence_reason">
            <v-col cols="12">
              <v-divider class="my-4"></v-divider>
              <v-alert type="error" variant="tonal">
                <template v-slot:title>
                  <strong>Автобус не вышел на линию</strong>
                </template>
                <strong>Причина:</strong> {{ viewingShift.absence_reason }}
              </v-alert>
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="viewDialog = false">
            Закрыть
          </v-btn>
          <v-btn color="warning" variant="text" @click="editShift(viewingShift)">
            Редактировать
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог пропущенных рейсов -->
    <v-dialog v-model="missedDialog" max-width="600px">
      <v-card>
        <v-card-title class="text-h5">
          <v-icon icon="mdi-bus-alert" class="mr-2"></v-icon>
          Пропущенные рейсы
        </v-card-title>

        <v-card-text>
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="missedDate"
                label="Выберите дату"
                type="date"
                variant="outlined"
                :max="today"
                @update:model-value="fetchMissedBuses"
              ></v-text-field>
            </v-col>
          </v-row>

          <v-alert v-if="missedBuses.length === 0 && missedDate" type="info" variant="tonal">
            На {{ formatDate(missedDate) }} нет пропущенных рейсов.
          </v-alert>

          <v-alert v-else-if="!missedDate" type="warning" variant="tonal">
            Выберите дату для просмотра пропущенных рейсов.
          </v-alert>

          <v-list v-else>
            <v-list-subheader>
              Пропущенные рейсы на {{ formatDate(missedDate) }}:
            </v-list-subheader>
            <v-list-item
              v-for="bus in missedBuses"
              :key="bus.bus"
            >
              <template v-slot:prepend>
                <v-icon icon="mdi-bus-alert" color="red"></v-icon>
              </template>
              <v-list-item-title>{{ bus.bus }}</v-list-item-title>
              <v-list-item-subtitle>{{ bus.reason }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>

          <div v-if="missedBuses.length > 0" class="mt-4 text-center">
            <v-chip color="red" variant="tonal">
              Всего пропущено: {{ missedBuses.length }}
            </v-chip>
          </div>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="missedDialog = false">
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
    const workShifts = ref([])
    const drivers = ref([])
    const buses = ref([])
    const routes = ref([])
    const missedBuses = ref([])
    const loading = ref(false)
    const loadingDrivers = ref(false)
    const loadingBuses = ref(false)
    const loadingRoutes = ref(false)
    const saving = ref(false)
    const deleting = ref(false)
    const dialog = ref(false)
    const deleteDialog = ref(false)
    const viewDialog = ref(false)
    const missedDialog = ref(false)
    const editMode = ref(false)
    const search = ref('')
    const missedDate = ref('')

    // Фильтры
    const filters = reactive({
      date: '',
      driver_id: null,
      bus_id: null,
      route_id: null
    })

    // Локальная форма
    const localForm = reactive({
      id: null,
      date: '',
      start_time: '08:00',
      end_time: '16:00',
      driver_id: null,
      bus_id: null,
      route_id: null,
      absence_reason: ''
    })

    // Для удаления и просмотра
    const shiftToDelete = ref(null)
    const viewingShift = ref(null)

    // Уведомления
    const snackbar = reactive({
      show: false,
      message: '',
      color: 'success'
    })

    // Заголовки таблицы
    const headers = ref([
      { title: 'ID', key: 'id', sortable: false, width: '80px' },
      { title: 'Дата', key: 'date', sortable: false, width: '120px' },
      { title: 'Время', key: 'time', sortable: false, width: '130px' },
      { title: 'Водитель', key: 'driver', sortable: false },
      { title: 'Автобус', key: 'bus', sortable: false, width: '150px' },
      { title: 'Маршрут', key: 'route', sortable: false, width: '150px' },
      { title: 'Статус', key: 'absence_reason', sortable: false, width: '150px' },
      { title: 'Действия', key: 'actions', sortable: false, width: '150px', align: 'center' }
    ])

    // Вычисляемые свойства
    const filteredShifts = computed(() => {
      let filtered = workShifts.value

      if (filters.date) {
        filtered = filtered.filter(shift => shift.date === filters.date)
      }
      if (filters.driver_id) {
        filtered = filtered.filter(shift => shift.driver?.id === filters.driver_id)
      }
      if (filters.bus_id) {
        filtered = filtered.filter(shift => shift.bus?.id === filters.bus_id)
      }
      if (filters.route_id) {
        filtered = filtered.filter(shift => shift.route?.id === filters.route_id)
      }

      return filtered
    })

    const activeBuses = computed(() => {
      return buses.value.filter(bus => bus.is_active)
    })

    const today = computed(() => {
      return new Date().toISOString().split('T')[0]
    })

    const hasConflicts = computed(() => {
      if (!localForm.date || !localForm.driver_id || !localForm.start_time || !localForm.end_time) {
        return false
      }

      // Проверка конфликтов для выбранного водителя в эту дату
      const driverShifts = workShifts.value.filter(
        shift => shift.driver?.id === localForm.driver_id &&
                shift.date === localForm.date &&
                shift.id !== localForm.id
      )

      if (driverShifts.length === 0) return false

      // Здесь можно добавить логику проверки пересечения времени
      return driverShifts.length > 0
    })

    // Вспомогательные функции
    const formatDate = (dateStr) => {
      if (!dateStr) return ''
      return new Date(dateStr).toLocaleDateString('ru-RU')
    }

    const formatTime = (timeStr) => {
      if (!timeStr) return ''
      return timeStr.substring(0, 5)
    }

    const getDayOfWeek = (dateStr) => {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      const days = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
      return days[date.getDay()]
    }

    const calculateDuration = (startTime, endTime) => {
      if (!startTime || !endTime) return ''

      const start = new Date(`2000-01-01T${startTime}`)
      const end = new Date(`2000-01-01T${endTime}`)
      let diff = end - start

      // Если время переходит через полночь
      if (diff < 0) diff += 24 * 60 * 60 * 1000

      const hours = Math.floor(diff / (60 * 60 * 1000))
      const minutes = Math.floor((diff % (60 * 60 * 1000)) / (60 * 1000))

      if (hours === 0) return `${minutes} мин`
      if (minutes === 0) return `${hours} ч`
      return `${hours} ч ${minutes} мин`
    }

    const getDriverInitials = (driver) => {
      if (!driver) return '??'
      return `${driver.first_name?.[0] || ''}${driver.last_name?.[0] || ''}`.toUpperCase()
    }

    const getRouteColor = (route) => {
      if (!route || !route.number) return 'blue'
      if (route.number.includes('Э') || route.number.includes('E')) return 'yellow'
      if (route.number.includes('А') || route.number.includes('A')) return 'red'
      if (route.number.includes('Т') || route.number.includes('T')) return 'green'
      return 'blue'
    }

    const getRouteIcon = (route) => {
      if (!route || !route.number) return 'М'
      if (route.number.includes('Э') || route.number.includes('E')) return 'Э'
      if (route.number.includes('А') || route.number.includes('A')) return 'А'
      if (route.number.includes('Т') || route.number.includes('T')) return 'Т'
      return route.number
    }

    const getUniqueDates = () => {
      const dates = workShifts.value.map(shift => shift.date)
      return [...new Set(dates)].sort()
    }

    const getDateColor = (date) => {
      const shifts = workShifts.value.filter(shift => shift.date === date)
      const missed = shifts.filter(shift => shift.absence_reason)

      if (missed.length > 0) return 'red'
      if (shifts.length > 5) return 'orange'
      return 'blue'
    }

    const getShiftsCountForDate = (date) => {
      return workShifts.value.filter(shift => shift.date === date).length
    }

    // API функции
    const fetchWorkShifts = async () => {
      loading.value = true
      try {
        const response = await apiClient.get('workshifts/')
        workShifts.value = response.data
      } catch (error) {
        console.error('Ошибка загрузки смен:', error)
        showSnackbar('Ошибка загрузки данных', 'error')
      } finally {
        loading.value = false
      }
    }

    const fetchDrivers = async () => {
      loadingDrivers.value = true
      try {
        const response = await apiClient.get('drivers/')
        drivers.value = response.data.map(driver => ({
          ...driver,
          full_name: `${driver.last_name} ${driver.first_name}`
        }))
      } catch (error) {
        console.error('Ошибка загрузки водителей:', error)
      } finally {
        loadingDrivers.value = false
      }
    }

    const fetchBuses = async () => {
      loadingBuses.value = true
      try {
        const response = await apiClient.get('buses/')
        buses.value = response.data
      } catch (error) {
        console.error('Ошибка загрузки автобусов:', error)
      } finally {
        loadingBuses.value = false
      }
    }

    // Завершение файла, продолжая с того места, где остановился код

const fetchRoutes = async () => {
  loadingRoutes.value = true
  try {
    const response = await apiClient.get('routes/')
    routes.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки маршрутов:', error)
  } finally {
    loadingRoutes.value = false
  }
}

const fetchMissedBuses = async () => {
  if (!missedDate.value) return

  try {
    const response = await apiClient.get('workshifts/missed/', {
      params: { date: missedDate.value }
    })
    missedBuses.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки пропущенных рейсов:', error)
    showSnackbar('Ошибка загрузки пропущенных рейсов', 'error')
  }
}

// Уведомления
const showSnackbar = (message, color = 'success') => {
  snackbar.message = message
  snackbar.color = color
  snackbar.show = true
}

// Диалоги
const openCreateDialog = () => {
  editMode.value = false
  Object.assign(localForm, {
    id: null,
    date: new Date().toISOString().split('T')[0],
    start_time: '08:00',
    end_time: '16:00',
    driver_id: null,
    bus_id: null,
    route_id: null,
    absence_reason: ''
  })
  dialog.value = true
}

const openMissedDialog = () => {
  missedDate.value = new Date().toISOString().split('T')[0]
  missedDialog.value = true
  fetchMissedBuses()
}

const viewShift = (shift) => {
  viewingShift.value = shift
  viewDialog.value = true
}

const editShift = (shift) => {
  editMode.value = true
  Object.assign(localForm, {
    id: shift.id,
    date: shift.date,
    start_time: shift.start_time,
    end_time: shift.end_time,
    driver_id: shift.driver?.id,
    bus_id: shift.bus?.id,
    route_id: shift.route?.id,
    absence_reason: shift.absence_reason || ''
  })
  dialog.value = true
}

const deleteShift = (shift) => {
  shiftToDelete.value = shift
  deleteDialog.value = true
}

// Сохранение смены
const saveShift = async () => {
  // Валидация
  if (!localForm.date || !localForm.start_time || !localForm.end_time) {
    showSnackbar('Заполните обязательные поля: дата и время', 'error')
    return
  }

  if (!localForm.driver_id || !localForm.bus_id || !localForm.route_id) {
    showSnackbar('Выберите водителя, автобус и маршрут', 'error')
    return
  }

  // Проверка, что время окончания позже времени начала
  const start = new Date(`2000-01-01T${localForm.start_time}`)
  const end = new Date(`2000-01-01T${localForm.end_time}`)
  if (end <= start) {
    showSnackbar('Время окончания должно быть позже времени начала', 'error')
    return
  }

  saving.value = true
  try {
    const shiftData = {
      date: localForm.date,
      start_time: localForm.start_time,
      end_time: localForm.end_time,
      driver: localForm.driver_id,
      bus: localForm.bus_id,
      route: localForm.route_id,
      absence_reason: localForm.absence_reason || null
    }

    if (editMode.value && localForm.id) {
      // Обновление существующей смены
      await apiClient.put(`workshifts/${localForm.id}/`, shiftData)
      showSnackbar('Смена успешно обновлена')
    } else {
      // Создание новой смены
      await apiClient.post('workshifts/', shiftData)
      showSnackbar('Смена успешно создана')
    }

    // Обновляем список смен
    await fetchWorkShifts()

    // Закрываем диалог
    closeDialog()

  } catch (error) {
    console.error('Ошибка сохранения смены:', error)

    // Обработка ошибок валидации
    if (error.response?.data) {
      const errorData = error.response.data
      let errorMessage = 'Ошибка сохранения'

      if (typeof errorData === 'object') {
        // Собираем все ошибки в одну строку
        const errors = []
        for (const [field, messages] of Object.entries(errorData)) {
          errors.push(`${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
        }
        errorMessage = errors.join('; ')
      } else if (typeof errorData === 'string') {
        errorMessage = errorData
      }

      showSnackbar(errorMessage, 'error')
    } else {
      showSnackbar('Ошибка сохранения. Проверьте подключение к серверу', 'error')
    }
  } finally {
    saving.value = false
  }
}

// Подтверждение удаления
const confirmDelete = async () => {
  if (!shiftToDelete.value) return

  deleting.value = true
  try {
    await apiClient.delete(`workshifts/${shiftToDelete.value.id}/`)
    showSnackbar('Смена успешно удалена')

    // Обновляем список смен
    await fetchWorkShifts()

  } catch (error) {
    console.error('Ошибка удаления смены:', error)
    showSnackbar('Ошибка удаления смены', 'error')
  } finally {
    deleting.value = false
    deleteDialog.value = false
    shiftToDelete.value = null
  }
}

// Закрытие диалога
const closeDialog = () => {
  dialog.value = false
  setTimeout(() => {
    Object.assign(localForm, {
      id: null,
      date: '',
      start_time: '08:00',
      end_time: '16:00',
      driver_id: null,
      bus_id: null,
      route_id: null,
      absence_reason: ''
    })
  }, 300)
}

// Фильтры
const applyFilters = () => {
  // Фильтры применяются автоматически через computed свойство
  console.log('Фильтры применены:', filters)
}

const setDateFilter = (date) => {
  filters.date = date
  // Автоматическое применение через v-model
}

const checkConflicts = async () => {
  if (!localForm.driver_id || !localForm.date) return

  try {
    // Получаем все смены водителя на выбранную дату
    const response = await apiClient.get('workshifts/', {
      params: {
        driver_id: localForm.driver_id,
        date: localForm.date
      }
    })

    const conflicts = response.data.filter(shift => {
      // Исключаем текущую смену при редактировании
      if (editMode.value && shift.id === localForm.id) return false

      // Проверяем пересечение временных интервалов
      const existingStart = new Date(`2000-01-01T${shift.start_time}`)
      const existingEnd = new Date(`2000-01-01T${shift.end_time}`)
      const newStart = new Date(`2000-01-01T${localForm.start_time}`)
      const newEnd = new Date(`2000-01-01T${localForm.end_time}`)

      return (newStart < existingEnd && newEnd > existingStart)
    })

    if (conflicts.length > 0) {
      let message = `Найдены конфликты с ${conflicts.length} сменой(ами):\n`
      conflicts.forEach((shift, index) => {
        message += `${index + 1}. ${formatTime(shift.start_time)}-${formatTime(shift.end_time)} `
        message += `(Маршрут: ${shift.route?.number})\n`
      })

      // Показываем предупреждение
      if (confirm(message + '\nВсе равно сохранить?')) {
        return true // Продолжить сохранение
      } else {
        return false // Отменить сохранение
      }
    }

    showSnackbar('Конфликтов не найдено', 'info')
    return true

  } catch (error) {
    console.error('Ошибка проверки конфликтов:', error)
    return true // Продолжить в случае ошибки
  }
}

// Инициализация
onMounted(async () => {
  await Promise.all([
    fetchWorkShifts(),
    fetchDrivers(),
    fetchBuses(),
    fetchRoutes()
  ])
})

// Экспорт
return {
  // Реактивные переменные
  workShifts,
  drivers,
  buses,
  routes,
  missedBuses,
  loading,
  loadingDrivers,
  loadingBuses,
  loadingRoutes,
  saving,
  deleting,
  dialog,
  deleteDialog,
  viewDialog,
  missedDialog,
  editMode,
  search,
  missedDate,
  filters,
  localForm,
  shiftToDelete,
  viewingShift,
  snackbar,
  headers,

  // Вычисляемые свойства
  filteredShifts,
  activeBuses,
  today,
  hasConflicts,

  // Вспомогательные функции
  formatDate,
  formatTime,
  getDayOfWeek,
  calculateDuration,
  getDriverInitials,
  getRouteColor,
  getRouteIcon,
  getUniqueDates,
  getDateColor,
  getShiftsCountForDate,

  // Методы
  fetchWorkShifts,
  fetchMissedBuses,
  showSnackbar,
  openCreateDialog,
  openMissedDialog,
  viewShift,
  editShift,
  deleteShift,
  saveShift,
  confirmDelete,
  closeDialog,
  applyFilters,
  setDateFilter,
  checkConflicts
}
  }
}
</script>

<style scoped>
.v-badge {
  --v-badge-size: 18px;
}

.v-chip {
  cursor: pointer;
}

.v-chip:hover {
  opacity: 0.8;
}

.gap-2 {
  gap: 8px;
}

.text-error {
  color: #f44336;
}

.text-orange {
  color: #ff9800;
}
</style>
