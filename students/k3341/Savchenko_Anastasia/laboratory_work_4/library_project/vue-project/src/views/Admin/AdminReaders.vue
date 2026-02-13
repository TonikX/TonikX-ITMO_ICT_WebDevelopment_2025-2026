<template>
  <div class="admin-readers">
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <div class="d-flex justify-space-between align-center mb-4">
            <h1 class="text-h4">Управление читателями</h1>
            <v-btn
              color="success"
              prepend-icon="mdi-account-plus"
              @click="goToRegister"
            >
              Зарегистрировать читателя
            </v-btn>
          </div>

          <v-card>
            <v-card-text>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="searchQuery"
                    label="Поиск читателя"
                    placeholder="Введите ФИО, номер билета или паспорт"
                    prepend-inner-icon="mdi-magnify"
                    clearable
                    density="comfortable"
                    variant="outlined"
                    hide-details
                    @keyup.enter="searchReaders"
                  ></v-text-field>
                </v-col>
              </v-row>

              <v-row class="mt-2">
                <v-col cols="12">
                  <v-btn color="primary" @click="searchReaders" :loading="loading" class="mr-2">
                    <v-icon left>mdi-magnify</v-icon>
                    Найти
                  </v-btn>
                  <v-btn variant="outlined" @click="resetSearch" class="mr-2">
                    Сбросить
                  </v-btn>
                  <v-btn
                    color="warning"
                    variant="outlined"
                    @click="removeInactive"
                    :loading="removingInactive"
                  >
                    <v-icon left>mdi-account-remove</v-icon>
                    Исключить неактивных
                  </v-btn>
                </v-col>
              </v-row>

              <v-divider class="my-4"></v-divider>

              <!-- Таблица читателей -->
              <v-data-table
                :headers="headers"
                :items="readers"
                :loading="loading"
                class="elevation-1"
              >
                <template v-slot:item.actions="{ item }">
                  <v-btn
                    icon="mdi-eye"
                    size="small"
                    color="primary"
                    variant="text"
                    @click="viewReader(item.reader_id)"
                  ></v-btn>
                  <v-btn
                    icon="mdi-pencil"
                    size="small"
                    color="warning"
                    variant="text"
                    @click="editReader(item.reader_id)"
                  ></v-btn>
                </template>

                <template v-slot:item.is_active_member="{ item }">
                  <v-chip
                    :color="item.is_active_member ? 'success' : 'error'"
                    size="small"
                  >
                    {{ item.is_active_member ? 'Активен' : 'Неактивен' }}
                  </v-chip>
                </template>

                <template v-slot:no-data>
                  <div class="text-center pa-4">
                    <v-icon size="48" color="grey-lighten-1">mdi-account-off</v-icon>
                    <p class="text-grey mt-2">Читатели не найдены</p>
                  </div>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Диалог редактирования -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card v-if="selectedReader">
        <v-card-title>
          <span class="text-h5">Редактирование читателя</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="selectedReader.full_name"
                  label="ФИО"
                  readonly
                  disabled
                  variant="outlined"
                  density="comfortable"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="selectedReader.library_card_id"
                  label="Номер билета"
                  readonly
                  disabled
                  variant="outlined"
                  density="comfortable"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="selectedReader.passport"
                  label="Паспорт"
                  readonly
                  disabled
                  variant="outlined"
                  density="comfortable"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="selectedReader.birth_date"
                  label="Дата рождения"
                  readonly
                  disabled
                  variant="outlined"
                  density="comfortable"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="selectedReader.education_level"
                  :items="educationLevels"
                  label="Образование"
                  readonly
                  disabled
                  variant="outlined"
                  density="comfortable"
                ></v-select>
              </v-col>
              <v-col cols="12">
                <v-divider class="my-2"></v-divider>
                <p class="text-subtitle-2 mb-2">Контактные данные (можно изменить)</p>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="editForm.phone_number"
                  label="Телефон"
                  variant="outlined"
                  density="comfortable"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="editForm.hall_id"
                  :items="halls"
                  item-title="name"
                  item-value="hall_id"
                  label="Зал"
                  variant="outlined"
                  density="comfortable"
                ></v-select>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="editForm.home_address"
                  label="Адрес"
                  rows="2"
                  variant="outlined"
                  density="comfortable"
                ></v-textarea>
              </v-col>
              <v-col cols="12">
                <v-switch
                  v-model="editForm.is_active_member"
                  label="Активный читатель"
                  color="success"
                ></v-switch>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="dialog = false">
            Отмена
          </v-btn>
          <v-btn color="primary" @click="saveReader" :loading="saving">
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../../api/client'

const router = useRouter()
const loading = ref(false)
const saving = ref(false)
const removingInactive = ref(false)
const readers = ref([])
const dialog = ref(false)
const selectedReader = ref(null)
const halls = ref([])
const searchQuery = ref('')

const editForm = reactive({
  phone_number: '',
  home_address: '',
  hall_id: null,
  is_active_member: true
})

const headers = [
  { title: '№ билета', key: 'library_card_id' },
  { title: 'ФИО', key: 'full_name' },
  { title: 'Телефон', key: 'phone_number' },
  {
    title: 'Зал',
    key: 'hall_name',
    value: (item) => {
      // Получаем название зала из halls по ID
      if (item.hall_id && halls.value.length > 0) {
        const hall = halls.value.find(h => h.hall_id === item.hall_id)
        return hall ? hall.name : 'Не указан'
      }
      return 'Не указан'
    }
  },
  { title: 'Статус', key: 'is_active_member' },
  { title: 'Действия', key: 'actions', sortable: false }
]

const educationLevels = [
  { title: 'Начальное', value: 'primary' },
  { title: 'Среднее', value: 'secondary' },
  { title: 'Высшее', value: 'higher' },
  { title: 'Ученая степень', value: 'degree' }
]

// Переход на страницу регистрации
const goToRegister = () => {
  router.push('/admin/readers/register')
}

// Загрузка читателей
const loadReaders = async () => {
  loading.value = true
  try {
    // Используем АДМИНСКИЙ эндпоинт, который показывает ВСЕХ
    const response = await apiClient.get('admin/readers/')
    readers.value = response.data
    console.log('Загружены читатели:', readers.value)
  } catch (error) {
    console.error('Ошибка загрузки читателей:', error)
    // Если админский эндпоинт не работает, используем обычный
    try {
      const fallbackResponse = await apiClient.get('readers/')
      readers.value = fallbackResponse.data
    } catch (e) {
      console.error('И обычный эндпоинт не работает:', e)
    }
  } finally {
    loading.value = false
  }
}

// Загрузка залов
const loadHalls = async () => {
  try {
    const response = await apiClient.get('halls/')
    halls.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки залов:', error)
  }
}

// Поиск читателей
const searchReaders = async () => {
  if (!searchQuery.value) {
    loadReaders()
    return
  }

  loading.value = true
  try {
    const response = await apiClient.get(`readers/?search=${searchQuery.value}`)
    readers.value = response.data
  } catch (error) {
    console.error('Ошибка поиска:', error)
  } finally {
    loading.value = false
  }
}

const resetSearch = () => {
  searchQuery.value = ''
  loadReaders()
}

// Просмотр читателя
const viewReader = (id) => {
  router.push(`/admin/readers/${id}`)
}

// Редактирование
const editReader = async (id) => {
  try {
    const response = await apiClient.get(`readers/${id}/`)
    selectedReader.value = response.data
    editForm.phone_number = response.data.phone_number || ''
    editForm.home_address = response.data.home_address || ''
    editForm.hall_id = response.data.hall_id
    editForm.is_active_member = response.data.is_active_member
    dialog.value = true
  } catch (error) {
    console.error('Ошибка загрузки читателя:', error)
  }
}

const saveReader = async () => {
  saving.value = true
  try {
    await apiClient.patch(`readers/${selectedReader.value.reader_id}/`, {
      phone_number: editForm.phone_number,
      home_address: editForm.home_address,
      hall_id: editForm.hall_id,
      is_active_member: editForm.is_active_member
    })
    dialog.value = false
    await loadReaders()
  } catch (error) {
    console.error('Ошибка сохранения:', error)
  } finally {
    saving.value = false
  }
}

// Исключение неактивных
const removeInactive = async () => {
  if (!confirm('Исключить читателей, не проходивших перерегистрацию более года?')) return

  removingInactive.value = true
  try {
    const response = await apiClient.post('readers/remove-inactive/')
    alert(`Исключено читателей: ${response.data.removed_readers?.length || 0}`)
    await loadReaders()
  } catch (error) {
    console.error('Ошибка:', error)
    alert('Ошибка при исключении читателей')
  } finally {
    removingInactive.value = false
  }
}

onMounted(() => {
  loadReaders()
  loadHalls()
})
</script>

<style scoped>
.admin-readers {
  width: 100%;
  min-height: 100%;
}

/* Минимальные стили - без конфликтов */
.v-container {
  padding: 20px !important;
}

.v-card {
  border-radius: 8px;
}

/* Адаптивность */
@media (max-width: 768px) {
  .v-container {
    padding: 10px !important;
  }
}
</style>