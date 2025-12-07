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
.input {
  display: block;
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.btn {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 10px;
}

.btn:hover {
  background-color: #35a372;
}
</style>

