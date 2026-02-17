<script setup>
/**
 * SchedulesView.vue - Страница управления графиком уборки.
 * Основная задача: назначение сотрудников на уборку конкретных этажей по дням недели.
 * Включает в себя проверку на недопустимость назначения одного человека на два этажа в один день.
 */
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()

// --- Состояние данных ---
const schedules = ref([])  // Список назначенных смен
const employees = ref([])  // Список сотрудников для выбора
const floors = ref([])     // Список этажей для выбора
const loading = ref(true)  // Индикатор загрузки

// --- Управление диалогами ---
const dialog = ref(false)
const deleteDialog = ref(false)
const editedIndex = ref(-1)

// --- Валидация ---
const form = ref(null)
const valid = ref(false)

const defaultItem = { employee: null, day_of_week: null, floor: null }
const editedItem = ref({ ...defaultItem })
const itemToDelete = ref(null)

// Справочник дней недели
const days = [
    { title: 'Понедельник', value: 'mon' },
    { title: 'Вторник', value: 'tue' },
    { title: 'Среда', value: 'wed' },
    { title: 'Четверг', value: 'thu' },
    { title: 'Пятница', value: 'fri' },
    { title: 'Суббота', value: 'sat' },
    { title: 'Воскресенье', value: 'sun' },
]

// --- Правила валидации (Frontend-level) ---
const rules = {
    required: v => !!v || 'Обязательное поле',
    /**
     * Проверка уникальности: сотрудник не может убирать 
     * два разных этажа в один и тот же день.
     */
    unique: () => {
        if (!editedItem.value.employee || !editedItem.value.day_of_week) return true

        const duplicate = schedules.value.find(s =>
            s.employee === editedItem.value.employee &&
            s.day_of_week === editedItem.value.day_of_week &&
            s.id !== editedItem.value.id
        )

        if (duplicate) {
            let floorInfo = duplicate.floor
            if (duplicate.floor_details) {
                floorInfo = duplicate.floor_details.number
            } else {
                const f = floors.value.find(fl => fl.id === duplicate.floor)
                if (f) floorInfo = f.number
            }
            return `Сотрудник уже занят в этот день на ${floorInfo} этаже!`
        }
        return true
    }
}

const headers = [
    { title: 'Сотрудник', key: 'employee' },
    { title: 'День', key: 'day_display' },
    { title: 'Этаж', key: 'floor' },
    { title: 'Действия', key: 'actions', sortable: false },
]

/**
 * Загрузка всех необходимых данных.
 * Реализовано через Promise.all для ускорения инициализации страницы.
 */
async function fetchData() {
    loading.value = true
    try {
        const [schedRes, empRes, floorRes] = await Promise.all([
            api.get('/api/schedules/'),
            api.get('/api/employees/'),
            api.get('/api/floors/')
        ])
        schedules.value = schedRes.data
        employees.value = empRes.data
        floors.value = floorRes.data

        // Обработка перехода по быстрой кнопке с главной страницы
        if (route.query.new === 'true') {
            dialog.value = true
            router.replace({ query: null })
        }
    } catch (e) {
        console.error('Ошибка при загрузке данных графика:', e)
    } finally {
        loading.value = false
    }
}

/**
 * Поиск ФИО сотрудника по его ID для отображения в таблице.
 */
function getEmpName(id) {
    const emp = employees.value.find(e => e.id === id)
    return emp ? `${emp.last_name} ${emp.first_name}` : `ID: ${id}`
}

/**
 * Сохранение данных (Создание новой смены или изменение старой).
 */
async function save() {
    const { valid } = await form.value.validate()
    if (!valid) return

    try {
        const payload = { ...editedItem.value }

        // Предотвращение отправки объектов вместо ID (типичная проблема Vuetify)
        if (typeof payload.floor === 'object' && payload.floor !== null) {
            payload.floor = payload.floor.id
        }
        if (typeof payload.employee === 'object' && payload.employee !== null) {
            payload.employee = payload.employee.id
        }

        if (editedIndex.value > -1) {
            await api.put(`/api/schedules/${editedItem.value.id}/`, payload)
        } else {
            await api.post('/api/schedules/', payload)
        }
        close()
        fetchData()
    } catch (e) {
        const msg = e.response?.data?.non_field_errors || e.response?.data?.detail || 'Ошибка на стороне сервера.'
        alert('Ошибка сохранения: ' + JSON.stringify(msg))
    }
}

async function deleteItemConfirm() {
    try {
        await api.delete(`/api/schedules/${itemToDelete.value.id}/`)
        fetchData()
    } catch (e) {
        alert('Ошибка при удалении записи.')
    }
    closeDelete()
}

/**
 * Подготовка данных для редактирования (синхронизация ID этажа).
 */
function editItem(item) {
    editedIndex.value = schedules.value.indexOf(item)
    editedItem.value = Object.assign({}, item)

    // Обеспечиваем корректный выбор в селекте
    if (item.floor_details) {
        editedItem.value.floor = item.floor_details.id
    }
    dialog.value = true
}

function deleteItem(item) {
    itemToDelete.value = item
    deleteDialog.value = true
}

function close() {
    dialog.value = false
    editedItem.value = { ...defaultItem }
    editedIndex.value = -1
}

function closeDelete() {
    deleteDialog.value = false
    itemToDelete.value = null
}

onMounted(fetchData)
</script>

<template>
    <v-container>
        <v-data-table :headers="headers" :items="schedules" :loading="loading" class="elevation-1">
            <template v-slot:top>
                <v-toolbar flat color="white">
                    <v-toolbar-title class="font-weight-bold text-indigo">График уборки</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-btn color="indigo-darken-2" variant="flat" prepend-icon="mdi-calendar-plus"
                        @click="dialog = true">
                        Назначить смену
                    </v-btn>

                    <!-- Диалог назначения -->
                    <v-dialog v-model="dialog" max-width="500">
                        <v-card>
                            <v-card-title class="bg-indigo-darken-3 text-white pa-4">
                                <span class="text-h5">{{ editedIndex === -1 ? 'Назначить смену' : 'Редактировать смену'
                                    }}</span>
                            </v-card-title>

                            <v-card-text class="pt-6">
                                <v-form ref="form" v-model="valid" @submit.prevent="save">
                                    <v-select v-model="editedItem.employee" :items="employees" item-title="last_name"
                                        item-value="id" label="Сотрудник" variant="outlined"
                                        prepend-inner-icon="mdi-account"
                                        :rules="[rules.required, rules.unique]"></v-select>

                                    <v-select v-model="editedItem.day_of_week" :items="days" item-title="title"
                                        item-value="value" label="День недели" variant="outlined"
                                        prepend-inner-icon="mdi-calendar-range"
                                        :rules="[rules.required, rules.unique]"></v-select>

                                    <v-select v-model="editedItem.floor" :items="floors" item-title="number"
                                        item-value="id" label="Этаж" variant="outlined" prepend-inner-icon="mdi-layers"
                                        suffix="этаж" :rules="[rules.required]"></v-select>

                                    <div class="d-flex justify-end mt-4">
                                        <v-btn variant="text" @click="close" class="mr-2">Отмена</v-btn>
                                        <v-btn type="submit" color="indigo-darken-2" variant="flat">Сохранить</v-btn>
                                    </div>
                                </v-form>
                            </v-card-text>
                        </v-card>
                    </v-dialog>

                    <!-- Подтверждение удаления -->
                    <v-dialog v-model="deleteDialog" max-width="400px">
                        <v-card>
                            <v-card-title class="text-h6 text-center pa-4 text-error">Удалить смену из
                                графика?</v-card-title>
                            <v-card-actions class="justify-center pb-4">
                                <v-btn variant="text" @click="closeDelete">Отмена</v-btn>
                                <v-btn color="error" variant="flat" @click="deleteItemConfirm">Да, удалить</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </v-toolbar>
            </template>

            <!-- Кастомное отображение колонок -->
            <template v-slot:item.employee="{ item }">
                {{ getEmpName(item.employee) }}
            </template>

            <template v-slot:item.floor="{ item }">
                <v-chip size="small" variant="tonal" color="indigo">
                    {{ item.floor_details ? item.floor_details.number : item.floor }} этаж
                </v-chip>
            </template>

            <template v-slot:item.actions="{ item }">
                <v-icon size="small" class="mr-2" color="indigo" @click="editItem(item)">mdi-pencil</v-icon>
                <v-icon size="small" color="error" @click="deleteItem(item)">mdi-delete</v-icon>
            </template>
        </v-data-table>
    </v-container>
</template>