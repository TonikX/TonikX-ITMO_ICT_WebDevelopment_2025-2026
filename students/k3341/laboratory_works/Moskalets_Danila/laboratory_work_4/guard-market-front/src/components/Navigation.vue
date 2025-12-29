<template>
  <v-app-bar color="primary" density="compact">
    <template v-slot:prepend>
      <v-app-bar-nav-icon @click="toggleDrawer"></v-app-bar-nav-icon>
    </template>

    <v-app-bar-title>Guard Market</v-app-bar-title>

    <template v-slot:append>
      <v-btn v-if="!authStore.isAuthenticated" to="/login" variant="text">
        Войти
      </v-btn>
      <v-menu v-else>
        <template v-slot:activator="{ props }">
          <v-btn v-bind="props" variant="text">
            <v-icon start>mdi-account</v-icon>
            {{ authStore.user?.name }}
            <v-badge
                v-if="authStore.hasCompany"
                color="success"
                dot
                inline
                class="ml-2"
            ></v-badge>
          </v-btn>
        </template>
        <v-list>
          <v-list-item to="/profile">
            <template v-slot:prepend>
              <v-icon>mdi-account</v-icon>
            </template>
            Профиль
          </v-list-item>

          <v-list-item v-if="authStore.hasCompany" :to="`/companies/${authStore.company.id}`">
            <template v-slot:prepend>
              <v-icon>mdi-office-building</v-icon>
            </template>
            Моя компания
          </v-list-item>

          <v-list-item v-if="authStore.hasCompany" to="/company">
            <template v-slot:prepend>
              <v-icon>mdi-cog</v-icon>
            </template>
            Управление компанией
          </v-list-item>

          <v-divider></v-divider>

          <v-list-item to="/favorites">
            <template v-slot:prepend>
              <v-icon>mdi-heart</v-icon>
            </template>
            Избранное
            <v-badge
                v-if="authStore.user?.favorites?.length"
                :content="authStore.user.favorites.length"
                color="primary"
                inline
                class="ml-2"
            ></v-badge>
          </v-list-item>

          <v-list-item to="/requests">
            <template v-slot:prepend>
              <v-icon>mdi-format-list-bulleted</v-icon>
            </template>
            Мои заявки
            <v-badge
                v-if="authStore.user?.service_requests?.length"
                :content="authStore.user.service_requests.length"
                color="primary"
                inline
                class="ml-2"
            ></v-badge>
          </v-list-item>

          <v-divider></v-divider>

          <v-list-item @click="authStore.logout">
            <template v-slot:prepend>
              <v-icon>mdi-logout</v-icon>
            </template>
            Выйти
          </v-list-item>
        </v-list>
      </v-menu>
    </template>
  </v-app-bar>

  <v-navigation-drawer v-model="drawer" temporary>
    <v-list>
      <v-list-item prepend-icon="mdi-home" title="Главная" to="/"></v-list-item>

      <template v-if="!authStore.isAuthenticated">
        <v-list-item prepend-icon="mdi-login" title="Вход" to="/login"></v-list-item>
        <v-list-item prepend-icon="mdi-account-plus" title="Регистрация" to="/register"></v-list-item>
      </template>

      <template v-else>
        <v-list-item
            prepend-icon="mdi-account"
            title="Профиль"
            to="/profile"
        ></v-list-item>

        <v-list-item
            v-if="authStore.hasCompany"
            :to="`/companies/${authStore.company.id}`"
            prepend-icon="mdi-office-building"
            :title="authStore.company?.name || 'Моя компания'"
        ></v-list-item>

        <v-list-item
            v-if="authStore.hasCompany"
            prepend-icon="mdi-cog"
            title="Управление компанией"
            to="/company"
        ></v-list-item>

        <v-list-item
            prepend-icon="mdi-heart"
            title="Избранное"
            to="/favorites"
        >
          <template v-slot:append>
            <v-badge
                v-if="authStore.user?.favorites?.length"
                :content="authStore.user.favorites.length"
                color="primary"
                size="small"
            ></v-badge>
          </template>
        </v-list-item>

        <v-list-item
            prepend-icon="mdi-format-list-bulleted"
            title="Мои заявки"
            to="/requests"
        >
          <template v-slot:append>
            <v-badge
                v-if="authStore.user?.service_requests?.length"
                :content="authStore.user.service_requests.length"
                color="primary"
                size="small"
            ></v-badge>
          </template>
        </v-list-item>

        <v-divider></v-divider>

        <v-list-item
            prepend-icon="mdi-shield-account"
            title="Все компании"
            to="/companies"
        ></v-list-item>

        <v-list-item
            prepend-icon="mdi-tools"
            title="Все услуги"
            to="/services"
        ></v-list-item>

        <v-list-item
            prepend-icon="mdi-star"
            title="Мои отзывы"
            to="/reviews"
        ></v-list-item>
      </template>
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const drawer = ref(false)

const toggleDrawer = () => {
  drawer.value = !drawer.value
}
</script>