<template>
  <v-app>
    <!-- Боковое меню -->
    <v-navigation-drawer
        v-model="drawer"
        app
        permanent
        width="280"
        color="grey-darken-4"
        dark
    >
      <v-list density="compact" nav>
        <!-- Заголовок -->
        <v-list-item prepend-icon="mdi-shield-account" title="Админ-панель" class="mb-4">
          <template v-slot:append>
            <v-btn icon @click="drawer = !drawer" variant="text">
              <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
          </template>
        </v-list-item>

        <v-divider class="mb-4"></v-divider>

        <!-- Навигация -->
        <v-list-item
            prepend-icon="mdi-view-dashboard"
            title="Дашборд"
            value="dashboard"
            to="/admin"
            exact
        ></v-list-item>

        <v-list-group value="cars">
          <template v-slot:activator="{ props }">
            <v-list-item
                v-bind="props"
                prepend-icon="mdi-car"
                title="Автомобили"
            ></v-list-item>
          </template>
          <v-list-item
              title="Все автомобили"
              value="all-cars"
              to="/admin/cars"
          ></v-list-item>
          <v-list-item
              title="Добавить автомобиль"
              value="new-car"
              to="/admin/cars/new"
          ></v-list-item>
        </v-list-group>

        <!-- НОВОЕ: Добавляем обслуживание автомобилей в группу автомобилей -->
        <v-list-group value="maintenance">
          <template v-slot:activator="{ props }">
            <v-list-item
                v-bind="props"
                prepend-icon="mdi-wrench"
                title="Обслуживание"
            ></v-list-item>
          </template>
          <v-list-item
              title="Компании обслуживания"
              value="maintenance-companies"
              to="/admin/maintenance_companies"
          ></v-list-item>
          <v-list-item
              title="Добавить компанию"
              value="new-maintenance-company"
              to="/admin/maintenance_companies/new"
          ></v-list-item>
        </v-list-group>

        <v-list-item
            prepend-icon="mdi-file-document"
            title="Заявки на аренду"
            value="applications"
            to="/admin/applications"
        >
          <template v-slot:append>
            <v-badge v-if="pendingApplications > 0" color="error" :content="pendingApplications"></v-badge>
          </template>
        </v-list-item>

        <v-list-item
            prepend-icon="mdi-file-sign"
            title="Договоры аренда"
            value="leases"
            to="/admin/leases"
        ></v-list-item>

        <v-list-item
            prepend-icon="mdi-account-group"
            title="Клиенты"
            value="clients"
            to="/admin/clients"
        ></v-list-item>

        <v-list-item
            prepend-icon="mdi-file-sign"
            title="Отчеты"
            value="reports"
            to="/admin/reports"
        ></v-list-item>

        <v-divider class="my-4"></v-divider>

        <!-- Выход -->
        <v-list-item
            prepend-icon="mdi-logout"
            title="Выйти"
            @click="logout"
            class="logout-btn"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Шапка -->
    <v-app-bar app color="primary" dark flat>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>{{ pageTitle }}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon @click="goToPublic">
        <v-icon>mdi-home</v-icon>
        <v-tooltip activator="parent" location="bottom">На публичный сайт</v-tooltip>
      </v-btn>
      <v-avatar size="40" class="ml-4">
        <v-icon>mdi-account-circle</v-icon>
      </v-avatar>
      <span class="ml-2">{{ user?.username }}</span>
    </v-app-bar>

    <!-- Основной контент -->
    <v-main>
      <v-container fluid class="pa-6">
        <router-view></router-view>
      </v-container>
    </v-main>

    <!-- Футер -->
    <v-footer app color="grey lighten-3" class="px-4">
      <v-col class="text-center" cols="12">
        Лизинг Авто — Админ-панель • {{ new Date().getFullYear() }}
      </v-col>
    </v-footer>
  </v-app>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import axios from 'axios'

export default {
  name: 'AdminLayout',
  data() {
    return {
      drawer: true,
      pendingApplications: 0
    }
  },
  computed: {
    ...mapGetters('auth', ['user']),
    pageTitle() {
      const routeName = this.$route.name
      const titles = {
        'AdminDashboard': 'Дашборд',
        'AdminCars': 'Автомобили',
        'AdminCarCreate': 'Добавить автомобиль',
        'AdminCarEdit': 'Редактировать автомобиль',
        'AdminCarDetail': 'Детали автомобиля',
        'AdminApplications': 'Заявки на аренду',
        'AdminApplicationDetail': 'Детали заявки',
        'AdminLeases': 'Договоры аренды',
        'AdminLeaseDetail': 'Детали договора',
        'AdminClients': 'Клиенты',
        'AdminMaintenanceCompanyList': 'Компании по обслуживанию',
        'AdminMaintenanceCompanyCreate': 'Добавить компанию',
        'AdminMaintenanceCompanyDetail': 'Детали компании',
        'AdminMaintenanceCompanyEdit': 'Редактировать компанию',
        'CarMaintenance': 'Обслуживание автомобиля',
        'CarSpecificationDetail': 'Характеристики автомобиля',
        'CarSpecificationCreate': 'Добавление характеристик',
        'CarSpecificationEdit': 'Редактирование характеристик',
      }
      return titles[routeName] || 'Админ-панель'
    }
  },
  methods: {
    ...mapActions('auth', ['logout']),
    goToPublic() {
      this.$router.push('/')
    },

    handleLogout() {
      this.logout()
      this.$router.push('/login')
    }
  },
}
</script>

<style scoped>
.logout-btn:hover {
  color: #ff5252 !important;
}
.v-list-item--active {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
}
</style>