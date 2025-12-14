<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>Добро пожаловать в систему управления гостиницей</h1>
      </v-col>
      <v-col cols="12" md="4" v-for="card in cards" :key="card.title">
        <v-card>
          <v-card-title>{{ card.title }}</v-card-title>
          <v-card-text>{{ card.text }}</v-card-text>
          <v-card-actions>
            <v-btn :to="card.link" color="primary">Перейти</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { useAuth } from '../composables/useAuth'

export default {
  name: 'Home',
  setup() {
    const { isAuthenticated } = useAuth()
    
    const cards = [
      {
        title: 'Номера',
        text: 'Управление номерами гостиницы',
        link: '/rooms'
      },
      {
        title: 'Клиенты',
        text: 'Управление клиентами',
        link: '/guests'
      },
      {
        title: 'Проживания',
        text: 'Управление проживаниями',
        link: '/stays'
      }
    ]

    return { cards, isAuthenticated }
  }
}
</script>

