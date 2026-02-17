<script setup>
/**
 * EmployeesView.vue - Страница управления персоналом отеля.
 * Реализует CRUD операции и механизм "мягкого удаления" (увольнения).
 * Уволенные сотрудники остаются в базе для истории, но помечаются соответствующим статусом.
 */
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()

// --- Состояние ---
const employees = ref([])
const loading = ref(true)
const search = ref('')
const error = ref('')

// Управление диалогами
const dialog = ref(false)
const editedIndex = ref(-1)

// Валидация
const form = ref(null)
const valid = ref(false)
const rules = {
    required: v => !!v || 'Это поле обязательно'
}

const defaultItem = {
    last_name: '',
    first_name: '',
    patronymic: '',
    is_active: true
}

const editedItem = ref({ ...defaultItem })

const formTitle = computed(() => editedIndex.value === -1 ? 'Новый сотрудник' : 'Редактировать данные')

const headers = [
    { title: 'Фамилия', key: 'last_name' },
    { title: 'Имя', key: 'first_name' },
    { title: 'Отчество', key: 'patronymic' },
    { title: 'Статус', key: 'is_active', align: 'center' },
    { title: 'Действия', key: 'actions', sortable: false, align: 'end' },
]

/**
 * Загрузка списка сотрудников.
 */
async function fetchEmployees() {
    loading.value = true
    try {
        const res = await api.get('/api/employees/')
        employees.value = res.data

        // Если перешли с главной страницы по кнопке "Добавить", открываем диалог
        if (route.query.new === 'true') {
            dialog.value = true
            router.replace({ query: null })
        }
    } catch (e) {
        console.error('Ошибка загрузки сотрудников:', e)
    } finally {
        loading.value = false
    }
}

/**
 * Сохранение (Создание или Обновление).
 */
async function save() {
    error.value = ''
    const { valid } = await form.value.validate()
    if (!valid) return

    try {
        if (editedIndex.value > -1) {
            await api.put(`/api/employees/${editedItem.value.id}/`, editedItem.value)
        } else {
            await api.post('/api/employees/', editedItem.value)
        }
        close()
        fetchEmployees()
    } catch (e) {
        error.value = 'Ошибка при сохранении данных сотрудника'
        console.error(e)
    }
}

/**
 * "Увольнение" сотрудника (PATCH запрос для изменения флага активности).
 */
async function fireEmployee(item) {
    if (!confirm(`Вы действительно хотите уволить сотрудника ${item.last_name}?`)) return
    try {
        await api.patch(`/api/employees/${item.id}/`, { is_active: false })
        fetchEmployees()
    } catch (e) {
        alert('Ошибка при выполнении операции увольнения')
    }
}

/**
 * Восстановление сотрудника на работу.
 */
async function restoreEmployee(item) {
    if (!confirm(`Восстановить сотрудника ${item.last_name} в штате?`)) return
    try {
        await api.patch(`/api/employees/${item.id}/`, { is_active: true })
        fetchEmployees()
    } catch (e) {
        alert('Ошибка при восстановлении сотрудника')
    }
}

function editItem(item) {
    editedIndex.value = employees.value.indexOf(item)
    editedItem.value = Object.assign({}, item)
    dialog.value = true
}

function close() {
    dialog.value = false
    error.value = ''
    editedItem.value = { ...defaultItem }
    editedIndex.value = -1
}

onMounted(fetchEmployees)
</script>

<template>
    <v-container>
        <v-data-table :headers="headers" :items="employees" :search="search" :loading="loading" class="elevation-1">
            <template v-slot:top>
                <v-toolbar flat color="white">
                    <v-toolbar-title class="font-weight-bold text-success">Персонал отеля</v-toolbar-title>
                    <v-divider class="mx-4" inset vertical></v-divider>
                    <v-spacer></v-spacer>

                    <v-text-field v-model="search" density="compact" label="Поиск по фамилии" single-line hide-details
                        variant="outlined" prepend-inner-icon="mdi-magnify" class="mr-4"
                        style="max-width: 300px"></v-text-field>

                    <v-btn color="success" variant="flat" prepend-icon="mdi-account-hard-hat" @click="dialog = true">
                        Принять на работу
                    </v-btn>

                    <!-- Форма редактирования -->
                    <v-dialog v-model="dialog" max-width="500px">
                        <v-card shadow="12">
                            <v-card-title class="bg-success text-white pa-4">
                                <span class="text-h5">{{ formTitle }}</span>
                            </v-card-title>

                            <v-card-text class="pt-6">
                                <v-form ref="form" v-model="valid" @submit.prevent="save">
                                    <v-row dense>
                                        <v-col cols="12">
                                            <v-text-field v-model="editedItem.last_name" label="Фамилия"
                                                variant="outlined" density="compact"
                                                :rules="[rules.required]"></v-text-field>
                                        </v-col>
                                        <v-col cols="12">
                                            <v-text-field v-model="editedItem.first_name" label="Имя" variant="outlined"
                                                density="compact" :rules="[rules.required]"></v-text-field>
                                        </v-col>
                                        <v-col cols="12">
                                            <v-text-field v-model="editedItem.patronymic" label="Отчество"
                                                variant="outlined" density="compact"></v-text-field>
                                        </v-col>
                                    </v-row>

                                    <v-alert v-if="error" type="error" variant="tonal" class="mt-4" density="compact">
                                        {{ error }}
                                    </v-alert>

                                    <div class="d-flex justify-end mt-6">
                                        <v-btn color="grey" variant="text" @click="close" class="mr-2">Отмена</v-btn>
                                        <v-btn color="success" type="submit" variant="flat">Сохранить</v-btn>
                                    </div>
                                </v-form>
                            </v-card-text>
                        </v-card>
                    </v-dialog>
                </v-toolbar>
            </template>

            <!-- Отображение статуса -->
            <template v-slot:item.is_active="{ item }">
                <v-chip :color="item.is_active ? 'success' : 'error'" size="small" class="font-weight-bold">
                    {{ item.is_active ? 'РАБОТАЕТ' : 'УВОЛЕН' }}
                </v-chip>
            </template>

            <!-- Колонки действий -->
            <template v-slot:item.actions="{ item }">
                <v-icon size="small" class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>

                <!-- Кнопка увольнения (только для активных) -->
                <v-tooltip text="Уволить" location="top" v-if="item.is_active">
                    <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" icon="mdi-account-remove" size="x-small" color="error" variant="text"
                            @click="fireEmployee(item)"></v-btn>
                    </template>
                </v-tooltip>

                <!-- Кнопка восстановления (только для уволенных) -->
                <v-tooltip text="Восстановить" location="top" v-else>
                    <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" icon="mdi-account-check" size="x-small" color="success" variant="text"
                            @click="restoreEmployee(item)"></v-btn>
                    </template>
                </v-tooltip>
            </template>
        </v-data-table>
    </v-container>
</template>