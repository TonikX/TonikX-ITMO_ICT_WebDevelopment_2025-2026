<template>
  <div class="home-view">
    <v-row class="mb-8">
      <v-col cols="12">
        <div class="welcome-section">
          <h1 class="welcome-title">Добро пожаловать в Издательский дом</h1>
          <p class="welcome-subtitle">Система управления издательской деятельностью</p>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" sm="6" md="4" lg="3" v-for="card in dashboardCards" :key="card.title">
        <v-card
          :to="card.to"
          class="dashboard-card"
          hover
        >
          <div class="card-icon-wrapper" :style="{ background: card.gradient }">
            <v-icon :icon="card.icon" size="32" color="white"></v-icon>
          </div>
          <v-card-text class="text-center pt-4">
            <h3 class="card-title">{{ card.title }}</h3>
            <p class="text-medium-emphasis text-body-2">{{ card.description }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-8">
      <v-col cols="12">
        <h2 class="section-title mb-4">
          <v-icon class="mr-2">mdi-chart-box</v-icon>
          Быстрый доступ к отчётам
        </h2>
      </v-col>

      <v-col cols="12" md="6" lg="4" v-for="report in quickReports" :key="report.title">
        <v-card class="report-card" variant="outlined">
          <v-card-title class="d-flex align-center">
            <v-icon :icon="report.icon" :color="report.color" class="mr-2"></v-icon>
            {{ report.title }}
          </v-card-title>
          <v-card-text class="text-medium-emphasis">
            {{ report.description }}
          </v-card-text>
          <v-card-actions>
            <v-btn
              :to="{ name: 'reports', query: { tab: report.tab } }"
              color="primary"
              variant="text"
            >
              Открыть отчёт
              <v-icon right>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
const dashboardCards = [
  {
    title: 'Сотрудники',
    description: 'Управление персоналом',
    icon: 'mdi-account-group',
    to: { name: 'employees' },
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  {
    title: 'Авторы',
    description: 'Каталог авторов',
    icon: 'mdi-feather',
    to: { name: 'authors' },
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
  },
  {
    title: 'Книги',
    description: 'Библиотека изданий',
    icon: 'mdi-book-open-page-variant',
    to: { name: 'books' },
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
  },
  {
    title: 'Контракты',
    description: 'Договоры на издание',
    icon: 'mdi-file-document-edit',
    to: { name: 'contracts' },
    gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
  },
  {
    title: 'Заказчики',
    description: 'База клиентов',
    icon: 'mdi-account-tie',
    to: { name: 'customers' },
    gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
  },
  {
    title: 'Заказы',
    description: 'Управление заказами',
    icon: 'mdi-cart',
    to: { name: 'orders' },
    gradient: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)'
  },
  {
    title: 'Отчёты',
    description: 'Аналитика и статистика',
    icon: 'mdi-chart-bar',
    to: { name: 'reports' },
    gradient: 'linear-gradient(135deg, #2D3E50 0%, #C9A959 100%)'
  }
]

const quickReports = [
  {
    title: 'Книги по авторам',
    description: 'Список всех изданных книг заданного автора',
    icon: 'mdi-book-account',
    color: 'primary',
    tab: 'books-by-author'
  },
  {
    title: 'Ответственные редакторы',
    description: 'Список ответственных редакторов для всех изданий',
    icon: 'mdi-account-edit',
    color: 'secondary',
    tab: 'chief-editors'
  },
  {
    title: 'Квартальный отчёт',
    description: 'Отчёт о контрактах за квартал с детализацией',
    icon: 'mdi-calendar-check',
    color: 'success',
    tab: 'quarterly'
  }
]
</script>

<style scoped>
.home-view {
  max-width: 1400px;
  margin: 0 auto;
}

.welcome-section {
  text-align: center;
  padding: 2rem;
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.05) 0%, rgba(var(--v-theme-secondary), 0.1) 100%);
  border-radius: 16px;
  border: 1px solid rgba(var(--v-theme-secondary), 0.2);
}

.welcome-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2.5rem;
  font-weight: 600;
  color: rgb(var(--v-theme-on-background));
  margin-bottom: 0.5rem;
}

.welcome-subtitle {
  font-size: 1.1rem;
  color: #666;
}

.dashboard-card {
  text-align: center;
  padding-top: 3rem;
  position: relative;
  overflow: visible;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.dashboard-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

.card-icon-wrapper {
  position: absolute;
  top: -24px;
  left: 50%;
  transform: translateX(-50%);
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.card-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.25rem;
  font-weight: 600;
  color: rgb(var(--v-theme-on-surface));
}

.section-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.5rem;
  font-weight: 600;
  color: rgb(var(--v-theme-on-background));
}

.report-card {
  height: 100%;
  transition: border-color 0.3s ease;
}

.report-card:hover {
  border-color: #C9A959;
}
</style>

