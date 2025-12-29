<template>
  <div>

    <v-row class="mb-6">
      <v-col cols="12">
        <v-card class="hero-card" color="primary">
          <v-card-text class="pa-10 text-center">
            <v-avatar size="120" class="mb-6" color="white">
              <v-icon size="64" color="primary">mdi-shield-check</v-icon>
            </v-avatar>
            <h1 class="text-h2 font-weight-bold mb-4" style="color: white;">
              Guard Market
            </h1>
            <p class="text-h5 mb-6" style="color: rgba(255, 255, 255, 0.9);">
              Платформа для поиска и оказания охранных услуг
            </p>

            <!-- Приветствие для авторизованных -->
            <div v-if="authStore.isAuthenticated" class="mb-6">
              <v-chip size="x-large" class="mr-2 mb-2" color="white">
                <v-avatar start color="primary">
                  <v-icon icon="mdi-account"></v-icon>
                </v-avatar>
                {{ authStore.user.name || authStore.user.email }}
              </v-chip>
              <v-chip size="x-large" class="mb-2" color="white" v-if="authStore.hasCompany">
                <v-avatar start color="success">
                  <v-icon icon="mdi-office-building"></v-icon>
                </v-avatar>
                Владелец компании
              </v-chip>
            </div>

            <!-- Кнопки действий -->
            <div class="d-flex justify-center gap-4">
              <v-btn
                  v-if="!authStore.isAuthenticated"
                  to="/login"
                  color="white"
                  variant="outlined"
                  size="x-large"
                  class="px-8"
              >
                <v-icon start icon="mdi-login"></v-icon>
                Войти
              </v-btn>

              <v-btn
                  v-if="!authStore.isAuthenticated"
                  to="/register"
                  color="white"
                  size="x-large"
                  class="px-8"
              >
                <v-icon start icon="mdi-account-plus"></v-icon>
                Регистрация
              </v-btn>

              <v-btn
                  v-if="authStore.isAuthenticated && !authStore.hasCompany"
                  to="/companies"
                  color="white"
                  variant="outlined"
                  size="x-large"
                  class="px-8"
              >
                <v-icon start icon="mdi-magnify"></v-icon>
                Найти услуги
              </v-btn>

              <v-btn
                  v-if="authStore.isAuthenticated && authStore.hasCompany"
                  :to="`/companies/${authStore.company.id}`"
                  color="white"
                  size="x-large"
                  class="px-8"
              >
                <v-icon start icon="mdi-office-building"></v-icon>
                Моя компания
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Быстрые действия -->
    <v-row v-if="authStore.isAuthenticated" class="mb-8">
      <v-col cols="12">
        <h2 class="text-h4 mb-6 text-center">Быстрые действия</h2>
        <v-row>
          <v-col cols="12" md="3" v-for="action in quickActions" :key="action.title">
            <v-card
                class="action-card"
                :color="action.color"
                :to="action.to"
                height="100%"
            >
              <v-card-text class="text-center pa-6">
                <v-icon size="48" class="mb-4" color="white">{{ action.icon }}</v-icon>
                <h3 class="text-h6 mb-3" style="color: white;">{{ action.title }}</h3>
                <p class="text-body-2" style="color: rgba(255, 255, 255, 0.9);">
                  {{ action.description }}
                </p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <!-- Особенности платформы -->
    <v-row class="mb-8">
      <v-col cols="12">
        <h2 class="text-h4 mb-6 text-center">Возможности платформы</h2>
        <v-row>
          <v-col
              cols="12"
              md="4"
              v-for="feature in features"
              :key="feature.title"
          >
            <v-card class="feature-card pa-6" height="100%">
              <div class="feature-icon mb-4">
                <v-icon size="48" color="primary">{{ feature.icon }}</v-icon>
              </div>
              <h3 class="text-h5 mb-3">{{ feature.title }}</h3>
              <p class="text-body-1 text-grey-darken-1">
                {{ feature.description }}
              </p>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <!-- Как это работает -->
    <v-row class="mb-8">
      <v-col cols="12">
        <v-card class="process-card">
          <v-card-title class="text-h4 text-center pa-6">
            <v-icon large color="primary" class="mr-3">mdi-cogs</v-icon>
            Как это работает
          </v-card-title>
          <v-card-text>
            <v-timeline direction="horizontal" align="start">
              <v-timeline-item
                  v-for="(step, index) in processSteps"
                  :key="step.title"
                  :dot-color="step.color"
                  size="small"
              >
                <template v-slot:icon>
                  <v-avatar size="48" :color="step.color">
                    <span class="text-h5">{{ index + 1 }}</span>
                  </v-avatar>
                </template>
                <v-card class="pa-4" elevation="2">
                  <v-card-title class="text-h6">{{ step.title }}</v-card-title>
                  <v-card-text>{{ step.description }}</v-card-text>
                </v-card>
              </v-timeline-item>
            </v-timeline>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- CTA для неавторизованных -->
    <v-row v-if="!authStore.isAuthenticated">
      <v-col cols="12">
        <v-card class="cta-card" color="primary">
          <v-card-text class="pa-10 text-center">
            <h2 class="text-h3 mb-4" style="color: white;">
              Присоединяйтесь к Guard Market
            </h2>
            <p class="text-h6 mb-6" style="color: rgba(255, 255, 255, 0.9);">
              Начните пользоваться платформой уже сегодня
            </p>
            <div class="d-flex justify-center gap-4">
              <v-btn
                  to="/register"
                  color="white"
                  size="x-large"
                  class="px-8"
              >
                <v-icon start icon="mdi-account-plus"></v-icon>
                Создать аккаунт
              </v-btn>
              <v-btn
                  to="/login"
                  color="white"
                  variant="outlined"
                  size="x-large"
                  class="px-8"
              >
                <v-icon start icon="mdi-login"></v-icon>
                Войти
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// Быстрые действия для авторизованных пользователей
const quickActions = computed(() => {
  const baseActions = [
    {
      title: 'Все компании',
      icon: 'mdi-office-building',
      description: 'Просмотр охранных компаний',
      color: 'primary',
      to: '/companies'
    },
    {
      title: 'Мои заявки',
      icon: 'mdi-format-list-bulleted',
      description: 'Отслеживайте ваши заявки',
      color: 'info',
      to: '/requests'
    },
    {
      title: 'Избранное',
      icon: 'mdi-heart',
      description: 'Сохраненные услуги',
      color: 'pink',
      to: '/favorites'
    }
  ]

  // Добавляем дополнительные действия в зависимости от роли
  if (authStore.hasCompany) {
    baseActions.push({
      title: 'Управление',
      icon: 'mdi-cog',
      description: 'Управление компанией',
      color: 'success',
      to: '/company'
    })
  } else if (authStore.isAuthenticated) {
    baseActions.push({
      title: 'Создать компанию',
      icon: 'mdi-plus-circle',
      description: 'Создайте свою компанию',
      color: 'success',
      to: '/company'
    })
  }

  return baseActions
})

// Особенности платформы
const features = [
  {
    icon: 'mdi-shield-search',
    title: 'Поиск услуг',
    description: 'Найдите подходящую охранную услугу среди множества компаний'
  },
  {
    icon: 'mdi-handshake',
    title: 'Прямое взаимодействие',
    description: 'Общайтесь напрямую с поставщиками услуг и клиентами'
  },
  {
    icon: 'mdi-star',
    title: 'Рейтинги и отзывы',
    description: 'Оценивайте компании и оставляйте отзывы о сотрудничестве'
  },
  {
    icon: 'mdi-heart',
    title: 'Избранное',
    description: 'Сохраняйте понравившиеся услуги для быстрого доступа'
  },
  {
    icon: 'mdi-chart-line',
    title: 'Аналитика',
    description: 'Отслеживайте статистику и эффективность вашей компании'
  },
  {
    icon: 'mdi-security',
    title: 'Безопасность',
    description: 'Все транзакции защищены и проходят проверку'
  }
]

// Этапы работы
const processSteps = [
  {
    title: 'Регистрация',
    description: 'Создайте аккаунт как клиент или владелец компании',
    color: 'primary'
  },
  {
    title: 'Поиск',
    description: 'Найдите подходящую услугу или создайте свою компанию',
    color: 'info'
  },
  {
    title: 'Заявка',
    description: 'Оставьте заявку на услугу или примите заявку от клиента',
    color: 'success'
  },
  {
    title: 'Сотрудничество',
    description: 'Выполните заказ или получите услугу',
    color: 'warning'
  },
  {
    title: 'Оценка',
    description: 'Оставьте отзыв о сотрудничестве',
    color: 'pink'
  }
]
</script>

<style scoped>
/* Герой-секция */
.hero-card {
  border-radius: 16px !important;
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
  overflow: hidden;
  position: relative;
}

.hero-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
}

/* Карточки действий */
.action-card {
  border-radius: 12px !important;
  transition: all 0.3s ease;
  cursor: pointer;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2) !important;
}

/* Карточки особенностей */
.feature-card {
  border-radius: 12px !important;
  transition: all 0.3s ease;
  border: 1px solid #e0e0e0;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
  border-color: #1976d2;
}

.feature-icon {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(25, 118, 210, 0.1);
  border-radius: 50%;
  margin: 0 auto;
}

/* Карточка процесса */
.process-card {
  border-radius: 16px !important;
  overflow: hidden;
}

/* CTA секция */
.cta-card {
  border-radius: 16px !important;
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
  overflow: hidden;
  position: relative;
}

.cta-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
}

/* Общие стили */
.gap-4 {
  gap: 16px;
}

.text-center {
  text-align: center;
}

/* Адаптивность */
@media (max-width: 960px) {
  .hero-card .v-card-text {
    padding: 48px 24px !important;
  }

  .text-h2 {
    font-size: 2.5rem !important;
  }

  .cta-card .v-card-text {
    padding: 48px 24px !important;
  }

  .text-h3 {
    font-size: 2rem !important;
  }
}

@media (max-width: 600px) {
  .hero-card .v-card-text {
    padding: 32px 16px !important;
  }

  .text-h2 {
    font-size: 2rem !important;
  }

  .d-flex.justify-center.gap-4 {
    flex-direction: column;
    align-items: center;
  }

  .cta-card .v-card-text {
    padding: 32px 16px !important;
  }

  .text-h3 {
    font-size: 1.5rem !important;
  }
}

/* Стили для таймлайна */
:deep(.v-timeline-item__dot) {
  box-shadow: none;
}

:deep(.v-timeline-item__body) {
  max-width: 200px;
}
</style>