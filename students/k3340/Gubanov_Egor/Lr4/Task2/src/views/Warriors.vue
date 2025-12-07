<template>
  <div class="app">
    <h1>Портал информации о войнах в онлайн РПГ</h1>
    <button v-on:click="fetchWarriors">Получить список войнов</button>
    <warrior-form/>
    <warrior-list
        v-bind:warriors="warriors"
    />
  </div>
</template>

<script>
import WarriorForm from "@/components/WarriorForm.vue";
import WarriorList from "@/components/WarriorList.vue";
import axios from "axios";

export default {
  components: {
    WarriorForm, WarriorList
  },
  data() {
    return {
      warriors: []
    }
  },
  methods: {
    async fetchWarriors () {
      try {
        const response = await axios.get('http://62.109.28.95:8890/warriors/list/')
        console.log(response.data.results)
        this.warriors = response.data.results
      } catch (e) {
        alert('Ошибка')
      }
    }
  },
  mounted() {
    this.fetchWarriors()
  }
}
</script>

<style scoped>
button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 20px;
}

button:hover {
  background-color: #35a372;
}
</style>

