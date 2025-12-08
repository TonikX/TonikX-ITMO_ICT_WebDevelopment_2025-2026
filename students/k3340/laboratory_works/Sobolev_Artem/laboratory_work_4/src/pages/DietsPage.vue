<template>
  <div class="diets">
    <div class="diets__actions">
      <Button
          label="Добавить диету"
          mode="violet"
          location="page-action"
          @click="showModal = true"
      />
      <!-- <Button
          label="Удалить диету"
          mode="violet"
          location="page-action"
      /> -->
    </div>

    <Modal
        v-if="showModal"
        title="Добавить диету"
        :form-component="AddDietForm"
        @close="showModal = false"
        @submit="handleSubmit"
    />

    <DietsTable
        v-if="loading===false"
        :headers-item="[
          { key: 'code', label: 'Код' },
          { key: 'title', label: 'Название' },
          { key: 'season', label: 'Сезон' },
          { key: 'description', label: 'Описание' },
        ]"
        :body-items="diets"
        :height-size="diets.length"
    />

    <Loader v-if="loading===true"/>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Button from "@/components/ui/Button.vue";
import DietsTable from "@/components/tables/DietsTable.vue";
import Loader from "@/components/ui/Loader.vue";
import useDiets from "@/composables/useDiets.js";
import AddDietForm from "@/components/forms/AddDietForm.vue";
import Modal from "@/components/ui/Modal.vue";

const { diets, loading, fetchDiets } = useDiets();
const showModal = ref(false);

const handleSubmit = async () => {
  await fetchDiets();
  showModal.value = false;
};

</script>

<style lang="scss" scoped>
.diets {
  &__actions {
    margin-bottom: 16px;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    gap: 32px;
  }

  &__form {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 24px;
    max-width: 400px;
  }

  &__select {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 8px;
  }
}
</style>
