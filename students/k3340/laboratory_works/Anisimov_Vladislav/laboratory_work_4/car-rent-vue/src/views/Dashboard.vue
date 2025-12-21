<!-- views/Dashboard.vue -->
<template>
  <v-container class="py-8">
    <v-row justify="center">
      <v-col cols="12" class="text-center">

        <h1 class="text-h3 font-weight-bold mb-2">Управление прокатом авто</h1>
        <p class="text-h6 text-medium-emphasis mb-8">
          Выберите раздел для управления системой аренды автомобилей
        </p>
      </v-col>
    </v-row>

    <v-row>
      <v-col
        v-for="card in cards"
        :key="card.id"
        cols="12"
        sm="6"
        md="4"
        lg="4"
      >
        <v-card
          :to="card.route"
          height="100%"
          hover
          class="transition-swing"
        >
          <v-card-item>
            <template v-slot:prepend>
              <v-avatar
                :color="card.color"
                size="56"
                class="mr-4"
              >
                <v-icon :icon="card.icon" size="32"></v-icon>
              </v-avatar>
            </template>
            
            <v-card-title class="text-h6 font-weight-bold">
              {{ card.title }}
            </v-card-title>
            
            <v-card-subtitle class="text-body-1">
              {{ card.description }}
            </v-card-subtitle>
          </v-card-item>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              :color="card.color"
              variant="text"
              append-icon="mdi-arrow-right"
            >
              Перейти
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'

const quickAction = ref(null)

const cards = ref([
  {
    id: 1,
    title: 'Автомобили',
    description: 'Управление автомобилями и ценами на прокат',
    icon: 'mdi-car',
    route: '/cars',
    color: 'primary'
  },
  {
    id: 2,
    title: 'Характеристики',
    description: 'Технические характеристики автомобилей',
    icon: 'mdi-cog',
    route: '/specifications',
    color: 'blue'
  },
  {
    id: 3,
    title: 'Описания',
    description: 'Модели и описания автомобилей',
    icon: 'mdi-text-box-multiple',
    route: '/descriptions',
    color: 'indigo'
  },
  {
    id: 4,
    title: 'Контракты',
    description: 'Договоры аренды с клиентами',
    icon: 'mdi-file-document',
    route: '/contracts',
    color: 'orange'
  },
  {
    id: 5,
    title: 'Клиенты',
    description: 'База клиентов',
    icon: 'mdi-account-group',
    route: '/clients',
    color: 'green'
  },
  {
    id: 6,
    title: 'Персонал',
    description: 'Сотрудники компании',
    icon: 'mdi-briefcase-account',
    route: '/staff',
    color: 'deep-purple'
  }
])
</script>

<style scoped>
.transition-swing {
  transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.transition-swing:hover {
  transform: translateY(-4px);
}
</style>