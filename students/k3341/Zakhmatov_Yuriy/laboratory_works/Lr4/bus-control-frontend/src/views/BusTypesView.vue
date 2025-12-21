<template>
  <div>
    <!-- Заголовок и кнопка добавления -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card color="green-darken-3" dark>
          <v-card-title class="text-h4">
            <v-icon icon="mdi-bus-double-decker" size="large" class="mr-3"></v-icon>
            Типы автобусов
          </v-card-title>
          <v-card-subtitle class="text-h6">
            Управление типами транспортных средств
          </v-card-subtitle>
          <v-card-actions>
            <v-btn color="white" variant="outlined" @click="openCreateDialog">
              <v-icon icon="mdi-plus-circle" class="mr-2"></v-icon>
              Добавить тип
            </v-btn>
            <v-btn color="white" variant="text" @click="fetchBusTypes">
              <v-icon icon="mdi-refresh" class="mr-2"></v-icon>
              Обновить
            </v-btn>
            <v-btn color="white" variant="text" @click="showReport = !showReport">
              <v-icon icon="mdi-chart-bar" class="mr-2"></v-icon>
              {{ showReport ? 'Скрыть отчет' : 'Показать отчет' }}
            </v-btn>
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              label="Поиск типов..."
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

    <!-- Отчет по автопарку -->
    <v-expand-transition>
      <div v-if="showReport && report.length > 0">
        <v-row class="mb-6">
          <v-col cols="12">
            <v-card elevation="2">
              <v-card-title class="text-h6">
                <v-icon icon="mdi-chart-bar" class="mr-2"></v-icon>
                Отчет по автопарку
                <v-chip color="primary" class="ml-2">
                  {{ report.length }} {{ report.length === 1 ? 'тип' : 'типа' }}
                </v-chip>
              </v-card-title>
              <v-card-text>
                <v-row>
                  <v-col
                    v-for="item in report"
                    :key="item.bus_type"
                    cols="12" md="6" lg="4"
                  >
                    <v-card class="mb-4" elevation="3">
                      <v-card-title class="text-h6">
                        <v-icon icon="mdi-bus" class="mr-2"></v-icon>
                        {{ item.bus_type }}
                      </v-card-title>
                      <v-card-subtitle>
                        Автобусов: {{ item.bus_count }}
                      </v-card-subtitle>
                      <v-card-text>
                        <v-list density="compact">
                          <v-list-item>
                            <template v-slot:prepend>
                              <v-icon icon="mdi-map-marker-path"></v-icon>
                            </template>
                            <v-list-item-title>Маршрутов</v-list-item-title>
                            <v-list-item-subtitle>
                              {{ item.routes?.length || 0 }}
                              <template v-if="item.total_route_duration">
                                ({{ formatDuration(item.total_route_duration) }})
                              </template>
                            </v-list-item-subtitle>
                          </v-list-item>

                          <v-list-item>
                            <template v-slot:prepend>
                              <v-icon icon="mdi-account-group"></v-icon>
                            </template>
                            <v-list-item-title>Водителей</v-list-item-title>
                            <v-list-item-subtitle>
                              {{ item.drivers?.length || 0 }}
                              <template v-if="item.drivers_avg_experience">
                                (ср. опыт: {{ item.drivers_avg_experience.toFixed(1) }} лет)
                              </template>
                            </v-list-item-subtitle>
                          </v-list-item>
                        </v-list>

                        <v-divider class="my-2"></v-divider>

                        <div v-if="item.routes && item.routes.length > 0" class="mt-2">
                          <div class="text-caption text-medium-emphasis mb-1">
                            Маршруты:
                          </div>
                          <v-chip
                            v-for="route in item.routes.slice(0, 3)"
                            :key="route.id"
                            size="small"
                            class="mr-1 mb-1"
                            color="blue-lighten-4"
                          >
                            {{ route.number }}
                          </v-chip>
                          <span v-if="item.routes.length > 3" class="text-caption">
                            +{{ item.routes.length - 3 }} ещё
                          </span>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </div>
    </v-expand-transition>

    <!-- Таблица типов -->
    <v-card elevation="2">
      <v-data-table
        :headers="headers"
        :items="filteredTypes"
        :loading="loading"
        :search="search"
        class="elevation-1"
      >
        <!-- Заголовок таблицы -->
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Список типов автобусов</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>
            <v-chip color="green" variant="tonal">
              Всего: {{ busTypes.length }}
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

        <!-- Колонка названия -->
        <template v-slot:item.name="{ item }">
          <div class="d-flex align-center">
            <v-avatar :color="getTypeColor(item.name)" size="36" class="mr-3">
              <v-icon icon="mdi-bus" color="white"></v-icon>
            </v-avatar>
            <div>
              <strong>{{ item.name }}</strong>
              <div class="text-caption text-medium-emphasis">
                ID: {{ item.id }}
              </div>
            </div>
          </div>
        </template>

        <!-- Колонка вместимости -->
        <template v-slot:item.capacity="{ item }">
          <div class="d-flex align-center">
            <v-icon icon="mdi-account-group" color="blue" class="mr-2"></v-icon>
            <div>
              <div class="text-subtitle-1 font-weight-bold">{{ item.capacity }}</div>
              <div class="text-caption text-medium-emphasis">пассажиров</div>
            </div>
          </div>
        </template>

        <!-- Колонка количества автобусов -->
        <template v-slot:item.bus_count="{ item }">
          <v-chip :color="getBusCountColor(item.bus_count)" variant="flat">
            {{ item.bus_count || 0 }}
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
              @click="viewType(item)"
              title="Просмотр"
            ></v-btn>
            <v-btn
              icon="mdi-pencil"
              size="small"
              color="warning"
              variant="text"
              @click="editType(item)"
              title="Редактировать"
            ></v-btn>
            <v-btn
              icon="mdi-delete"
              size="small"
              color="error"
              variant="text"
              @click="deleteType(item)"
              title="Удалить"
              :disabled="isTypeInUse(item.id)"
            ></v-btn>
          </div>
        </template>

        <!-- Пустая таблица -->
        <template v-slot:no-data>
          <v-alert type="info" variant="tonal" class="ma-4">
            Нет данных о типах автобусов. Нажмите "Добавить тип", чтобы создать первый.
          </v-alert>
        </template>
      </v-data-table>
    </v-card>

    <!-- Диалог создания/редактирования -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">
          <v-icon :icon="editMode ? 'mdi-pencil' : 'mdi-plus-circle'" class="mr-2"></v-icon>
          {{ editMode ? 'Редактирование типа' : 'Новый тип автобуса' }}
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="localForm.name"
                  label="Название типа*"
                  required
                  variant="outlined"
                  :rules="[v => !!v || 'Название обязательно']"
                  hint="Пример: Городской, Пригородный, Туристический"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-text-field
                  v-model.number="localForm.capacity"
                  label="Вместимость (пассажиров)*"
                  type="number"
                  required
                  variant="outlined"
                  :rules="[
                    v => !!v || 'Вместимость обязательна',
                    v => v > 0 || 'Вместимость должна быть больше 0',
                    v => v <= 200 || 'Вместимость не может превышать 200'
                  ]"
                  hint="Максимальное количество пассажиров"
                ></v-text-field>
              </v-col>

              <v-col v-if="editMode && localForm.bus_count > 0" cols="12">
                <v-alert type="info" variant="tonal">
                  <template v-slot:title>
                    <strong>Автобусов этого типа:</strong> {{ localForm.bus_count }}
                  </template>
                  Нельзя удалить тип, если к нему привязаны автобусы
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
          <v-btn color="primary" variant="flat" @click="saveType" :loading="saving">
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
          <template v-if="isTypeInUse(typeToDelete?.id)">
            <v-alert type="warning" variant="tonal" class="mb-4">
              Этот тип используется {{ getBusCountForType(typeToDelete?.id) }} автобусами!
            </v-alert>
            <p>
              Вы не можете удалить тип <strong>{{ typeToDelete?.name }}</strong>,
              так как он назначен автобусам.
            </p>
            <p class="text-error">
              Сначала измените тип у всех автобусов, затем повторите попытку.
            </p>
          </template>
          <template v-else>
            <p>
              Вы уверены, что хотите удалить тип
              <strong>{{ typeToDelete?.name }}</strong>?
            </p>
            <p class="text-error">
              Это действие нельзя отменить!
            </p>
          </template>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="deleteDialog = false">
            Отмена
          </v-btn>
          <v-btn
            v-if="!isTypeInUse(typeToDelete?.id)"
            color="error"
            variant="flat"
            @click="confirmDelete"
            :loading="deleting"
          >
            Удалить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог просмотра -->
    <v-dialog v-model="viewDialog" max-width="600px">
      <v-card v-if="viewingType">
        <v-card-title class="text-h5">
          <v-icon icon="mdi-bus" class="mr-2"></v-icon>
          Информация о типе автобуса
        </v-card-title>

        <v-card-text>
          <v-row class="mb-4">
            <v-col cols="12" class="text-center">
              <v-avatar :color="getTypeColor(viewingType.name)" size="120">
                <v-icon icon="mdi-bus" size="x-large" color="white"></v-icon>
              </v-avatar>
              <h2 class="mt-4">{{ viewingType.name }}</h2>
              <v-chip color="grey" variant="outlined" class="mt-2">
                ID: {{ viewingType.id }}
              </v-chip>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <v-row>
            <v-col cols="12" md="6">
              <v-list density="compact">
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-account-group"></v-icon>
                  </template>
                  <v-list-item-title>Вместимость</v-list-item-title>
                  <v-list-item-subtitle>
                    <span class="text-h6 text-blue">
                      {{ viewingType.capacity }} пассажиров
                    </span>
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-bus-multiple"></v-icon>
                  </template>
                  <v-list-item-title>Количество автобусов</v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip :color="getBusCountColor(viewingType.bus_count)" size="small">
                      {{ viewingType.bus_count || 0 }}
                    </v-chip>
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>

            <v-col cols="12" md="6">
              <v-list density="compact">
                <v-list-item v-if="viewingType.total_route_duration">
                  <template v-slot:prepend>
                    <v-icon icon="mdi-clock-outline"></v-icon>
                  </template>
                  <v-list-item-title>Общая протяженность маршрутов</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ formatDuration(viewingType.total_route_duration) }}
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item v-if="viewingType.drivers_avg_experience">
                  <template v-slot:prepend>
                    <v-icon icon="mdi-account-clock"></v-icon>
                  </template>
                  <v-list-item-title>Средний стаж водителей</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ viewingType.drivers_avg_experience.toFixed(1) }} лет
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>

          <!-- Маршруты этого типа -->
          <v-row v-if="viewingType.routes && viewingType.routes.length > 0">
            <v-col cols="12">
              <v-divider class="my-4"></v-divider>
              <v-card variant="tonal" color="info">
                <v-card-title class="text-h6">
                  <v-icon icon="mdi-map-marker-path" class="mr-2"></v-icon>
                  Маршруты этого типа ({{ viewingType.routes.length }})
                </v-card-title>
                <v-card-text>
                  <div class="d-flex flex-wrap gap-2">
                    <v-chip
                      v-for="route in viewingType.routes"
                      :key="route.id"
                      color="blue-lighten-4"
                      :prepend-icon="routeIcon(route)"
                    >
                      {{ route.number }}: {{ route.start_point }} → {{ route.end_point }}
                    </v-chip>
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
          <v-btn color="warning" variant="text" @click="editType(viewingType)">
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
    const busTypes = ref([])
    const buses = ref([]) // Для проверки использования типов
    const report = ref([])
    const loading = ref(false)
    const loadingReport = ref(false)
    const saving = ref(false)
    const deleting = ref(false)
    const dialog = ref(false)
    const deleteDialog = ref(false)
    const viewDialog = ref(false)
    const showReport = ref(false)
    const editMode = ref(false)
    const search = ref('')

    // Локальная форма для диалога
    const localForm = reactive({
      id: null,
      name: '',
      capacity: 30,
      bus_count: 0
    })

    // Для удаления и просмотра
    const typeToDelete = ref(null)
    const viewingType = ref(null)

    // Уведомления
    const snackbar = reactive({
      show: false,
      message: '',
      color: 'success'
    })

    // Заголовки таблицы БЕЗ сортировки
    const headers = ref([
      { title: 'ID', key: 'id', sortable: false, width: '80px' },
      { title: 'Тип автобуса', key: 'name', sortable: false },
      { title: 'Вместимость', key: 'capacity', sortable: false, width: '120px' },
      { title: 'Автобусов', key: 'bus_count', sortable: false, width: '100px' },
      { title: 'Действия', key: 'actions', sortable: false, width: '150px', align: 'center' }
    ])

    // Отфильтрованные типы
    const filteredTypes = computed(() => {
      if (!search.value) {
        return busTypes.value
      }

      const searchLower = search.value.toLowerCase()
      return busTypes.value.filter(type =>
        type.name.toLowerCase().includes(searchLower) ||
        type.capacity.toString().includes(searchLower)
      )
    })

    // Вспомогательные функции
    const formatCurrency = (value) => {
      if (!value) return '0 ₽'
      return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
        minimumFractionDigits: 0
      }).format(value)
    }

    const formatDuration = (minutes) => {
      if (!minutes) return '0 мин'
      const hours = Math.floor(minutes / 60)
      const mins = minutes % 60

      if (hours === 0) return `${mins} мин`
      if (mins === 0) return `${hours} ч`
      return `${hours} ч ${mins} мин`
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

    const getBusCountColor = (count) => {
      if (!count || count === 0) return 'grey'
      if (count <= 5) return 'orange'
      if (count <= 15) return 'blue'
      return 'green'
    }

    const routeIcon = (route) => {
      if (route.number.includes('Э')) return 'mdi-lightning-bolt'
      if (route.number.includes('А')) return 'mdi-airplane'
      return 'mdi-bus'
    }

    const isTypeInUse = (typeId) => {
      if (!typeId || !buses.value.length) return false
      return buses.value.some(bus => bus.bus_type?.id === typeId)
    }

    const getBusCountForType = (typeId) => {
      if (!typeId || !buses.value.length) return 0
      return buses.value.filter(bus => bus.bus_type?.id === typeId).length
    }

    // API функции
    const fetchBusTypes = async () => {
      loading.value = true
      try {
        const response = await apiClient.get('bus-types/')
        // Добавляем количество автобусов для каждого типа
        const typesWithCounts = await Promise.all(
          response.data.map(async (type) => {
            try {
              const busesRes = await apiClient.get(`buses/?bus_type=${type.id}`)
              return {
                ...type,
                bus_count: busesRes.data.length
              }
            } catch (error) {
              console.error(`Ошибка загрузки автобусов для типа ${type.id}:`, error)
              return { ...type, bus_count: 0 }
            }
          })
        )
        busTypes.value = typesWithCounts
      } catch (error) {
        console.error('Ошибка загрузки типов:', error)
        showSnackbar('Ошибка загрузки данных', 'error')
      } finally {
        loading.value = false
      }
    }

    const fetchBuses = async () => {
      try {
        const response = await apiClient.get('buses/')
        buses.value = response.data
      } catch (error) {
        console.error('Ошибка загрузки автобусов:', error)
      }
    }

    const fetchReport = async () => {
      loadingReport.value = true
      try {
        const response = await apiClient.get('bus-types/report/')
        report.value = response.data

        // Обновляем данные в busTypes из отчета
        if (report.value.length > 0) {
          busTypes.value = busTypes.value.map(type => {
            const reportData = report.value.find(r => r.bus_type === type.name)
            if (reportData) {
              return {
                ...type,
                bus_count: reportData.bus_count,
                routes: reportData.routes,
                total_route_duration: reportData.total_route_duration,
                drivers_avg_experience: reportData.drivers_avg_experience
              }
            }
            return type
          })
        }
      } catch (error) {
        console.error('Ошибка загрузки отчета:', error)
        // Если endpoint не работает, скрываем кнопку отчета
        showReport.value = false
      } finally {
        loadingReport.value = false
      }
    }

    // CRUD операции
    const openCreateDialog = () => {
      editMode.value = false
      resetForm()
      dialog.value = true
    }

    const editType = (type) => {
      editMode.value = true
      localForm.id = type.id
      localForm.name = type.name || ''
      localForm.capacity = type.capacity || 30
      localForm.bus_count = type.bus_count || 0

      dialog.value = true
    }

    const viewType = (type) => {
      // Находим полные данные из отчета
      const reportData = report.value.find(r => r.bus_type === type.name)
      viewingType.value = {
        ...type,
        ...reportData
      }
      viewDialog.value = true
    }

    const saveType = async () => {
      // Простая валидация
      if (!localForm.name.trim()) {
        showSnackbar('Введите название типа', 'error')
        return
      }
      if (!localForm.capacity || localForm.capacity <= 0) {
        showSnackbar('Введите корректную вместимость', 'error')
        return
      }

      saving.value = true
      try {
        const typeData = {
          name: localForm.name.trim(),
          capacity: Number(localForm.capacity)
        }

        if (editMode.value) {
          await apiClient.put(`bus-types/${localForm.id}/`, typeData)
          showSnackbar('Тип успешно обновлен', 'success')
        } else {
          await apiClient.post('bus-types/', typeData)
          showSnackbar('Тип успешно создан', 'success')
        }

        await Promise.all([
          fetchBusTypes(),
          fetchReport()
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

    const deleteType = (type) => {
      typeToDelete.value = type
      deleteDialog.value = true
    }

    const confirmDelete = async () => {
      if (!typeToDelete.value) return

      if (isTypeInUse(typeToDelete.value.id)) {
        showSnackbar('Невозможно удалить тип, который используется автобусами', 'error')
        deleteDialog.value = false
        return
      }

      deleting.value = true
      try {
        await apiClient.delete(`bus-types/${typeToDelete.value.id}/`)

        showSnackbar('Тип успешно удален', 'success')
        await Promise.all([
          fetchBusTypes(),
          fetchReport()
        ])
      } catch (error) {
        console.error('Ошибка удаления:', error)
        showSnackbar('Ошибка удаления', 'error')
      } finally {
        deleting.value = false
        deleteDialog.value = false
        typeToDelete.value = null
      }
    }

    const closeDialog = () => {
      dialog.value = false
      resetForm()
    }

    const resetForm = () => {
      localForm.id = null
      localForm.name = ''
      localForm.capacity = 30
      localForm.bus_count = 0
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
        fetchBusTypes(),
        fetchBuses(),
        fetchReport()
      ])
    })

    return {
      // Состояние
      busTypes,
      buses,
      report,
      loading,
      loadingReport,
      saving,
      deleting,
      dialog,
      deleteDialog,
      viewDialog,
      showReport,
      editMode,
      search,
      localForm,
      typeToDelete,
      viewingType,
      snackbar,

      // Данные таблицы
      headers,
      filteredTypes,

      // Методы
      fetchBusTypes,
      fetchReport,
      openCreateDialog,
      editType,
      viewType,
      saveType,
      deleteType,
      confirmDelete,
      closeDialog,

      // Вспомогательные методы
      formatCurrency,
      formatDuration,
      getTypeColor,
      getBusCountColor,
      routeIcon,
      isTypeInUse,
      getBusCountForType,
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

.text-blue {
  color: #2196F3;
}

/* Стили для отчета */
.gap-2 {
  gap: 8px;
}

/* Анимация для карточек отчета */
.v-card {
  transition: transform 0.3s ease;
}

.v-card:hover {
  transform: translateY(-5px);
}

/* Стили для чипов маршрутов */
.v-chip {
  transition: all 0.2s;
}

.v-chip:hover {
  transform: scale(1.05);
}
</style>
