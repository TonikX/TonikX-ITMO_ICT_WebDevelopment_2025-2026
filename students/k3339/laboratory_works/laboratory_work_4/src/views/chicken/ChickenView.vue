<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import ChickenList from "@/components/chicken/ChickenList.vue";
import ChickenModal from "@/components/chicken/ChickenModal.vue";

const chickens = ref([]);
const breeds = ref([]);
const isLoading = ref(false);
const isError = ref(false);
const isAddModalVisible = ref(false);
const cells = ref([]);
const diets = ref([])

async function fetchDiets() {
  await axios.get("manufactory/diets/").then(r => {
    diets.value = r.data
  })
}

async function fetchChickens() {
  isLoading.value = true;
  await axios
      .get('manufactory/chicken/')
      .then(response => {
        chickens.value = response.data;
      })
      .catch(error => {
        console.error("Ошибка загрузки куриц", error);
        isError.value = true;
      })
      .finally(() => {
        isLoading.value = false;
      });
}

async function fetchBreeds() {
  isLoading.value = true;
  await axios
      .get('manufactory/breeds/')
      .then(response => {
        breeds.value = response.data;
      })
      .catch(error => {
        console.error("Ошибка загрузки пород", error);
        isError.value = true;
      })
      .finally(() => {
        isLoading.value = false;
      });
}

async function addChicken(chicken) {
  const payload = normalizeChickenPayload(chicken)
  await axios.post(`manufactory/chicken/`, payload)
    .then(fetchChickens)
    .catch(error => {
      console.log("POST ERR:", error.response?.data)
      isError.value = true
    })
}

async function deleteChicken(id) {
  await axios.delete(`manufactory/chicken/${id}/`).then(() => {
    chickens.value = chickens.value.filter(item => item.id !== id);
  }).catch(error => {
    isError.value = true;
    console.error(`Ошибка удаления курицы: ${error}`);
  })
}

async function updateChicken(chicken) {
  const payload = normalizeChickenPayload(chicken)
  await axios.patch(`manufactory/chicken/${chicken.id}/`, payload)
    .then(fetchChickens)
    .catch(error => {
      console.log("PATCH ERR:", error.response?.data)
      isError.value = true
    })
}

async function fetchCells() {
  isLoading.value = true;
  await axios
    .get('manufactory/cells/')
    .then(response => {
      cells.value = response.data;
    })
    .catch(error => {
      console.error("Ошибка загрузки клеток", error);
      isError.value = true;
    })
    .finally(() => {
      isLoading.value = false;
    });
}

function toId(v) {
  return v && typeof v === "object" ? v.id : v
}

function normalizeChickenPayload(ch) {
  return {
    weight: Number(ch.weight),
    age: Number(ch.age),
    egg_performance_month: Number(ch.egg_performance_month),

    breed: toId(ch.breed),
    cell: toId(ch.cell),

    diet: toId(ch.diet),
  }
}

onMounted(async () => {
  await Promise.all([fetchChickens(), fetchBreeds(), fetchCells()])
});

</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <template v-if="isLoading">
      <v-skeleton-loader
          type="card"
          class="mt-4"
          max-width="500"
      ></v-skeleton-loader>
    </template>
    <template v-else>
      <h2>Список куриц</h2>
      <v-btn color="primary" @click="isAddModalVisible = true">Добавить курицу</v-btn>
      <ChickenList :chickens="chickens" :breeds="breeds" @delete-chicken="deleteChicken" @update-chicken="updateChicken"/>
    <ChickenModal
      v-model="isAddModalVisible"
      mode="add"
      :breeds="breeds"
      :cells="cells"
      @submit-chicken="addChicken"
    />
    </template>
  </div>
</template>

<style scoped>
.info {
  flex-grow: 1;
  margin-right: 10px;
}

.actions {
  display: flex;
  gap: 5px;
}

.actions > .v-btn {
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}
</style>
