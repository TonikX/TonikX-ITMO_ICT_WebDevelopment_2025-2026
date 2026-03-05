<script setup>
import {computed, onMounted, ref} from 'vue';
import axios from 'axios';
import {useRouter} from 'vue-router';

const cells = ref([]);
const router = useRouter();

const fetchCells = async () => {
  axios.get('/manufactory/cells').then(response => {
    cells.value = response.data;
  }).catch(error => console.log(error));
};

const groupedCages = computed(() => {
  return cells.value.reduce((acc, cell) => {
    const workshop = cell.workshop.title;
    if (!acc[workshop]) acc[workshop] = [];
    acc[workshop].push(cell);
    return acc;
  }, {});
});

onMounted(fetchCells);
</script>

<template>
  <div>
    <div v-for="(cells, workshop) in groupedCages" :key="workshop" class="mb-6">
      <h2 class="text-xl font-bold mb-4">{{ workshop }}</h2>
      <div class="grid grid-cols-4 gap-4">
        <div
            v-for="cell in cells"
            :key="cell.id"
            class="card cursor-pointer flex items-center justify-center shadow-md rounded-lg hover:shadow-lg transition"
            @click="router.push(`/cells/${cell.cell_code}`)"
        >
          <h3 class="font-bold text-lg">{{ cell.cell_code }}</h3>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  border: 1px solid #eaeaea;
  aspect-ratio: 1 / 1;
  padding: 1rem;
  text-align: center;
}

.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

</style>
