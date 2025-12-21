<template>
  <div>
    <!-- Заголовок и кнопки -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card color="blue-darken-3" dark>
          <v-card-title class="text-h4">
            <v-icon icon="mdi-bus" size="large" class="mr-3"></v-icon>
            Автобусы
          </v-card-title>
          <v-card-subtitle class="text-h6">
            Управление автопарком
          </v-card-subtitle>
          <v-card-actions>
            <v-btn color="white" variant="outlined" @click="openCreateDialog">
              <v-icon icon="mdi-plus-circle" class="mr-2"></v-icon>
              Добавить автобус
            </v-btn>
            <v-btn color="white" variant="text" @click="fetchBuses">
              <v-icon icon="mdi-refresh" class="mr-2"></v-icon>
              Обновить
            </v-btn>
            <v-btn color="white" variant="text" @click="toggleFilters">
              <v-icon icon="mdi-filter" class="mr-2"></v-icon>
              {{ showFilters ? 'Скрыть фильтры' : 'Фильтры' }}
            </v-btn>
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              label="Поиск автобусов..."
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
    <v-expand-transition>
      <v-row v-if="showFilters" class="mb-4">
        <v-col cols="12">
          <v-card elevation="2">
            <v-card-text>
              <v-row>
                <v-col cols="12" md="4">
                  <v-select
                    v-model="filters.bus_type_id"
                    :items="busTypes"
                    item-title="name"
                    item-value="id"
                    label="Тип автобуса"
                    clearable
                    variant="outlined"
                    density="compact"
                  ></v-select>
                </v-col>
                <v-col cols="12" md="4">
                  <v-select
                    v-model="filters.depot_id"
                    :items="depots"
                    item-title="name"
                    item-value="id"
                    label="Депо"
                    clearable
                    variant="outlined"
                    density="compact"
                  ></v-select>
                </v-col>
                <v-col cols="12" md="4">
                  <v-select
                    v-model="filters.is_active"
                    :items="[
                      { title: 'Все', value: null },
                      { title: 'Активные', value: true },
                      { title: 'Неактивные', value: false }
                    ]"
                    label="Статус"
                    clearable
                    variant="outlined"
                    density="compact"
                  ></v-select>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-expand-transition>

    <!-- Статистика -->
    <v-row class="mb-4">
      <v-col cols="12" sm="6" md="3">
        <v-card elevation="2">
          <v-card-text class="text-center">
            <div class="text-h4">{{ totalBuses }}</div>
            <div class="text-subtitle-1">Всего автобусов</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card elevation="2" color="green-lighten-5">
          <v-card-text class="text-center">
            <div class="text-h4">{{ activeBuses }}</div>
            <div class="text-subtitle-1">Активных</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card elevation="2" color="orange-lighten-5">
          <v-card-text class="text-center">
            <div class="text-h4">{{ inactiveBuses }}</div>
            <div class="text-subtitle-1">Неактивных</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card elevation="2" color="blue-lighten-5">
          <v-card-text class="text-center">
            <div class="text-h4">{{ depots.length }}</div>
            <div class="text-subtitle-1">Депо</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Таблица автобусов -->
    <v-card elevation="2">
      <v-data-table
        :headers="headers"
        :items="filteredBuses"
        :loading="loading"
        :search="search"
        class="elevation-1"
      >
        <!-- Заголовок таблицы -->
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Список автобусов</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>
            <v-chip color="blue" variant="tonal">
              Показано: {{ filteredBuses.length }}
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

        <!-- Колонка регистрационного номера -->
        <template v-slot:item.registration_number="{ item }">
          <div class="d-flex align-center">
            <v-avatar :color="getBusColor(item)" size="36" class="mr-3">
              <v-icon icon="mdi-bus" color="white"></v-icon>
            </v-avatar>
            <div>
              <strong class="text-h6">{{ item.registration_number }}</strong>
              <div class="text-caption text-medium-emphasis">
                ID: {{ item.id }}
              </div>
            </div>
          </div>
        </template>

        <!-- Колонка типа автобуса -->
        <template v-slot:item.bus_type.name="{ item }">
          <v-chip :color="getTypeColor(item.bus_type?.name)" size="small">
            {{ item.bus_type?.name || 'Не указан' }}
            <template v-if="item.bus_type">
              ({{ item.bus_type.capacity }} мест)
            </template>
          </v-chip>
        </template>

        <!-- Колонка депо -->
        <template v-slot:item.depot.name="{ item }">
          <div v-if="item.depot">
            <v-chip :color="getDepotColor(item.depot)" size="small">
              {{ item.depot.name }}
            </v-chip>
            <div class="text-caption text-medium-emphasis">
              {{ formatDepotInfo(item.depot) }}
            </div>
          </div>
          <v-chip v-else color="grey" size="small" variant="outlined">
            Не указано
          </v-chip>
        </template>

        <!-- Колонка статуса -->
        <template v-slot:item.is_active="{ item }">
          <v-chip :color="item.is_active ? 'green' : 'red'" variant="flat">
            {{ item.is_active ? 'Активен' : 'Неактивен' }}
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
              @click="viewBus(item)"
              title="Просмотр"
            ></v-btn>
            <v-btn
              icon="mdi-pencil"
              size="small"
              color="warning"
              variant="text"
              @click="editBus(item)"
              title="Редактировать"
            ></v-btn>
            <v-btn
              icon="mdi-delete"
              size="small"
              color="error"
              variant="text"
              @click="deleteBus(item)"
              title="Удалить"
            ></v-btn>
          </div>
        </template>

        <!-- Пустая таблица -->
        <template v-slot:no-data>
          <v-alert type="info" variant="tonal" class="ma-4">
            Нет данных об автобусах. Нажмите "Добавить автобус", чтобы создать первый.
          </v-alert>
        </template>
      </v-data-table>
    </v-card>

    <!-- Диалог создания/редактирования -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title class="text-h5">
          <v-icon :icon="editMode ? 'mdi-pencil' : 'mdi-bus-plus'" class="mr-2"></v-icon>
          {{ editMode ? 'Редактирование автобуса' : 'Новый автобус' }}
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="localForm.registration_number"
                  label="Регистрационный номер*"
                  required
                  variant="outlined"
                  :rules="[v => !!v || 'Номер обязателен']"
                  hint="Пример: A123BC 777"
                  counter="20"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-autocomplete
                  v-model="localForm.bus_type_id"
                  :items="busTypes"
                  item-title="name"
                  item-value="id"
                  label="Тип автобуса*"
                  :rules="[v => !!v || 'Тип обязателен']"
                  required
                  variant="outlined"
                  :loading="loadingTypes"
                  :disabled="loadingTypes"
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props">
                      <template v-slot:title>
                        {{ item.raw.name }}
                      </template>
                      <template v-slot:subtitle>
                        Вместимость: {{ item.raw.capacity }} мест
                      </template>
                    </v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>

              <v-col cols="12" md="6">
                <v-autocomplete
                  v-model="localForm.depot_id"
                  :items="depots"
                  item-title="name"
                  item-value="id"
                  label="Депо*"
                  :rules="[v => !!v || 'Депо обязательно']"
                  required
                  variant="outlined"
                  :loading="loadingDepots"
                  :disabled="loadingDepots"
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props">
                      <template v-slot:title>
                        {{ item.raw.name }}
                      </template>
                      <template v-slot:subtitle>
                        {{ item.raw.address }} (свободно: {{ item.raw.free_spaces }})
                      </template>
                    </v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>

              <v-col cols="12">
                <v-switch
                  v-model="localForm.is_active"
                  label="Автобус активен"
                  color="green"
                  hide-details
                ></v-switch>
                <div class="text-caption text-medium-emphasis mt-1">
                  Неактивные автобусы не выходят на маршруты
                </div>
              </v-col>

              <v-col v-if="localForm.depot_id" cols="12">
                <v-alert type="info" variant="tonal">
                  <template v-slot:title>
                    <strong>Информация о депо:</strong>
                  </template>
                  {{ getDepotInfo(localForm.depot_id) }}
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
          <v-btn color="primary" variant="flat" @click="saveBus" :loading="saving">
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
            Вы уверены, что хотите удалить автобус
            <strong>{{ busToDelete?.registration_number }}</strong>?
          </p>
          <v-alert v-if="hasWorkShifts(busToDelete?.id)" type="warning" variant="tonal">
            У этого автобуса есть записи в графике работы!
          </v-alert>
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
      <v-card v-if="viewingBus">
        <v-card-title class="text-h5">
          <v-icon icon="mdi-bus" class="mr-2"></v-icon>
          Автобус {{ viewingBus.registration_number }}
        </v-card-title>

        <v-card-text>
          <v-row class="mb-4">
            <v-col cols="12" class="text-center">
              <v-avatar :color="getBusColor(viewingBus)" size="120">
                <v-icon icon="mdi-bus" size="x-large" color="white"></v-icon>
              </v-avatar>
              <h2 class="mt-4">{{ viewingBus.registration_number }}</h2>
              <v-chip color="grey" variant="outlined" class="mt-2">
                ID: {{ viewingBus.id }}
              </v-chip>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <v-row>
            <v-col cols="12" md="6">
              <v-list density="compact">
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-bus-double-decker"></v-icon>
                  </template>
                  <v-list-item-title>Тип автобуса</v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip :color="getTypeColor(viewingBus.bus_type?.name)" size="small">
                      {{ viewingBus.bus_type?.name || 'Не указан' }}
                    </v-chip>
                    <span v-if="viewingBus.bus_type" class="ml-2">
                      ({{ viewingBus.bus_type.capacity }} мест)
                    </span>
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-map-marker"></v-icon>
                  </template>
                  <v-list-item-title>Депо</v-list-item-title>
                  <v-list-item-subtitle v-if="viewingBus.depot">
                    <div>
                      <strong>{{ viewingBus.depot.name }}</strong>
                    </div>
                    <div>{{ viewingBus.depot.address }}</div>
                    <div class="mt-1">
                      <v-chip size="small" :color="getDepotColor(viewingBus.depot)">
                        {{ viewingBus.depot.current_occupancy }}/{{ viewingBus.depot.capacity }}
                      </v-chip>
                    </div>
                  </v-list-item-subtitle>
                  <v-list-item-subtitle v-else>
                    Не указано
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>

            <v-col cols="12" md="6">
              <v-list density="compact">
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon :icon="viewingBus.is_active ? 'mdi-check-circle' : 'mdi-close-circle'"
                            :color="viewingBus.is_active ? 'green' : 'red'"></v-icon>
                  </template>
                  <v-list-item-title>Статус</v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip :color="viewingBus.is_active ? 'green' : 'red'" variant="flat">
                      {{ viewingBus.is_active ? 'Активен' : 'Неактивен' }}
                    </v-chip>
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-calendar"></v-icon>
                  </template>
                  <v-list-item-title>Добавлен</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ formatDate(viewingBus.created_at) || 'Неизвестно' }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <!-- Контакты депо -->
          <v-row v-if="viewingBus.depot">
            <v-col cols="12">
              <v-card variant="tonal" color="info">
                <v-card-title class="text-h6">
                  <v-icon icon="mdi-contacts" class="mr-2"></v-icon>
                  Контакты депо
                </v-card-title>
                <v-card-text>
                  <v-row>
                    <v-col cols="12" md="6">
                      <div class="d-flex align-center mb-2">
                        <v-icon icon="mdi-phone" class="mr-2"></v-icon>
                        <span>{{ viewingBus.depot.phone }}</span>
                      </div>
                    </v-col>
                    <v-col cols="12" md="6">
                      <div class="d-flex align-center mb-2">
                        <v-icon icon="mdi-email" class="mr-2"></v-icon>
                        <span>{{ viewingBus.depot.email }}</span>
                      </div>
                    </v-col>
                  </v-row>
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
          <v-btn color="warning" variant="text" @click="editBus(viewingBus)">
            Редактировать
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
    const buses = ref([])
    const busTypes = ref([])
    const depots = ref([])
    const loading = ref(false)
    const loadingTypes = ref(false)
    const loadingDepots = ref(false)
    const saving = ref(false)
    const deleting = ref(false)
    const dialog = ref(false)
    const deleteDialog = ref(false)
    const viewDialog = ref(false)
    const showFilters = ref(false)
    const editMode = ref(false)
    const search = ref('')

    // Фильтры
    const filters = reactive({
      bus_type_id: null,
      depot_id: null,
      is_active: null
    })

    // Локальная форма
    const localForm = reactive({
      id: null,
      registration_number: '',
      bus_type_id: null,
      depot_id: null,
      is_active: true
    })

    // Для удаления и просмотра
    const busToDelete = ref(null)
    const viewingBus = ref(null)

    // Уведомления
    const snackbar = reactive({
      show: false,
      message: '',
      color: 'success'
    })

    // Заголовки таблицы
    const headers = ref([
      { title: 'ID', key: 'id', sortable: false, width: '80px' },
      { title: 'Рег. номер', key: 'registration_number', sortable: false },
      { title: 'Тип', key: 'bus_type.name', sortable: false },
      { title: 'Депо', key: 'depot.name', sortable: false },
      { title: 'Статус', key: 'is_active', sortable: false, width: '100px' },
      { title: 'Действия', key: 'actions', sortable: false, width: '150px', align: 'center' }
    ])

    // Вычисляемые свойства
    const filteredBuses = computed(() => {
      return buses.value.filter(bus => {
        if (filters.bus_type_id && bus.bus_type?.id !== filters.bus_type_id) return false
        if (filters.depot_id && bus.depot?.id !== filters.depot_id) return false
        if (filters.is_active !== null && bus.is_active !== filters.is_active) return false
        return true
      })
    })

    const totalBuses = computed(() => buses.value.length)
    const activeBuses = computed(() => buses.value.filter(b => b.is_active).length)
    const inactiveBuses = computed(() => buses.value.filter(b => !b.is_active).length)

    // Вспомогательные функции
    const formatDate = (dateStr) => {
      if (!dateStr) return ''
      return new Date(dateStr).toLocaleDateString('ru-RU')
    }

    const getBusColor = (bus) => {
      if (!bus.is_active) return 'grey'
      if (bus.bus_type?.name?.includes('Городской')) return 'blue'
      if (bus.bus_type?.name?.includes('Пригородный')) return 'green'
      if (bus.bus_type?.name?.includes('Туристический')) return 'orange'
      return 'blue-darken-2'
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

    const getDepotColor = (depot) => {
      if (!depot) return 'grey'
      const percentage = (depot.current_occupancy / depot.capacity) * 100
      if (percentage < 50) return 'green'
      if (percentage < 80) return 'orange'
      return 'red'
    }

    const formatDepotInfo = (depot) => {
      if (!depot) return ''
      return `${depot.address} (${depot.current_occupancy}/${depot.capacity})`
    }

    const getDepotInfo = (depotId) => {
      const depot = depots.value.find(d => d.id === depotId)
      if (!depot) return ''
      return `${depot.name}, ${depot.address}. Свободно мест: ${depot.free_spaces}`
    }

    const hasWorkShifts = (busId) => {
      // Можно добавить проверку через API если есть endpoint
      return false
    }

    // API функции
    const fetchBuses = async () => {
      loading.value = true
      try {
        const response = await apiClient.get('buses/')
        buses.value = response.data
      } catch (error) {
        console.error('Ошибка загрузки автобусов:', error)
        showSnackbar('Ошибка загрузки данных', 'error')
      } finally {
        loading.value = false
      }
    }

    const fetchBusTypes = async () => {
      loadingTypes.value = true
      try {
        const response = await apiClient.get('bus-types/')
        busTypes.value = response.data
      } catch (error) {
        console.error('Ошибка загрузки типов автобусов:', error)
      } finally {
        loadingTypes.value = false
      }
    }

    const fetchDepots = async () => {
      loadingDepots.value = true
      try {
        try {
          const response = await apiClient.get('depots/')
          depots.value = response.data || []

          // Обогащаем депо статистикой
          const depotsWithStats = await Promise.all(
            depots.value.map(async (depot) => {
              try {
                // Получаем статистику для каждого депо
                const statsResponse = await apiClient.get(`depots/${depot.id}/statistics/`)
                const stats = statsResponse.data

                return {
                  ...depot,
                  capacity: stats.capacity || depot.capacity || 0,
                  current_occupancy: stats.current_occupancy || 0,
                  free_spaces: stats.free_spaces || 0,
                  active_buses: stats.active_buses || 0,
                  inactive_buses: stats.inactive_buses || 0
                }
              } catch (statsError) {
                console.warn(`Не удалось загрузить статистику для депо ${depot.id}:`, statsError)
                // Возвращаем депо без статистики
                return {
                  ...depot,
                  capacity: depot.capacity || 0,
                  current_occupancy: 0,
                  free_spaces: depot.capacity || 0,
                  active_buses: 0,
                  inactive_buses: 0
                }
              }
            })
          )

          depots.value = depotsWithStats
          console.log('✅ Загружены депо:', depots.value)

        } catch (apiError) {
          console.warn('Не удалось загрузить депо через API:', apiError)
        }

      } catch (error) {
        console.error('Общая ошибка загрузки депо:', error)
      } finally {
        loadingDepots.value = false
      }
    }

    // CRUD операции
    const openCreateDialog = () => {
      editMode.value = false
      resetForm()
      dialog.value = true
    }

    const editBus = (bus) => {
      editMode.value = true
      localForm.id = bus.id
      localForm.registration_number = bus.registration_number || ''
      localForm.bus_type_id = bus.bus_type?.id || bus.bus_type_id || null
      localForm.depot_id = bus.depot?.id || bus.depot_id || null
      localForm.is_active = bus.is_active

      dialog.value = true
    }

    const viewBus = (bus) => {
      viewingBus.value = bus
      viewDialog.value = true
    }

    const saveBus = async () => {
      // Валидация
      if (!localForm.registration_number.trim()) {
        showSnackbar('Введите регистрационный номер', 'error')
        return
      }
      if (!localForm.bus_type_id) {
        showSnackbar('Выберите тип автобуса', 'error')
        return
      }
      if (!localForm.depot_id) {
        showSnackbar('Выберите депо', 'error')
        return
      }

      saving.value = true
      try {
        const busData = {
          registration_number: localForm.registration_number.trim(),
          bus_type_id: Number(localForm.bus_type_id),
          depot_id: Number(localForm.depot_id),
          is_active: localForm.is_active
        }

        if (editMode.value) {
          await apiClient.put(`buses/${localForm.id}/`, busData)
          showSnackbar('Автобус успешно обновлен', 'success')
        } else {
          await apiClient.post('buses/', busData)
          showSnackbar('Автобус успешно создан', 'success')
        }

        await fetchBuses()
        closeDialog()
      } catch (error) {
        console.error('Ошибка сохранения:', error)
        const message = error.response?.data?.detail || error.response?.data || 'Ошибка сохранения'
        showSnackbar(message, 'error')
      } finally {
        saving.value = false
      }
    }

    const deleteBus = (bus) => {
      busToDelete.value = bus
      deleteDialog.value = true
    }

    const confirmDelete = async () => {
      if (!busToDelete.value) return

      deleting.value = true
      try {
        await apiClient.delete(`buses/${busToDelete.value.id}/`)

        showSnackbar('Автобус успешно удален', 'success')
        await fetchBuses()
      } catch (error) {
        console.error('Ошибка удаления:', error)
        showSnackbar('Ошибка удаления', 'error')
      } finally {
        deleting.value = false
        deleteDialog.value = false
        busToDelete.value = null
      }
    }

    const closeDialog = () => {
      dialog.value = false
      resetForm()
    }

    const resetForm = () => {
      localForm.id = null
      localForm.registration_number = ''
      localForm.bus_type_id = null
      localForm.depot_id = null
      localForm.is_active = true
      editMode.value = false
    }

    const toggleFilters = () => {
      showFilters.value = !showFilters.value
    }

    const showSnackbar = (message, color = 'success') => {
      snackbar.message = message
      snackbar.color = color
      snackbar.show = true
    }

    // Инициализация
    onMounted(async () => {
      await Promise.all([
        fetchBuses(),
        fetchBusTypes(),
        fetchDepots()
      ])
    })

    return {
      // Состояние
      buses,
      busTypes,
      depots,
      loading,
      loadingTypes,
      loadingDepots,
      saving,
      deleting,
      dialog,
      deleteDialog,
      viewDialog,
      showFilters,
      editMode,
      search,
      filters,
      localForm,
      busToDelete,
      viewingBus,
      snackbar,

      // Вычисляемые свойства
      headers,
      filteredBuses,
      totalBuses,
      activeBuses,
      inactiveBuses,

      // Методы
      fetchBuses,
      openCreateDialog,
      editBus,
      viewBus,
      saveBus,
      deleteBus,
      confirmDelete,
      closeDialog,
      toggleFilters,

      // Вспомогательные методы
      formatDate,
      getBusColor,
      getTypeColor,
      getDepotColor,
      formatDepotInfo,
      getDepotInfo,
      hasWorkShifts,
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

/* Анимации */
.v-card {
  transition: transform 0.3s ease;
}

.v-card:hover {
  transform: translateY(-5px);
}

/* Стили для статистики */
.v-card.elevation-2 {
  border-radius: 12px;
}
</style>
