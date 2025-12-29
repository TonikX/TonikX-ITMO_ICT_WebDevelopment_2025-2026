<template>
  <div>
    <div v-if="isLoading" class="text-center py-10">
      <v-progress-circular indeterminate></v-progress-circular>
    </div>

    <v-row v-else>
      <v-col
          v-for="service in services"
          :key="service.id"
          cols="12"
          md="6"
          lg="4"
      >
        <v-card class="h-100">
          <v-card-title class="text-h6">
            {{ service.name }}
          </v-card-title>

          <v-card-subtitle class="mb-2">
            <v-chip
                v-if="service.current_discount"
                color="red"
                text-color="white"
                size="small"
                class="mr-2"
            >
              -{{ service.current_discount.discount_percent }}%
            </v-chip>
            <span class="text-body-2">
              Цена за услугу
            </span>
          </v-card-subtitle>

          <v-card-text>
            <p class="text-body-2 mb-4">
              {{ service.description || 'Нет описания' }}
            </p>

            <div class="d-flex align-center">
              <div>
                <div class="text-h5 font-weight-bold">
                  {{ service.current_price || service.price }} ₽
                </div>
                <div
                    v-if="service.current_price && service.current_price !== service.price"
                    class="text-body-2 text-decoration-line-through text-grey"
                >
                  {{ service.price }} ₽
                </div>
                <div v-if="service.current_discount" class="text-caption text-red mt-1">
                  Скидка действует до: {{ formatDate(service.current_discount.end_date) }}
                </div>
              </div>

              <v-spacer></v-spacer>

              <v-btn
                  v-if="isAuthenticated"
                  color="primary"
                  @click="$emit('create-request', service)"
                  size="small"
              >
                Оставить заявку
              </v-btn>

              <v-btn
                  v-else
                  to="/login"
                  color="primary"
                  variant="outlined"
                  size="small"
              >
                Войдите
              </v-btn>
            </div>
          </v-card-text>

          <v-card-actions>
            <v-btn
                v-if="isAuthenticated && !isServiceInFavorites(service.id)"
                @click="$emit('add-to-favorites', service)"
                variant="text"
                color="pink"
                size="small"
                :loading="favoritesLoading"
            >
              <v-icon start icon="mdi-heart-outline"></v-icon>
              В избранное
            </v-btn>

            <v-btn
                v-else-if="isAuthenticated"
                @click="$emit('remove-from-favorites', service.id)"
                variant="text"
                color="pink"
                size="small"
                :loading="favoritesLoading"
            >
              <v-icon start icon="mdi-heart"></v-icon>
              В избранном
            </v-btn>

            <v-spacer></v-spacer>

            <!-- Кнопки управления для владельца -->
            <div v-if="isCompanyOwner" class="d-flex">
              <v-btn
                  @click="$emit('edit-service', service)"
                  variant="text"
                  size="small"
                  color="primary"
                  class="mr-2"
                  :loading="serviceLoading"
              >
                <v-icon icon="mdi-pencil"></v-icon>
              </v-btn>
              <v-btn
                  @click="$emit('delete-service', service.id)"
                  variant="text"
                  size="small"
                  color="error"
                  :loading="serviceLoading"
              >
                <v-icon icon="mdi-delete"></v-icon>
              </v-btn>
            </div>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col v-if="services.length === 0" cols="12">
        <v-alert type="info">
          {{ noServicesMessage }}
        </v-alert>

        <div v-if="isCompanyOwner && showAddButton" class="text-center mt-4">
          <v-btn
              color="primary"
              @click="$emit('add-service')"
              :loading="serviceLoading"
          >
            <v-icon start icon="mdi-plus"></v-icon>
            {{ addButtonText }}
          </v-btn>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  services: {
    type: Array,
    default: () => []
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  isAuthenticated: {
    type: Boolean,
    default: false
  },
  isCompanyOwner: {
    type: Boolean,
    default: false
  },
  favorites: {
    type: Array,
    default: () => []
  },
  favoritesLoading: {
    type: Boolean,
    default: false
  },
  serviceLoading: {
    type: Boolean,
    default: false
  },
  noServicesMessage: {
    type: String,
    default: 'У этой компании пока нет услуг.'
  },
  showAddButton: {
    type: Boolean,
    default: false
  },
  addButtonText: {
    type: String,
    default: 'Добавить первую услугу'
  }
})

const emit = defineEmits([
  'create-request',
  'add-to-favorites',
  'remove-from-favorites',
  'edit-service',
  'delete-service',
  'add-service'
])

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const isServiceInFavorites = (serviceId) => {
  return props.favorites.some(fav => fav.service_info?.id === serviceId)
}
</script>

<style scoped>
.h-100 {
  height: 100%;
}

.v-card {
  transition: transform 0.2s;
}

.v-card:hover {
  transform: translateY(-2px);
}
</style>