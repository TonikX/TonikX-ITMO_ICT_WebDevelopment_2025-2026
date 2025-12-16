<template>
  <v-container>
    <div class="d-flex justify-space-between align-center mb-6">
      <h1 class="text-h4 font-weight-bold">Сотрудники</h1>
      <v-btn color="primary" prepend-icon="mdi-account-plus" size="large" elevation="2" @click="showHireDialog = true">
        Принять на работу
      </v-btn>
    </div>

    <v-card elevation="2" rounded="lg">
      <v-card-title class="d-flex align-center py-3">
        <v-icon icon="mdi-account-group" class="mr-2" color="grey"></v-icon>
        Активный персонал
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          density="compact"
          label="Поиск"
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          hide-details
          single-line
          style="max-width: 300px;"
        ></v-text-field>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="employees"
        :loading="loading"
        :search="search"
        hover
        @click:row="openEmployee"
      >
        <template v-slot:item.full_name="{ item }">
          <div class="d-flex align-center py-2">
            <v-avatar color="primary" class="mr-3" size="40">
              <span class="text-white text-subtitle-2">{{ getInitials(item) }}</span>
            </v-avatar>
            <div>
              <div class="font-weight-bold">{{ item.last_name }} {{ item.first_name }}</div>
              <div class="text-caption text-grey">{{ item.patronymic }}</div>
            </div>
          </div>
        </template>

        <template v-slot:item.is_active="{ item }">
          <v-chip
            color="success"
            size="small"
            variant="flat"
            class="font-weight-medium"
          >
            Активен
          </v-chip>
        </template>

        <template v-slot:item.actions>
          <v-icon color="grey">mdi-chevron-right</v-icon>
        </template>
      </v-data-table>
    </v-card>

    <v-dialog v-model="showHireDialog" max-width="500">
      <v-card rounded="lg">
        <v-card-title class="bg-primary text-white">Новый сотрудник</v-card-title>
        <v-card-text class="pt-4">
          <v-form @submit.prevent="hireEmployee">
            <v-text-field v-model="form.last_name" label="Фамилия" required variant="outlined"/>
            <v-text-field v-model="form.first_name" label="Имя" required variant="outlined"/>
            <v-text-field v-model="form.patronymic" label="Отчество" variant="outlined"/>
            <v-btn type="submit" color="primary" block size="large" class="mt-2">Сохранить</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/api'

const router = useRouter()
const employees = ref([])
const loading = ref(false)
const showHireDialog = ref(false)
const search = ref('')

const form = reactive({
  first_name: '', last_name: '', patronymic: ''
})

const headers = [
  { title: 'Сотрудник', key: 'full_name', align: 'start' },
  { title: 'Статус', key: 'is_active', align: 'center' },
  { title: '', key: 'actions', sortable: false, align: 'end' },
]

const loadEmployees = async () => {
  loading.value = true
  try {
    const { data } = await api.get('/api/employees/')
    employees.value = data.filter(e => e.is_active)
  } finally {
    loading.value = false
  }
}

const hireEmployee = async () => {
  try {
    await api.post('/api/employees/', { ...form, is_active: true })
    showHireDialog.value = false
    form.first_name = ''; form.last_name = ''; form.patronymic = ''
    loadEmployees()
  } catch (e) {
    alert('Ошибка при создании сотрудника')
  }
}

const openEmployee = (event, { item }) => {
  router.push(`/staff/${item.id}`)
}

const getInitials = (item) => {
  return (item.last_name[0] + item.first_name[0]).toUpperCase()
}

onMounted(loadEmployees)
</script>
