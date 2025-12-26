<template>
  <v-container>
    <v-breadcrumbs :items="breadcrumbs" class="pl-0">
      <template v-slot:divider>
        <v-icon>mdi-chevron-right</v-icon>
      </template>
    </v-breadcrumbs>

    <h1 class="text-h3 mb-4">Управление кабинетами</h1>

    <!-- Здесь будет компонент списка кабинетов -->
    <!-- Аналогично другим View -->

  </v-container>
</template>

<script>
export default {
  name: 'ClassroomsView',
  data() {
    return {
      loading: false,
      classrooms: []
    }
  },
  computed: {
    breadcrumbs() {
      return [
        { title: 'Главная', to: '/dashboard' },
        { title: 'Кабинеты', disabled: true }
      ]
    }
  }
}
</script>