<script setup>
/**
 * BookingsView.vue - Журнал заселения (основной рабочий экран администратора).
 * Реализует сложную логику: 
 * 1. Бронирование номеров.
 * 2. Создание новых гостей "на лету" (вместе с новыми городами).
 * 3. Автоматический расчет стоимости на стороне клиента.
 * 4. Быстрое выселение (Check-out).
 */
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()

// --- Состояние данных ---
const bookings = ref([])
const rooms = ref([])
const guests = ref([])
const cities = ref([])
const loading = ref(true)
const error = ref('') // Для вывода ошибок валидации или сервера

// --- Управление интерфейсом ---
const dialog = ref(false)
const deleteDialog = ref(false)
const editedIndex = ref(-1)
const guestTab = ref(0) // 0 - выбор существующего, 1 - создание нового

const form = ref(null)
const valid = ref(false)

// Начальные значения для новой брони
const defaultItem = {
    room: null,
    guest: null,
    new_last_name: '',
    new_first_name: '',
    new_patronymic: '',
    new_passport: '',
    new_city: null,
    check_in: new Date().toISOString().substr(0, 10),
    check_out: new Date(new Date().setDate(new Date().getDate() + 1)).toISOString().substr(0, 10),
    is_active: true
}

const editedItem = ref({ ...defaultItem })
const itemToDelete = ref(null)

// --- Валидация (Frontend-level) ---
const rules = {
    required: v => !!v || 'Это поле обязательно',
    dates: v => {
        const start = new Date(editedItem.value.check_in)
        const end = new Date(editedItem.value.check_out)
        return end > start || 'Дата выезда должна быть позже даты заезда'
    },
    roomStatus: v => {
        const room = rooms.value.find(r => r.id === v)
        if (room && room.status === 'maintenance') return 'Номер на ремонте!'
        return true
    }
}

const formTitle = computed(() => editedIndex.value === -1 ? 'Новое заселение' : 'Редактировать бронь')

// Получение объекта выбранной комнаты для доступа к цене
const selectedRoomData = computed(() => {
    return rooms.value.find(r => r.id === editedItem.value.room)
})

// Отображение тарифа
const priceLabel = computed(() => {
    if (selectedRoomData.value) {
        const price = selectedRoomData.value.room_type_details?.price
        return `Тариф: ${price} ₽/сутки`
    }
    return 'Выберите номер для расчета цены'
})

// Калькулятор итоговой суммы (работает мгновенно при смене дат или номера)
const estimatedCost = computed(() => {
    if (!selectedRoomData.value || !editedItem.value.check_in || !editedItem.value.check_out) return 0

    const start = new Date(editedItem.value.check_in)
    const end = new Date(editedItem.value.check_out)

    if (end <= start) return 0

    const diffTime = Math.abs(end - start)
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

    const price = Number(selectedRoomData.value.room_type_details?.price || 0)
    return diffDays * price
})

const headers = [
    { title: 'Гость', key: 'guest_details.last_name' },
    { title: 'Номер', key: 'room_details.number' },
    { title: 'Заезд', key: 'check_in' },
    { title: 'Выезд', key: 'check_out' },
    { title: 'Сумма', key: 'total_cost', align: 'end' },
    { title: 'Действия', key: 'actions', sortable: false, align: 'end' },
]

/**
 * Загрузка всех данных, необходимых для работы страницы.
 */
async function fetchData() {
    loading.value = true
    try {
        const [bRes, rRes, gRes, cRes] = await Promise.all([
            api.get('/api/bookings/'),
            api.get('/api/rooms/'),
            api.get('/api/guests/'),
            api.get('/api/cities/')
        ])
        bookings.value = bRes.data
        rooms.value = rRes.data
        guests.value = gRes.data
        cities.value = cRes.data

        // Если пришли с главной через "Быстрое действие", открываем окно
        if (route.query.new === 'true') {
            dialog.value = true
            router.replace({ query: null })
        }
    } catch (e) {
        console.error('Ошибка загрузки данных:', e)
    } finally {
        loading.value = false
    }
}

// Форматирование ФИО в списке выбора
function guestTitle(item) {
    const patronymic = item.patronymic ? ` ${item.patronymic}` : ''
    return `${item.last_name} ${item.first_name}${patronymic} (${item.passport})`
}

// Форматирование номера комнаты в списке
function roomTitle(item) {
    const type = item.room_type_details?.name || '?'
    const price = item.room_type_details?.price || 0
    const statusMap = { 'free': 'Свободен', 'occupied': 'Занят', 'maintenance': 'На обслуживании' }
    return `№${item.number} | ${statusMap[item.status]} | ${type} (${price}₽)`
}

/**
 * Главный метод сохранения.
 * Выполняет цепочку действий, если выбран вкладка "Новый гость".
 */
async function save() {
    error.value = ''
    const { valid } = await form.value.validate()
    if (!valid) return

    try {
        let finalGuestId = editedItem.value.guest

        // ШАГ 1: Если гость новый, создаем его
        if (guestTab.value === 1 && editedIndex.value === -1) {
            let cityId = editedItem.value.new_city

            // Если город введен текстом в combobox — создаем город
            if (typeof cityId === 'string' && cityId.trim() !== '') {
                const cityRes = await api.post('/api/cities/', { name: cityId })
                cityId = cityRes.data.id
            } else if (cityId && typeof cityId === 'object') {
                cityId = cityId.id
            }

            const guestPayload = {
                last_name: editedItem.value.new_last_name,
                first_name: editedItem.value.new_first_name,
                patronymic: editedItem.value.new_patronymic,
                passport: editedItem.value.new_passport,
                city: cityId
            }
            const guestRes = await api.post('/api/guests/', guestPayload)
            finalGuestId = guestRes.data.id
        }

        // ШАГ 2: Сохраняем бронирование
        const payload = {
            room: editedItem.value.room,
            guest: finalGuestId,
            check_in: editedItem.value.check_in,
            check_out: editedItem.value.check_out,
            is_active: editedItem.value.is_active
        }

        // Нормализация ID комнаты
        if (typeof payload.room === 'object' && payload.room) payload.room = payload.room.id

        if (editedIndex.value > -1) {
            await api.put(`/api/bookings/${editedItem.value.id}/`, payload)
        } else {
            await api.post('/api/bookings/', payload)
        }

        close()
        fetchData()
    } catch (e) {
        // Показываем ошибку от бэкенда (например, нарушение clean() в модели)
        const msg = e.response?.data?.non_field_errors || e.response?.data || 'Ошибка сервера'
        error.value = Array.isArray(msg) ? msg.join(', ') : JSON.stringify(msg)
    }
}

async function deleteItemConfirm() {
    try {
        await api.delete(`/api/bookings/${itemToDelete.value.id}/`)
        fetchData()
    } catch (e) { alert('Ошибка удаления') }
    closeDelete()
}

/**
 * Быстрое выселение: установка статуса "неактивно" и даты выезда на сегодня.
 */
async function checkOut(item) {
    if (!confirm(`Выселить гостя ${item.guest_details.last_name} сегодня?`)) return

    try {
        const today = new Date().toISOString().substr(0, 10)
        await api.patch(`/api/bookings/${item.id}/`, {
            check_out: today,
            is_active: false
        })
        fetchData()
    } catch (e) {
        alert('Ошибка при выселении: ' + JSON.stringify(e.response?.data))
    }
}

function editItem(item) {
    editedIndex.value = bookings.value.indexOf(item)
    editedItem.value = Object.assign({}, item)

    if (editedItem.value.room_details) editedItem.value.room = editedItem.value.room_details.id
    if (editedItem.value.guest_details) editedItem.value.guest = editedItem.value.guest_details.id

    guestTab.value = 0
    dialog.value = true
}

function deleteItem(item) { itemToDelete.value = item; deleteDialog.value = true }

function close() {
    dialog.value = false
    error.value = ''
    editedIndex.value = -1
    resetForm()
}

function closeDelete() { deleteDialog.value = false }

function resetForm() {
    editedItem.value = {
        ...defaultItem,
        check_in: new Date().toISOString().substr(0, 10),
        check_out: new Date(new Date().setDate(new Date().getDate() + 1)).toISOString().substr(0, 10)
    }
}

onMounted(fetchData)
</script>

<template>
    <v-container>
        <v-data-table :headers="headers" :items="bookings" :loading="loading" class="elevation-1">
            <template v-slot:top>
                <v-toolbar flat color="white">
                    <v-toolbar-title class="font-weight-bold text-indigo">Журнал заселения</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-btn color="indigo-darken-2" variant="flat" prepend-icon="mdi-key" @click="dialog = true">
                        Заселить гостя
                    </v-btn>

                    <!-- МОДАЛЬНОЕ ОКНО ЗАСЕЛЕНИЯ -->
                    <v-dialog v-model="dialog" max-width="800px" persistent>
                        <v-card>
                            <v-card-title class="bg-indigo-darken-3 text-white pa-4">
                                <span class="text-h5">{{ formTitle }}</span>
                            </v-card-title>

                            <v-card-text class="pa-4">
                                <v-form ref="form" v-model="valid" @submit.prevent="save">
                                    <v-row>
                                        <!-- Выбор номера -->
                                        <v-col cols="12">
                                            <v-autocomplete v-model="editedItem.room" :items="rooms"
                                                :item-title="roomTitle" item-value="id" label="Выберите номер"
                                                variant="outlined" prepend-inner-icon="mdi-door"
                                                :rules="[rules.required, rules.roomStatus]">
                                                <template v-slot:item="{ props, item }">
                                                    <v-list-item v-bind="props"
                                                        :base-color="item.raw.status === 'free' ? '' : 'error'">
                                                        <template v-slot:append>
                                                            <v-chip size="x-small" v-if="item.raw.status === 'occupied'"
                                                                color="warning">Занят</v-chip>
                                                            <v-chip size="x-small"
                                                                v-if="item.raw.status === 'maintenance'"
                                                                color="warning">На обслуживании</v-chip>
                                                        </template>
                                                    </v-list-item>
                                                </template>
                                            </v-autocomplete>
                                        </v-col>

                                        <!-- Выбор гостя -->
                                        <v-col cols="12" v-if="editedIndex === -1">
                                            <v-tabs v-model="guestTab" color="indigo" align-tabs="center" class="mb-4">
                                                <v-tab :value="0">Выбрать из базы</v-tab>
                                                <v-tab :value="1">Новый гость</v-tab>
                                            </v-tabs>

                                            <v-window v-model="guestTab">
                                                <!-- Существующий гость -->
                                                <v-window-item :value="0">
                                                    <v-autocomplete v-model="editedItem.guest" :items="guests"
                                                        :item-title="guestTitle" item-value="id" label="Поиск гостя"
                                                        variant="outlined" prepend-inner-icon="mdi-account-search"
                                                        :rules="guestTab === 0 ? [rules.required] : []"></v-autocomplete>
                                                </v-window-item>

                                                <!-- Регистрация нового гостя -->
                                                <v-window-item :value="1">
                                                    <v-row dense>
                                                        <v-col cols="4"><v-text-field v-model="editedItem.new_last_name"
                                                                label="Фамилия" variant="outlined" density="compact"
                                                                :rules="guestTab === 1 ? [rules.required] : []"></v-text-field></v-col>
                                                        <v-col cols="4"><v-text-field
                                                                v-model="editedItem.new_first_name" label="Имя"
                                                                variant="outlined" density="compact"
                                                                :rules="guestTab === 1 ? [rules.required] : []"></v-text-field></v-col>
                                                        <v-col cols="4"><v-text-field
                                                                v-model="editedItem.new_patronymic" label="Отчество"
                                                                variant="outlined"
                                                                density="compact"></v-text-field></v-col>
                                                        <v-col cols="6"><v-text-field v-model="editedItem.new_passport"
                                                                label="Паспорт" variant="outlined" density="compact"
                                                                prepend-inner-icon="mdi-card-account-details"
                                                                :rules="guestTab === 1 ? [rules.required] : []"></v-text-field></v-col>
                                                        <v-col cols="6">
                                                            <v-combobox v-model="editedItem.new_city" :items="cities"
                                                                item-title="name" item-value="id" label="Город"
                                                                variant="outlined" density="compact"
                                                                prepend-inner-icon="mdi-city"
                                                                :rules="guestTab === 1 ? [rules.required] : []"></v-combobox>
                                                        </v-col>
                                                    </v-row>
                                                </v-window-item>
                                            </v-window>
                                        </v-col>

                                        <v-col cols="12" v-else>
                                            <v-text-field :model-value="guestTitle(editedItem.guest_details)"
                                                label="Гость" variant="outlined" readonly></v-text-field>
                                        </v-col>

                                        <!-- Даты проживания -->
                                        <v-col cols="6">
                                            <v-text-field v-model="editedItem.check_in" type="date" label="Дата заезда"
                                                variant="outlined" :rules="[rules.required]"></v-text-field>
                                        </v-col>
                                        <v-col cols="6">
                                            <v-text-field v-model="editedItem.check_out" type="date" label="Дата выезда"
                                                variant="outlined"
                                                :rules="[rules.required, rules.dates]"></v-text-field>
                                        </v-col>

                                        <!-- Калькулятор цены -->
                                        <v-col cols="12">
                                            <v-card color="indigo-lighten-5" flat
                                                class="pa-4 text-center rounded-lg border-dashed">
                                                <div class="text-subtitle-2 text-grey-darken-1">Итого к оплате</div>
                                                <div class="text-h4 font-weight-bold text-indigo-darken-4 my-1">
                                                    {{ estimatedCost }} ₽
                                                </div>
                                                <div class="text-caption">
                                                    {{ priceLabel }}
                                                </div>
                                            </v-card>
                                        </v-col>

                                        <v-col cols="12">
                                            <v-alert v-if="error" type="error" variant="tonal" class="mb-4"
                                                density="compact">
                                                {{ error }}
                                            </v-alert>

                                            <div class="d-flex align-center">
                                                <v-checkbox v-model="editedItem.is_active" label="Активно"
                                                    density="compact" hide-details></v-checkbox>
                                                <v-spacer></v-spacer>
                                                <v-btn variant="text" @click="close">Отмена</v-btn>
                                                <v-btn type="submit" color="indigo-darken-2" class="ml-2"
                                                    variant="flat">Подтвердить</v-btn>
                                            </div>
                                        </v-col>
                                    </v-row>
                                </v-form>
                            </v-card-text>
                        </v-card>
                    </v-dialog>

                    <!-- Подтверждение удаления -->
                    <v-dialog v-model="deleteDialog" max-width="400px">
                        <v-card>
                            <v-card-title class="text-h6 text-center pa-4">Удалить запись о бронировании?</v-card-title>
                            <v-card-actions class="justify-center pb-4">
                                <v-btn variant="text" @click="closeDelete">Отмена</v-btn>
                                <v-btn color="error" variant="flat" @click="deleteItemConfirm">Да, удалить</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </v-toolbar>
            </template>

            <!-- Отображение колонок -->
            <template v-slot:item.guest_details.last_name="{ item }">
                {{ item.guest_details.last_name }} {{ item.guest_details.first_name[0] }}.
            </template>

            <template v-slot:item.total_cost="{ item }">
                <span class="font-weight-bold">{{ item.total_cost }} ₽</span>
            </template>

            <template v-slot:item.actions="{ item }">
                <v-tooltip text="Выселить" location="top" v-if="item.is_active">
                    <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" icon="mdi-export" size="small" color="warning" variant="text"
                            @click="checkOut(item)"></v-btn>
                    </template>
                </v-tooltip>

                <v-icon size="small" class="mr-2" color="indigo" @click="editItem(item)">mdi-pencil</v-icon>
                <v-icon size="small" color="error" @click="deleteItem(item)">mdi-delete</v-icon>
            </template>
        </v-data-table>
    </v-container>
</template>