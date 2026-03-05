<script setup>

import {ref} from "vue";
import ChickenModal from "@/components/chicken/ChickenModal.vue";

defineProps({
  chickens: {
    type: Array
  },
  breeds: {
    type: Array
  }
})

const emits = defineEmits(["delete-chicken", "update-chicken"]);

const isEditModalVisible = ref(false);
const selectedChicken = ref({});

function handleEdit(chicken) {
  selectedChicken.value = {...chicken};
  isEditModalVisible.value = true;
}

function handleUpdateChicken(chicken) {
  emits("update-chicken", chicken);
  isEditModalVisible.value = false
}

function deleteChicken(id) {
  emits("delete-chicken", id);
}

</script>

<template>
  <div class="items-list">
    <template v-for="chicken in chickens" :key="chicken.id">
      <v-card class="chicken-card" width="600">
        <v-card-title>
          Курица: {{ chicken.id }}
        </v-card-title>
        <v-card-subtitle>Порода: {{ chicken.breed.name }}</v-card-subtitle>
        <v-card-subtitle>Возраст: {{ chicken.age }} г</v-card-subtitle>
        <v-card-actions class="chicken-card-actions">
          <v-btn
              size="x-small"
              icon
              :to="`/chickens/${chicken.id}`"
          >
            <v-icon size="18">mdi-eye</v-icon>
          </v-btn>
          <v-btn
              size="x-small"
              icon
              @click="handleEdit(chicken)"
          >
            <v-icon size="18">mdi-pencil</v-icon>
          </v-btn>
          <v-btn
              size="x-small"
              icon
              color="error"
              @click="deleteChicken(chicken.id)"
          >
            <v-icon size="18">mdi-delete</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
      <div v-if="chickens.length === 0">
        Нет данных для отображения.
      </div>
    </template>

    <ChickenModal
        v-model="isEditModalVisible"
        :chickenData="selectedChicken"
        :breeds="breeds"
        mode="edit"
        @submit-chicken="handleUpdateChicken"
    />
  </div>
</template>

<style scoped>
.items-list {
  max-width: 600px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

.chicken-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
}

.chicken-card {
  margin-bottom: 16px;
  position: relative;
  padding-bottom: 50px;
}

.chicken-card-actions {
  position: absolute;
  bottom: 10px;
  right: 10px;
  display: flex;
  gap: 8px;
}
</style>