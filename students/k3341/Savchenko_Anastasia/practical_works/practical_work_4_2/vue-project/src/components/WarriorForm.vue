<template>
  <form @submit.prevent>
    <h1>Создание война</h1>
    <input
      v-model="warrior.name"
      class="input"
      type="text"
      placeholder="Имя"
    >
    <input
      v-model="warrior.race"
      class="input"
      type="text"
      placeholder="Раса"
    >
    <button class="btn" @click="createWarrior">Создать</button>
  </form>
</template>

<script>
import axios from 'axios'

export default {
  name: 'WarriorForm',
  data() {
    return {
      warrior: {
        name: '',
        race: ''
      }
    }
  },
  methods: {
    async createWarrior() {
      try {
        await axios.post('http://62.109.28.95:8890/warriors/create/', this.warrior)
        alert('Войн создан!')
        this.warrior.name = ''
        this.warrior.race = ''
      } catch (error) {
        console.error(error)
        alert('Ошибка при создании')
      }
    }
  }
}
</script>

<style scoped>
</style>