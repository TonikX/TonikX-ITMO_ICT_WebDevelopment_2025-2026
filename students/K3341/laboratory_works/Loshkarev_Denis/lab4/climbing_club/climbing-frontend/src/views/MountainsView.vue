<template>
  <v-container>
    <v-row align="center" justify="space-between" class="mb-4">
      <v-col cols="auto">
        <h1 class="text-h4">Справочник Вершин</h1>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" prepend-icon="mdi-plus" @click="openDialog">
          Добавить гору
        </v-btn>
      </v-col>
    </v-row>

    <v-card elevation="2">
      <v-data-table-server
        v-model:page="page"
        :items-per-page="itemsPerPage"
        :headers="headers"
        :items="mountains"
        :items-length="totalMountains"
        :loading="loading"
        loading-text="Загрузка данных..."
        no-data-text="Нет данных о вершинах"
        class="elevation-1"
        @update:options="loadItems"
      >
        <template v-slot:item.height="{ item }">
          {{ item.height }} м.
        </template>

        <template v-slot:bottom>
          <v-divider></v-divider>
          <div class="d-flex justify-center pa-4">
            <v-pagination
              v-model="page"
              :length="totalPages"
              :total-visible="7"
              color="primary"
            ></v-pagination>
          </div>
        </template>
      </v-data-table-server>
    </v-card>

    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">Новая вершина</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field v-model="editedItem.name" label="Название горы" required></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field v-model="editedItem.height" label="Высота (м)" type="number" required></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field v-model="editedItem.country" label="Страна"></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field v-model="editedItem.region" label="Район"></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue-darken-1" variant="text" @click="closeDialog">Отмена</v-btn>
          <v-btn color="green-darken-1" variant="text" @click="saveMountain" :loading="saving">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
      {{ snackbar.text }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import api from '../api'

const mountains = ref([])
const totalMountains = ref(0)
const itemsPerPage = 10 
const page = ref(1)
const loading = ref(true)

const totalPages = computed(() => {
  return Math.ceil(totalMountains.value / itemsPerPage)
})

const headers = [
  { title: 'ID', align: 'start', key: 'id', sortable: true },
  { title: 'Название', key: 'name', sortable: true },
  { title: 'Высота', key: 'height', sortable: true },
  { title: 'Страна', key: 'country', sortable: true },
  { title: 'Район', key: 'region', sortable: true },
]

const dialog = ref(false)
const saving = ref(false)
const editedItem = ref({
  name: '',
  height: null,
  country: '',
  region: ''
})
const snackbar = ref({ show: false, text: '', color: 'success' })

const loadItems = async ({ page, sortBy }) => {
  loading.value = true
  try {
    const params = {
      page: page,
    }

    // Если запрошена сортировка
    if (sortBy && sortBy.length > 0) {
      const sortField = sortBy[0].key
      const sortOrder = sortBy[0].order === 'desc' ? '-' : ''
      params.ordering = `${sortOrder}${sortField}`
    }

    const response = await api.get('api/mountains/', { params })
    
    mountains.value = response.data.results || response.data
    totalMountains.value = response.data.count || response.data.length

  } catch (error) {
    showSnackbar('Ошибка загрузки данных', 'error')
    console.error('Ошибка API:', error)
  } finally {
    loading.value = false
  }
}

const openDialog = () => {
  editedItem.value = { name: '', height: null, country: '', region: '' }
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
}

const saveMountain = async () => {
  saving.value = true
  try {
    await api.post('api/mountains/', editedItem.value)
    showSnackbar('Вершина успешно добавлена!', 'success')
    closeDialog()
    page.value = 1
  } catch (error) {
    showSnackbar('Ошибка при сохранении', 'error')
    console.error(error)
  } finally {
    saving.value = false
  }
}

const showSnackbar = (text, color) => {
  snackbar.value = { show: true, text, color }
}
</script>
