<template>
  <form @submit.prevent>
    <h1>Создание война</h1>
    <input
        v-model="warrior.name"
        class="input"
        type="text"
        placeholder="Имя">
    <input
        v-model="warrior.race"
        class="input"
        type="text"
        placeholder="Расса">
    <button class="btn" v-on:click="createWarrior">Cоздать</button>
  </form>
</template>

<script>
import axios from "axios";

export default {
  name: "WarriorForm",
  data () {
    return {
      warrior: {
        name: '',
        race: ''
      }
    }
  },
  methods: {
    createWarrior() {
      axios.post('http://62.109.28.95:8890/warrior/create1', {
        race: this.warrior.race,
        name: this.warrior.name,
      });
    }
  }
}
</script>

<style scoped>

</style>

