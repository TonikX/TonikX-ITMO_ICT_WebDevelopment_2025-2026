<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './store/auth'

const drawer = ref(true)
const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const isAuthed = computed(() => !!auth.token)
const isAdmin = computed(() => auth.isAdmin)
const user = computed(() => auth.user)
const mainClasses = computed(() => ({
  'with-drawer': isAuthed.value && drawer.value,
}))

const catalogLinks = [
  { title: 'Manufacturers', to: '/catalog/manufacturers', icon: 'mdi-factory' },
  { title: 'Products', to: '/catalog/products', icon: 'mdi-package-variant' },
  { title: 'Broker Companies', to: '/catalog/broker-companies', icon: 'mdi-domain' },
  { title: 'Brokers', to: '/catalog/brokers', icon: 'mdi-account-tie' },
]

const tradingLinks = [
  { title: 'Batches', to: '/trading/batches', icon: 'mdi-truck-delivery' },
  { title: 'Batch Items', to: '/trading/batch-items', icon: 'mdi-cube-scan' },
]

const reportLinks = [
  { title: 'Product Quantities', to: '/reports/product-quantities', icon: 'mdi-chart-bar' },
  { title: 'Top Manufacturer', to: '/reports/top-manufacturer', icon: 'mdi-trophy' },
  { title: 'Unsold Products', to: '/reports/unsold-products', icon: 'mdi-magnify' },
  { title: 'Expired Items', to: '/reports/expired-items', icon: 'mdi-alert' },
  { title: 'Broker Salaries', to: '/reports/broker-salaries', icon: 'mdi-cash' },
  { title: 'Latest Trades', to: '/reports/latest-trades', icon: 'mdi-file-chart' },
]

const navLinks = [
  { title: 'Dashboard', to: '/', icon: 'mdi-view-dashboard' },
  { title: 'Profile', to: '/profile', icon: 'mdi-account-circle' },
]

const catalogVisible = computed(() => (isAdmin.value ? catalogLinks : []))

const isActive = (path: string) => route.path === path

const logout = async () => {
  await auth.logout()
}
</script>

<template>
  <v-app class="app-shell">
    <v-layout>
      <v-navigation-drawer
        v-if="isAuthed"
        v-model="drawer"
        app
        permanent
        class="app-nav"
        width="260"
      >
        <v-list nav density="compact">
          <v-list-item
            v-for="item in navLinks"
            :key="item.to"
            :title="item.title"
            :prepend-icon="item.icon"
            :to="item.to"
            :active="isActive(item.to)"
            link
          />
        </v-list>

        <v-divider class="my-2" />

        <v-list v-if="catalogVisible.length" nav density="compact" subheader>
          <v-list-subheader>Catalog</v-list-subheader>
          <v-list-item
            v-for="item in catalogVisible"
            :key="item.to"
            :title="item.title"
            :prepend-icon="item.icon"
            :to="item.to"
            :active="isActive(item.to)"
            link
          />
        </v-list>

        <v-list nav density="compact" subheader>
          <v-list-subheader>Trading</v-list-subheader>
          <v-list-item
            v-for="item in tradingLinks"
            :key="item.to"
            :title="item.title"
            :prepend-icon="item.icon"
            :to="item.to"
            :active="isActive(item.to)"
            link
          />
        </v-list>

        <v-list nav density="compact" subheader>
          <v-list-subheader>Reports</v-list-subheader>
          <v-list-item
            v-for="item in reportLinks"
            :key="item.to"
            :title="item.title"
            :prepend-icon="item.icon"
            :to="item.to"
            :active="isActive(item.to)"
            link
          />
        </v-list>
      </v-navigation-drawer>

      <v-app-bar v-if="isAuthed" app color="primary" dark flat class="app-bar">
        <v-app-bar-nav-icon @click="drawer = !drawer" />
        <v-toolbar-title>Trading Desk</v-toolbar-title>
        <v-spacer />
        <v-btn icon="mdi-account-circle" variant="text" />
        <span class="mr-4">{{ user?.username }}</span>
        <v-btn color="secondary" @click="router.push({ name: 'profile' })">Profile</v-btn>
        <v-btn color="white" variant="text" class="ml-2" @click="logout">Logout</v-btn>
      </v-app-bar>

      <v-main :class="['app-main', mainClasses]">
        <router-view />
      </v-main>
    </v-layout>
  </v-app>
</template>
