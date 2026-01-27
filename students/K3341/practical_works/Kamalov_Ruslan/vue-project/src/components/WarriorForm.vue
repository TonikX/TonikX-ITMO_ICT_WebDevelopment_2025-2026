<template>
  <form @submit.prevent>
    <h1>Создание война</h1>
    <input v-model="warrior.name" class="input" type="text" placeholder="Имя" />
    <input v-model="warrior.race" class="input" type="text" placeholder="Расса" />
    <button class="btn" v-on:click="createWarrior">Cоздать</button>
  </form>
</template>

<script>
import axios from "axios";

export default {
  name: "WarriorForm",
  data() {
    return {
      warrior: {
        name: "",
        race: "",
      },
    };
  },
  methods: {
    createWarrior() {
      axios.post("http://62.109.28.95:8890/warrior/create1", {
        race: this.warrior.race,
        name: this.warrior.name,
      });
    },
  },
};
</script>

<style scoped>
.input {
  display: block;
  margin: 10px 0;
  padding: 8px;
  width: 200px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn:hover {
  background-color: #0056b3;
}
</style>
