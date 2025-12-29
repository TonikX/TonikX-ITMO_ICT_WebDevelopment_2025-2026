<template>
  <v-card class="request-card">
    <v-card-title class="text-h6">
      {{ request.service_info?.name }}
    </v-card-title>

    <v-card-subtitle class="pb-2">
      <div class="d-flex align-center flex-wrap mb-1">
        <!-- Статус -->
        <v-chip
            :color="getStatusColor(request.status)"
            size="small"
            class="mr-2 mb-1"
        >
          {{ getStatusTranslation(request.status) }}
        </v-chip>

        <!-- Компания -->
        <v-chip
            v-if="request.service_info?.company"
            color="primary"
            variant="outlined"
            size="small"
            :to="`/companies/${request.service_info.company.id}`"
            class="mr-2 mb-1"
        >
          <v-icon start icon="mdi-office-building"></v-icon>
          {{ request.service_info.company.name }}
        </v-chip>

        <!-- Цена -->
        <v-chip
            color="secondary"
            variant="outlined"
            size="small"
            class="mr-2 mb-1"
        >
          <v-icon start icon="mdi-cash"></v-icon>
          {{ request.service_info?.price }} ₽
        </v-chip>
      </div>
    </v-card-subtitle>

    <v-card-text>
      <!-- Описание -->
      <div class="mb-3">
        <strong class="text-body-2">Описание:</strong>
        <p class="text-body-1 mt-1">
          {{ request.description || 'Нет описания' }}
        </p>
      </div>

      <!-- Информация о пользователе (для владельца компании) -->
      <div v-if="showUserInfo && request.user_info" class="mb-3">
        <strong class="text-body-2">Пользователь:</strong>
        <p class="text-body-1 mt-1">
          {{ request.user_info.name }}
          <br>
          <small class="text-grey">{{ request.user_info.email }}</small>
        </p>
      </div>

      <!-- Комментарий администратора -->
      <div v-if="request.admin_comment" class="mb-3">
        <strong class="text-body-2">Комментарий компании:</strong>
        <p class="text-body-1 mt-1 text-blue">
          {{ request.admin_comment }}
        </p>
      </div>

      <!-- Даты -->
      <div class="d-flex justify-space-between text-caption text-grey">
        <div>
          <v-icon small icon="mdi-calendar" class="mr-1"></v-icon>
          Создана: {{ formatDate(request.created_at) }}
        </div>
        <div v-if="request.created_at !== request.updated_at">
          <v-icon small icon="mdi-update" class="mr-1"></v-icon>
          Обновлена: {{ formatDate(request.updated_at) }}
        </div>
      </div>
    </v-card-text>

    <v-card-actions>
      <!-- Действия для автора заявки -->
      <template v-if="isMyRequest">
        <v-btn
            v-if="request.status === 'pending'"
            @click="$emit('edit-description', request)"
            variant="text"
            size="small"
            color="primary"
            :loading="loading"
        >
          <v-icon start icon="mdi-pencil"></v-icon>
          Изменить описание
        </v-btn>

        <v-btn
            @click="$emit('delete-request', request.id)"
            variant="text"
            size="small"
            color="error"
            :loading="loading"
        >
          <v-icon start icon="mdi-delete"></v-icon>
          Удалить
        </v-btn>
      </template>

      <!-- Действия для владельца компании -->
      <template v-else-if="isCompanyRequest">
        <v-btn
            @click="$emit('change-status', request)"
            variant="text"
            size="small"
            color="primary"
            :loading="loading"
        >
          <v-icon start icon="mdi-cog"></v-icon>
          Изменить статус
        </v-btn>

        <v-btn
            @click="$emit('add-comment', request)"
            variant="text"
            size="small"
            color="secondary"
            :loading="loading"
        >
          <v-icon start icon="mdi-comment"></v-icon>
          Добавить комментарий
        </v-btn>
      </template>

      <!-- Просмотр деталей -->
      <v-spacer></v-spacer>
      <v-btn
          @click="$emit('view-details', request)"
          variant="text"
          size="small"
          color="info"
      >
        <v-icon start icon="mdi-information"></v-icon>
        Подробнее
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  request: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  showUserInfo: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  'edit-description',
  'delete-request',
  'change-status',
  'add-comment',
  'view-details'
])

const authStore = useAuthStore()

// Computed свойства
const isMyRequest = computed(() => {
  if (!authStore.user || !props.request.user_info) return false
  return authStore.user.id === props.request.user_info.id
})

const isCompanyRequest = computed(() => {
  if (!authStore.user || !authStore.company) return false
  return props.request.service_info?.company?.id === authStore.company.id
})

// Вспомогательные функции
const getStatusTranslation = (status) => {
  const translations = {
    pending: 'Ожидание',
    confirmed: 'Подтверждено',
    in_progress: 'В работе',
    completed: 'Завершено',
    cancelled: 'Отменено'
  }
  return translations[status] || status
}

const getStatusColor = (status) => {
  const colors = {
    pending: 'warning',
    confirmed: 'info',
    in_progress: 'primary',
    completed: 'success',
    cancelled: 'error'
  }
  return colors[status] || 'grey'
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (e) {
    return dateString
  }
}
</script>

<style scoped>
.request-card {
  transition: transform 0.2s;
  margin-bottom: 16px;
}

.request-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
}
</style>