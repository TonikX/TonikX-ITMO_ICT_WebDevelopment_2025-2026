<template>
  <v-app class="app-background">
    <v-app-bar color="transparent" elevation="0" height="70" class="blur-app-bar">
      <v-container class="d-flex align-center py-0">
        <v-app-bar-title 
          class="font-weight-bold text-uppercase d-flex align-center cursor-pointer logo-title" 
          @click="$router.push('/')"
        >
          <div class="logo-icon-box mr-3">
            <v-icon icon="mdi-airplane-takeoff" color="white" size="24"></v-icon>
          </div>
          <span class="text-white tracking-widest">Airlines Admin Panel</span>
        </v-app-bar-title>

        <v-spacer></v-spacer>

        <div v-if="isAuthenticated" class="d-none d-md-flex gap-2">
          <v-btn to="/planes" rounded="lg" variant="text" class="nav-btn">
            <v-icon start>mdi-wrench</v-icon>Ремонт
          </v-btn>
          <v-btn to="/routes" rounded="lg" variant="text" class="nav-btn">
            <v-icon start>mdi-chart-timeline-variant</v-icon>Маршруты
          </v-btn>
          <v-btn to="/seats" rounded="lg" variant="text" class="nav-btn">
            <v-icon start>mdi-seat-passenger</v-icon>Места
          </v-btn>
          
          <div class="divider-vertical mx-3"></div>
          
          <v-btn to="/profile" rounded="pill" color="secondary" variant="flat" class="profile-btn px-4">
            <v-icon start>mdi-account</v-icon>Профиль
          </v-btn>
        </div>

        <div v-else>
          <v-btn to="/login" variant="outlined" color="white" rounded="pill" class="px-6">Войти</v-btn>
        </div>
      </v-container>
    </v-app-bar>

    <v-main>
      <router-view v-slot="{ Component }">
        <transition name="page-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </v-main>
  </v-app>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const isAuthenticated = computed(() => {
  return route.path !== '/login' && route.path !== '/register';
});
</script>

<style scoped>
.app-background {
  background: transparent !important;
}

.blur-app-bar {
  background: rgba(15, 23, 42, 0.6) !important;
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.logo-title {
  cursor: pointer;
  letter-spacing: 2px;
  font-size: 1.2rem;
}

.logo-icon-box {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(79, 172, 254, 0.4);
}

.nav-btn {
  color: #94a3b8 !important;
  text-transform: none !important;
  font-weight: 500;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.nav-btn:hover, .nav-btn.v-btn--active {
  color: #ffffff !important;
  background: rgba(255, 255, 255, 0.05);
}

.divider-vertical {
  width: 1px;
  background-color: rgba(255, 255, 255, 0.1);
  height: 24px;
  align-self: center;
}

.profile-btn {
  background: linear-gradient(45deg, #FF512F 0%, #DD2476 100%) !important;
  font-weight: bold;
  box-shadow: 0 4px 15px rgba(221, 36, 118, 0.4);
}

.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.page-fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.page-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
