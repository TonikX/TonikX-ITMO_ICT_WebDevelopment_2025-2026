<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex align-center">
            <span>Дома</span>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              prepend-icon="mdi-plus"
              @click="$router.push('/buildings/new')"
            >
              Создать дом
            </v-btn>
          </v-card-title>
          <v-card-text>
            <!-- Фильтры -->
            <v-row class="mb-4">
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="filters.search"
                  label="Поиск"
                  prepend-inner-icon="mdi-magnify"
                  variant="outlined"
                  density="compact"
                  clearable
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6" class="d-flex align-center">
                <v-btn
                  color="primary"
                  @click="loadBuildings"
                  prepend-icon="mdi-refresh"
                >
                  Обновить
                </v-btn>
              </v-col>
            </v-row>

            <!-- Таблица домов -->
            <v-data-table
              :headers="headers"
              :items="buildings"
              :loading="loading"
              :items-per-page="20"
              :items-per-page-options="[10, 20, 50, 100]"
              :server-items-length="totalCount"
              @update:options="handleOptionsUpdate"
            >
              <template v-slot:item.created_at="{ item }">
                {{ formatDateTime(item.created_at) }}
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn
                  icon="mdi-eye"
                  size="small"
                  variant="text"
                  @click="$router.push(`/buildings/${item.id}`)"
                ></v-btn>
                <v-btn
                  icon="mdi-pencil"
                  size="small"
                  variant="text"
                  @click="$router.push(`/buildings/${item.id}/edit`)"
                ></v-btn>
                <v-btn
                  icon="mdi-delete"
                  size="small"
                  variant="text"
                  color="error"
                  @click="confirmDelete(item)"
                ></v-btn>
              </template>
              <template v-slot:no-data>
                <div class="text-center py-8">
                  <v-icon size="64" color="grey-lighten-1">mdi-office-building-off</v-icon>
                  <div class="text-h6 mt-4 text-grey">Нет домов</div>
                </div>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить дом "{{ buildingToDelete?.address }}"? Это действие нельзя отменить.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="deleteDialog = false">Отмена</v-btn>
          <v-btn color="error" @click="deleteBuilding" :loading="deleting">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { buildingsService } from '@/services/buildingsService'
import { formatDateTime } from '@/utils/dateUtils'

export default {
  name: 'BuildingsList',
  data() {
    return {
      buildings: [],
      loading: false,
      totalCount: 0,
      filters: {
        search: null,
      },
      headers: [
        { title: 'ID', key: 'id', sortable: true },
        { title: 'Адрес', key: 'address', sortable: true },
        { title: 'Этажей', key: 'total_floors', sortable: true },
        { title: 'Описание', key: 'description', sortable: false },
        { title: 'Дата создания', key: 'created_at', sortable: true },
        { title: 'Действия', key: 'actions', sortable: false },
      ],
      pagination: {
        page: 1,
        itemsPerPage: 20,
        sortBy: [],
      },
      deleteDialog: false,
      buildingToDelete: null,
      deleting: false,
    }
  },
  async mounted() {
    await this.loadBuildings()
  },
  methods: {
    async loadBuildings() {
      this.loading = true
      try {
        const params = {
          page: this.pagination.page,
          page_size: this.pagination.itemsPerPage,
        }
        
        if (this.filters.search) {
          params.search = this.filters.search
        }
        if (this.pagination.sortBy.length > 0) {
          params.ordering = this.pagination.sortBy[0].key
          if (this.pagination.sortBy[0].order === 'desc') {
            params.ordering = `-${params.ordering}`
          }
        }

        const data = await buildingsService.getBuildings(params)
        this.buildings = data.results || []
        this.totalCount = data.count || 0
      } catch (error) {
        console.error('Error loading buildings:', error)
        this.buildings = []
      } finally {
        this.loading = false
      }
    },
    handleOptionsUpdate(options) {
      this.pagination.page = options.page
      this.pagination.itemsPerPage = options.itemsPerPage
      this.pagination.sortBy = options.sortBy || []
      this.loadBuildings()
    },
    confirmDelete(building) {
      this.buildingToDelete = building
      this.deleteDialog = true
    },
    async deleteBuilding() {
      this.deleting = true
      try {
        await buildingsService.deleteBuilding(this.buildingToDelete.id)
        this.deleteDialog = false
        this.buildingToDelete = null
        await this.loadBuildings()
      } catch (error) {
        console.error('Error deleting building:', error)
      } finally {
        this.deleting = false
      }
    },
    formatDateTime,
  },
}
</script>

