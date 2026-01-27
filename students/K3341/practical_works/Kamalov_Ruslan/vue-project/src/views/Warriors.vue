<template>
  <div class="app">
    <h1>Портал информации о войнах в онлайн РПГ</h1>
    <button v-on:click="fetchWarriors">Получить список войнов</button>
    <warrior-form />
    <warrior-list v-bind:warriors="warriors" />
  </div>
</template>

<script>
import WarriorForm from "@/components/WarriorForm.vue";
import WarriorList from "@/components/WarriorList.vue";
import axios from "axios";

export default {
  name: "WarriorsView",
  components: {
    WarriorForm,
    WarriorList,
  },

  data() {
    return {
      warriors: [],
    };
  },
  methods: {
    async fetchWarriors() {
      try {
        const response = await axios.get("http://62.109.28.95:8890/warriors/list/");
        console.log(response.data.results);
        this.warriors = response.data.results;
      } catch (e) {
        console.error("Ошибка при получении данных:", e);
        alert("Ошибка");
      }
    },
  },
  mounted() {
    this.fetchWarriors();
  },
};
</script>

<style scoped></style>
