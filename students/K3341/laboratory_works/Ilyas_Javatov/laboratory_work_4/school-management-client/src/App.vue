<template>
  <v-app>
    <AppHeader
      v-if="showHeader"
      @toggle-drawer="drawer = !drawer"
    />

    <AppSidebar
      v-if="showSidebar"
      v-model="drawer"
    />

    <v-main>
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </v-main>

    <AppFooter v-if="showFooter" />

    <!-- Глобальное уведомление о загрузке -->
    <v-overlay
      :model-value="loading"
      class="align-center justify-center"
      persistent
    >
      <v-progress-circular
        indeterminate
        size="64"
        color="primary"
      />
      <p class="mt-4 text-white">Загрузка...</p>
    </v-overlay>

    <!-- Глобальное уведомление об ошибке -->
    <v-snackbar
      v-model="showError"
      color="error"
      :timeout="5000"
      location="top"
    >
      {{ errorMessage }}
      <template v-slot:actions>
        <v-btn
          color="white"
          variant="text"
          @click="showError = false"
        >
          Закрыть
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script>
import { mapState } from 'vuex'
import AppHeader from './components/Layout/AppHeader.vue'
import AppSidebar from './components/Layout/AppSidebar.vue'
import AppFooter from './components/Layout/AppFooter.vue'

export default {
  name: 'App',
  components: {
    AppHeader,
    AppSidebar,
    AppFooter
  },
  data() {
    return {
      drawer: true
    }
  },
  computed: {
    ...mapState(['loading', 'error']),
    showHeader() {
      const guestPages = ['Login', 'Register', 'Home']
      return !guestPages.includes(this.$route.name)
    },
    showSidebar() {
      return this.$route.meta.requiresAuth
    },
    showFooter() {
      return !['Login', 'Register'].includes(this.$route.name)
    },
    showError: {
      get() {
        return !!this.error
      },
      set(value) {
        if (!value) {
          this.$store.dispatch('clearError')
        }
      }
    },
    errorMessage() {
      return this.error || ''
    }
  },
  watch: {
    error(newError) {
      if (newError) {
        console.error('Global error:', newError)
      }
    }
  },
  async created() {
    // Проверяем аутентификацию при загрузке приложения
    await this.$store.dispatch('auth/checkAuth')
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  font-family: 'Roboto', sans-serif;
}

#app {
  min-height: 100vh;
}

/* Анимации переходов */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Кастомные стили */
.v-application {
  background-color: #f5f5f5 !important;
}

/* Стили для скроллбара */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Утилитарные классы */
.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }
.gap-5 { gap: 20px; }
.gap-6 { gap: 24px; }

.h-100 { height: 100%; }
.w-100 { width: 100%; }
</style>