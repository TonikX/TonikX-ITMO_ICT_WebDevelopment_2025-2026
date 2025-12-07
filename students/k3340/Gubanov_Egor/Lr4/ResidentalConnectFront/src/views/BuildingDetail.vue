<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8" offset-md="2">
        <v-card v-if="building">
          <v-card-title class="d-flex align-center">
            <span>Дом #{{ building.id }}</span>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              prepend-icon="mdi-pencil"
              @click="$router.push(`/buildings/${building.id}/edit`)"
            >
              Редактировать
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-card variant="outlined" class="mb-4">
              <v-card-title>Основная информация</v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <v-list-item-title>Адрес</v-list-item-title>
                    <v-list-item-subtitle class="text-h6">{{ building.address }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Количество этажей</v-list-item-title>
                    <v-list-item-subtitle>{{ building.total_floors }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item v-if="building.description">
                    <v-list-item-title>Описание</v-list-item-title>
                    <v-list-item-subtitle>{{ building.description }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Дата создания</v-list-item-title>
                    <v-list-item-subtitle>{{ formatDateTime(building.created_at) }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>

            <!-- Квартиры в доме -->
            <v-card variant="outlined">
              <v-card-title>Квартиры в доме</v-card-title>
              <v-card-text>
                <v-btn
                  color="primary"
                  prepend-icon="mdi-home"
                  @click="$router.push(`/apartments?building=${building.id}`)"
                >
                  Просмотреть квартиры
                </v-btn>
              </v-card-text>
            </v-card>
          </v-card-text>
        </v-card>

        <v-card v-else-if="loading">
          <v-card-text>
            <v-skeleton-loader type="card"></v-skeleton-loader>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { buildingsService } from '@/services/buildingsService'
import { formatDateTime } from '@/utils/dateUtils'

export default {
  name: 'BuildingDetail',
  data() {
    return {
      building: null,
      loading: false,
    }
  },
  async mounted() {
    await this.loadBuilding()
  },
  methods: {
    async loadBuilding() {
      this.loading = true
      try {
        this.building = await buildingsService.getBuilding(this.$route.params.id)
      } catch (error) {
        console.error('Error loading building:', error)
        this.$router.push('/buildings')
      } finally {
        this.loading = false
      }
    },
    formatDateTime,
  },
}
</script>

