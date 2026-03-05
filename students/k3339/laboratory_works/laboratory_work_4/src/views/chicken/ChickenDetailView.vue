<script setup>
import {onMounted, ref} from 'vue';
import {useRoute} from 'vue-router';
import axios from "axios";

const chickenId = ref(null);
const chickenData = ref();
const breedData = ref();
const dietData = ref();
const isLoading = ref(true);
const isError = ref(false);
const route = useRoute();
chickenId.value = route.params.id;

async function fetchChicken() {
  isLoading.value = true;
  await axios
      .get(`manufactory/chicken/${chickenId.value}`)
      .then(response => {
        chickenData.value = response.data;
      })
      .catch(error => {
        console.error("Ошибка загрузки курицы", error);
        isError.value = true;
      })
}

async function fetchBreed(breedId) {
  isLoading.value = true;
  await axios
      .get(`manufactory/breeds/${breedId}`)
      .then(response => {
        breedData.value = response.data;
      })
      .catch(error => {
        console.error("Ошибка загрузки породы", error);
        isError.value = true;
      })
}

async function fetchDiet(dietId) {
  isLoading.value = true;
  await axios
      .get(`manufactory/diets/${dietId}`)
      .then(response => {
        dietData.value = response.data;
      })
      .catch(error => {
        console.error("Ошибка загрузки диеты", error);
        isError.value = true;
      })
}

onMounted(async () => {
  await fetchChicken();
  await fetchBreed(chickenData.value.breed)
  await fetchDiet(breedData.value.diet_number);
  isLoading.value = false;
})
</script>

<template>
  <div v-if="isLoading">Загрузка...</div>
  <div v-else-if="isError" class="error">Произошла ошибка при загрузке данных.</div>
  <div v-else>
    <v-card class="chicken-details-card" width="800">
      <v-card-title>
        Номер курицы: {{ chickenData.id}}
      </v-card-title>
      <v-card-subtitle>
        Вес: {{ chickenData.weight }} г
      </v-card-subtitle>
      <v-card-subtitle>
        Возраст: {{ chickenData.age }} л
      </v-card-subtitle>
      <v-divider></v-divider>
      <v-card-text>
        <h3>Яйценоскость:</h3>
        <p>{{ chickenData.egg_performance_month }} я/м</p>
      </v-card-text>
      <v-card-text>
        <h3>Описание породы:</h3>
        <p>Название: {{ breedData.name }}</p>
        <p>Средняя производительность {{ breedData.egg_performance_avg }}</p>
        <p>Средний вес: {{ breedData.weight_avg }} г</p>

      </v-card-text>
      <v-card-text>
        <h4>Описание диеты:</h4>
        <p>Номер диеты {{ dietData.id }}</p>
        <p>Описание {{ dietData.description }}</p>
        <p>Сезон: {{ dietData.season }} г</p>
      </v-card-text>
    </v-card>
  </div>
</template>

<style scoped>
.chicken-details-card {
  margin: 0 auto;
  padding: 16px;
}

.error {
  color: red;
  font-weight: bold;
  margin-top: 16px;
}
</style>