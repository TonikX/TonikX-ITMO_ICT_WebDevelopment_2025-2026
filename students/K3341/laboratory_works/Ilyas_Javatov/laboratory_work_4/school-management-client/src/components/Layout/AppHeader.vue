<template>
  <v-app-bar color="primary" dark app>
    <v-app-bar-nav-icon @click="$emit('toggle-drawer')" />

    <v-toolbar-title class="d-flex align-center">
      <v-icon class="mr-2">mdi-school</v-icon>
      <span class="font-weight-bold">{{ appTitle }}</span>
    </v-toolbar-title>

    <v-spacer />

    <v-btn icon class="mr-2" @click="toggleTheme">
      <v-icon>{{ isDark ? 'mdi-weather-sunny' : 'mdi-weather-night' }}</v-icon>
    </v-btn>

    <v-menu offset-y>
      <template v-slot:activator="{ props }">
        <v-btn variant="text" v-bind="props" class="text-capitalize">
          <v-avatar size="32" class="mr-2">
            <v-icon>mdi-account-circle</v-icon>
          </v-avatar>
          {{ user?.username || 'Пользователь' }}
          <v-icon right>mdi-chevron-down</v-icon>
        </v-btn>
      </template>
      <v-list>
        <v-list-item :to="{ name: 'Profile' }">
          <template v-slot:prepend>
            <v-icon>mdi-account-cog</v-icon>
          </template>
          <v-list-item-title>Профиль</v-list-item-title>
        </v-list-item>

        <v-divider />

        <v-list-item @click="logout">
          <template v-slot:prepend>
            <v-icon>mdi-logout</v-icon>
          </template>
          <v-list-item-title>Выйти</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'AppHeader',
  emits: ['toggle-drawer'],
  data() {
    return {
      isDark: false,
      appTitle: process.env.VUE_APP_TITLE || 'School Management System'
    }
  },
  computed: {
    ...mapState('auth', ['user'])
  },
  methods: {
    ...mapActions('auth', ['logout']),

    toggleTheme() {
      this.isDark = !this.isDark
      this.$vuetify.theme.global.name = this.isDark ? 'dark' : 'light'
    },

    async logout() {
      await this.$store.dispatch('auth/logout')
      this.$router.push('/login')
    }
  }
}
</script>