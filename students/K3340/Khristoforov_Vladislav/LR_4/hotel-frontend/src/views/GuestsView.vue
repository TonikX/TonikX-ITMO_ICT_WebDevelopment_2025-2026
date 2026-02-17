<script setup>
/**
 * GuestsView.vue - Страница управления базой гостей.
 * Позволяет просматривать список клиентов, добавлять новых
 * и создавать города "на лету" через v-combobox.
 */
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()

// --- Реактивное состояние ---
const guests = ref([])      // Список всех гостей
const cities = ref([])      // Справочник городов
const loading = ref(true)   // Индикатор загрузки данных
const search = ref('')      // Строка поиска в таблице
const error = ref('')       // Сообщение об ошибке для формы

// Состояние диалоговых окон
const dialog = ref(false)
const deleteDialog = ref(false)
const editedIndex = ref(-1)

// Валидация
const form = ref(null)
const valid = ref(false)
const rules = {
    required: v => !!v || 'Это поле обязательно для заполнения'
}

// Начальные данные
const defaultItem = {
    last_name: '',
    first_name: '',
    patronymic: '',
    passport: '',
    city: null
}
const editedItem = ref({ ...defaultItem })
const itemToDelete = ref(null)

const formTitle = computed(() => editedIndex.value === -1 ? 'Новый гость' : 'Редактировать данные')

const headers = [
    { title: 'Фамилия', key: 'last_name' },
    { title: 'Имя', key: 'first_name' },
    { title: 'Отчество', key: 'patronymic' },
    { title: 'Паспорт', key: 'passport' },
    { title: 'Город', key: 'city_details.name' },
    { title: 'Действия', key: 'actions', sortable: false },
]

/**
 * Загрузка данных.
 * Используем Promise.all для параллельного выполнения запросов.
 */
async function fetchData() {
    loading.value = true
    try {
        const [gRes, cRes] = await Promise.all([
            api.get('/api/guests/'),
            api.get('/api/cities/')
        ])
        guests.value = gRes.data
        cities.value = cRes.data

        // Обработка быстрого перехода с главной страницы (?new=true)
        if (route.query.new === 'true') {
            dialog.value = true
            router.replace({ query: null })
        }
    } catch (e) {
        console.error('Ошибка загрузки данных гостей:', e)
    } finally {
        loading.value = false
    }
}

/**
 * Сохранение гостя.
 * Если город введен вручную (текстом), создаем его в БД.
 */
async function save() {
    error.value = ''
    const { valid } = await form.value.validate()
    if (!valid) return

    try {
        const payload = { ...editedItem.value }

        // Логика работы с v-combobox для города
        if (typeof payload.city === 'string' && payload.city.trim() !== '') {
            // Ищем, нет ли такого города уже в списке
            const exist = cities.value.find(c => c.name.toLowerCase() === payload.city.toLowerCase())
            if (exist) {
                payload.city = exist.id
            } else {
                // Если город новый — создаем его через API
                const newCityRes = await api.post('/api/cities/', { name: payload.city })
                payload.city = newCityRes.data.id
                cities.value.push(newCityRes.data) // Обновляем локальный список
            }
        } else if (payload.city && typeof payload.city === 'object') {
            payload.city = payload.city.id
        }

        // Удаляем лишние вложенные данные перед отправкой
        if (payload.city_details) delete payload.city_details

        if (editedIndex.value > -1) {
            await api.put(`/api/guests/${payload.id}/`, payload)
        } else {
            await api.post('/api/guests/', payload)
        }
        close()
        fetchData()
    } catch (e) {
        error.value = 'Ошибка при сохранении данных гостя'
        console.error(e)
    }
}

/**
 * Удаление гостя.
 */
async function deleteItemConfirm() {
    try {
        await api.delete(`/api/guests/${itemToDelete.value.id}/`)
        fetchData()
    } catch (e) {
        alert('Ошибка удаления. Возможно, у гостя есть активные бронирования.')
    }
    closeDelete()
}

/**
 * Подготовка формы к редактированию.
 */
function editItem(item) {
    editedIndex.value = guests.value.indexOf(item)
    editedItem.value = Object.assign({}, item)
    // Извлекаем ID города для селекта
    if (editedItem.value.city_details) {
        editedItem.value.city = editedItem.value.city_details.id
    }
    dialog.value = true
}

function deleteItem(item) {
    itemToDelete.value = item
    deleteDialog.value = true
}

function close() {
    dialog.value = false
    error.value = ''
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
        <v-data-table :headers="headers" :items="guests" :search="search" :loading="loading" class="elevation-1">
            <template v-slot:top>
                <v-toolbar flat color="white">
                    <v-toolbar-title class="text-h6 font-weight-bold text-indigo">База гостей</v-toolbar-title>
                    <v-divider class="mx-4" inset vertical></v-divider>
                    <v-spacer></v-spacer>

                    <!-- Поиск -->
                    <v-text-field v-model="search" density="compact" label="Поиск гостя" single-line hide-details
                        variant="outlined" prepend-inner-icon="mdi-magnify" class="mr-4"
                        style="max-width: 300px"></v-text-field>

                    <!-- Кнопка добавления -->
                    <v-btn color="indigo-darken-2" variant="flat" prepend-icon="mdi-account-plus"
                        @click="dialog = true">
                        Добавить гостя
                    </v-btn>

                    <!-- Форма редактирования -->
                    <v-dialog v-model="dialog" max-width="600px" persistent>
                        <v-card>
                            <v-card-title class="bg-indigo-darken-3 text-white pa-4">
                                <span class="text-h5">{{ formTitle }}</span>
                            </v-card-title>

                            <v-card-text class="pt-6">
                                <v-form ref="form" v-model="valid" @submit.prevent="save">
                                    <v-row>
                                        <v-col cols="12" sm="4">
                                            <v-text-field v-model="editedItem.last_name" label="Фамилия"
                                                variant="outlined" density="compact"
                                                :rules="[rules.required]"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" sm="4">
                                            <v-text-field v-model="editedItem.first_name" label="Имя" variant="outlined"
                                                density="compact" :rules="[rules.required]"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" sm="4">
                                            <v-text-field v-model="editedItem.patronymic" label="Отчество"
                                                variant="outlined" density="compact"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" sm="6">
                                            <v-text-field v-model="editedItem.passport" label="Паспортные данные"
                                                variant="outlined" density="compact"
                                                prepend-inner-icon="mdi-card-account-details" hint="Серия и номер"
                                                persistent-hint :rules="[rules.required]"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" sm="6">
                                            <!-- v-combobox позволяет выбирать из списка или вводить текст -->
                                            <v-combobox v-model="editedItem.city" :items="cities" item-title="name"
                                                item-value="id" label="Город проживания" variant="outlined"
                                                density="compact" prepend-inner-icon="mdi-city"
                                                hint="Выберите из списка или введите новый" persistent-hint
                                                :rules="[rules.required]"></v-combobox>
                                        </v-col>
                                    </v-row>

                                    <v-alert v-if="error" type="error" variant="tonal" class="mt-4" density="compact">
                                        {{ error }}
                                    </v-alert>

                                    <div class="d-flex justify-end mt-6">
                                        <v-btn color="grey-darken-1" variant="text" @click="close"
                                            class="mr-2">Отмена</v-btn>
                                        <v-btn color="indigo-darken-2" type="submit" variant="flat">Сохранить</v-btn>
                                    </div>
                                </v-form>
                            </v-card-text>
                        </v-card>
                    </v-dialog>

                    <!-- Подтверждение удаления -->
                    <v-dialog v-model="deleteDialog" max-width="400px">
                        <v-card>
                            <v-card-title class="text-h6 text-center pa-4">Удалить гостя из базы?</v-card-title>
                            <v-card-text class="text-center pb-0 text-grey-darken-1">
                                Внимание: если у гостя есть история бронирований, удаление может быть заблокировано
                                системой.
                            </v-card-text>
                            <v-card-actions class="justify-center pa-4">
                                <v-btn color="grey" variant="text" @click="closeDelete">Отмена</v-btn>
                                <v-btn color="error" variant="flat" @click="deleteItemConfirm">Удалить</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </v-toolbar>
            </template>

            <!-- Кнопки действий -->
            <template v-slot:item.actions="{ item }">
                <v-icon size="small" class="mr-2" color="indigo" @click="editItem(item)">mdi-pencil</v-icon>
                <v-icon size="small" color="error" @click="deleteItem(item)">mdi-delete</v-icon>
            </template>
        </v-data-table>
    </v-container>
</template>