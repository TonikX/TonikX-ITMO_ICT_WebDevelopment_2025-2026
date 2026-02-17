<script setup>
/**
 * RoomsView.vue - Страница управления номерным фондом.
 * Позволяет просматривать список номеров, изменять их статус,
 * редактировать данные и создавать новые комнаты.
 */
import { ref, onMounted, computed } from 'vue'
import api from '../services/api'

// --- Реактивное состояние ---
const rooms = ref([])       // Список всех комнат
const roomTypes = ref([])   // Справочник типов (для селекта)
const floors = ref([])      // Справочник этажей (для селекта)
const loading = ref(true)   // Индикатор загрузки данных
const search = ref('')      // Строка поиска в таблице

// Состояние диалоговых окон
const dialog = ref(false)
const deleteDialog = ref(false)
const editedIndex = ref(-1)

// Названия статусов для отображения в интерфейсе (маппинг)
const statusMap = {
    'free': 'Свободен',
    'occupied': 'Занят',
    'maintenance': 'На обслуживании'
}

// Список опций для выпадающего списка (v-select)
const statusOptions = [
    { title: 'Свободен', value: 'free' },
    { title: 'Занят', value: 'occupied' },
    { title: 'На обслуживании', value: 'maintenance' }
]


// Начальные данные для формы
const defaultItem = {
    number: '',
    room_type: null,
    floor: null,
    phone: '',
    status: 'free',
}
const editedItem = ref({ ...defaultItem })
const itemToDelete = ref(null)


// --- Валидация ---
const valid = ref(false)
const form = ref(null)

// Правило: Номер комнаты должен начинаться с цифры выбранного этажа
const numberRules = [
    (v) => !!v || 'Номер обязателен',
    (v) => {
        if (!editedItem.value.floor) return true

        let floorNum = ''
        if (typeof editedItem.value.floor === 'object' && editedItem.value.floor) {
            floorNum = String(editedItem.value.floor.number)
        } else {
            // Если в модели floor хранится ID, ищем соответствующий объект этажа
            const f = floors.value.find((f) => f.id === editedItem.value.floor)
            if (f) floorNum = String(f.number)
        }

        if (floorNum && !v.startsWith(floorNum)) {
            return `На ${floorNum} этаже номер должен начинаться с "${floorNum}"`
        }
        return true
    },
]

const formTitle = computed(() => {
    return editedIndex.value === -1 ? 'Новый номер' : 'Редактировать номер'
})

const headers = [
    { title: 'Номер', key: 'number', align: 'start' },
    { title: 'Тип', key: 'room_type_details.name' },
    { title: 'Вместимость', key: 'room_type_details.max_guests' },
    { title: 'Этаж', key: 'floor' },
    { title: 'Статус', key: 'status' },
    { title: 'Цена', key: 'room_type_details.price' },
    { title: 'Действия', key: 'actions', sortable: false },
]

/**
 * Загрузка всех необходимых данных с сервера.
 * Справочники грузятся отдельно, чтобы ошибка в одном не блокировала остальные.
 */
async function fetchData() {
    loading.value = true
    // Загрузка комнат
    try {
        const rRes = await api.get('/api/rooms/')
        rooms.value = rRes.data
    } catch (e) {
        console.error('Ошибка загрузки комнат:', e)
    }

    // Загрузка типов
    try {
        const rtRes = await api.get('/api/room-types/')
        roomTypes.value = rtRes.data
    } catch (e) {
        console.error('Ошибка загрузки типов:', e)
    }

    // Загрузка этажей
    try {
        const fRes = await api.get('/api/floors/')
        floors.value = fRes.data
    } catch (e) {
        console.error('Ошибка загрузки этажей:', e)
    }

    loading.value = false
}

/**
 * Сохранение данных (Создание или Обновление).
 */
async function save() {
    const { valid } = await form.value.validate()
    if (!valid) return

    try {
        const payload = { ...editedItem.value }

        // Удаляем вложенные детали, так как сервер ожидает только ID в полях FK
        if (payload.room_type_details) delete payload.room_type_details
        if (payload.floor_details) delete payload.floor_details

        // Гарантируем, что на сервер уйдет ID этажа
        if (typeof payload.floor === 'object' && payload.floor !== null) {
            payload.floor = payload.floor.id || payload.floor.number
        }

        if (editedIndex.value > -1) {
            await api.put(`/api/rooms/${editedItem.value.id}/`, payload)
        } else {
            await api.post('/api/rooms/', payload)
        }
        close()
        fetchData()
    } catch (e) {
        const errorMsg = e.response?.data ? JSON.stringify(e.response.data) : e.message
        alert('Ошибка при сохранении: ' + errorMsg)
    }
}

/**
 * Подтверждение удаления комнаты.
 */
async function deleteItemConfirm() {
    try {
        await api.delete(`/api/rooms/${itemToDelete.value.id}/`)
        fetchData()
    } catch (e) {
        alert('Не удалось удалить номер. Возможно, в нем есть активные бронирования.')
    }
    closeDelete()
}

/**
 * Открытие диалога редактирования и подготовка данных.
 */
function editItem(item) {
    editedIndex.value = rooms.value.indexOf(item)
    editedItem.value = Object.assign({}, item)
    // Приводим ID этажа к плоскому виду для корректной работы v-select
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

function getStatusColor(status) {
    if (status === 'free') return 'success'
    if (status === 'occupied') return 'error'
    return 'warning'
}

onMounted(fetchData)
</script>

<template>
    <v-container>
        <!-- Основная таблица данных -->
        <v-data-table :headers="headers" :items="rooms" :search="search" :loading="loading" class="elevation-1">
            <template v-slot:top>
                <v-toolbar flat>
                    <v-toolbar-title>Управление номерами</v-toolbar-title>
                    <v-divider class="mx-4" inset vertical></v-divider>
                    <v-spacer></v-spacer>

                    <v-text-field v-model="search" density="compact" label="Поиск" single-line hide-details
                        variant="outlined" class="mr-4" style="max-width: 300px"></v-text-field>

                    <!-- Кнопка добавления -->
                    <v-btn color="indigo-darken-2" variant="flat" prepend-icon="mdi-door" @click="dialog = true">
                        Создать номер
                    </v-btn>

                    <!-- Модальное окно Создания/Редактирования -->
                    <v-dialog v-model="dialog" max-width="500px">
                        <v-card>
                            <v-card-title class="bg-indigo-darken-3 text-white pa-4">
                                <span class="text-h5">{{ formTitle }}</span>
                            </v-card-title>
                            <v-card-text>
                                <v-container>
                                    <v-form ref="form" v-model="valid" @submit.prevent="save">
                                        <v-row>
                                            <v-col cols="12" sm="6">
                                                <v-text-field v-model="editedItem.number" label="Номер комнаты"
                                                    variant="outlined" prepend-inner-icon="mdi-door"
                                                    :rules="numberRules" required></v-text-field>
                                            </v-col>
                                            <v-col cols="12" sm="6">
                                                <v-select v-model="editedItem.status" :items="statusOptions"
                                                    item-title="title" item-value="value" label="Статус"
                                                    variant="outlined"></v-select>
                                            </v-col>
                                            <v-col cols="12">
                                                <v-select v-model="editedItem.room_type" :items="roomTypes"
                                                    item-title="name" item-value="id" label="Тип номера"
                                                    variant="outlined" prepend-inner-icon="mdi-bed">
                                                    <template v-slot:item="{ props, item }">
                                                        <v-list-item v-bind="props"
                                                            :subtitle="item.raw.price + ' руб./сутки'"></v-list-item>
                                                    </template>
                                                </v-select>
                                            </v-col>
                                            <v-col cols="12" sm="6">
                                                <v-select v-model="editedItem.floor" :items="floors" item-title="number"
                                                    item-value="id" label="Этаж" variant="outlined"
                                                    prepend-inner-icon="mdi-layers"></v-select>
                                            </v-col>
                                            <v-col cols="12" sm="6">
                                                <v-text-field v-model="editedItem.phone" label="Телефон"
                                                    variant="outlined" prepend-inner-icon="mdi-phone"></v-text-field>
                                            </v-col>
                                        </v-row>
                                    </v-form>
                                </v-container>
                            </v-card-text>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="blue-darken-1" variant="text" @click="close">Отмена</v-btn>
                                <v-btn color="blue-darken-1" variant="text" @click="save">Сохранить</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>

                    <!-- Модальное окно подтверждения удаления -->
                    <v-dialog v-model="deleteDialog" max-width="400px">
                        <v-card>
                            <v-card-title class="text-h6 text-center pa-4">Вы уверены?</v-card-title>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="blue-darken-1" variant="text" @click="closeDelete">Нет</v-btn>
                                <v-btn color="red-darken-1" variant="text" @click="deleteItemConfirm">Да,
                                    удалить</v-btn>
                                <v-spacer></v-spacer>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </v-toolbar>
            </template>

            <!-- Слот для красивого отображения статуса -->
            <template v-slot:item.status="{ item }">
                <v-chip :color="getStatusColor(item.status)" size="small">
                    {{ statusMap[item.status] }}
                </v-chip>
            </template>

            <!-- Слот для форматирования цены -->
            <template v-slot:item.room_type_details.price="{ item }">
                {{ item.room_type_details?.price }} ₽
            </template>

            <!-- Слот для отображения этажа (номер вместо ID) -->
            <template v-slot:item.floor="{ item }">
                {{ item.floor_details ? item.floor_details.number : item.floor }} этаж
            </template>

            <!-- Слот для кнопок действий -->
            <template v-slot:item.actions="{ item }">
                <v-icon size="small" class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
                <v-icon size="small" color="error" @click="deleteItem(item)">mdi-delete</v-icon>
            </template>
        </v-data-table>
    </v-container>
</template>