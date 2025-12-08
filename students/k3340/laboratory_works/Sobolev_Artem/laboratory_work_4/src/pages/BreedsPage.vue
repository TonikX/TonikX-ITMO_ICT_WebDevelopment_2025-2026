<template>
  <div class="breeds">
    <div class="breeds__actions">
      <Button
          label="Добавить породу"
          mode="violet"
          location="page-action"
          @click="showModal = true"
      />
      <!-- <Button
          label="Удалить породу"
          mode="violet"
          location="page-action"
      /> -->
    </div>

    <Modal
        v-if="showModal"
        title="Добавить породу"
        :formComponent="AddBreedForm"
        @close="showModal = false"
        @submit="handleSubmit"
    />

    <BreedsTable
        v-if="loading===false"
        :headers-item="[
            { key: 'name', label: 'Название' },
            { key: 'eggsNumber', label: 'Яиц в месяц' },
            { key: 'weight', label: 'Вес' },
          ]"
        :body-items="breeds"
        :height-size="breeds.length"
    />

    <Loader v-if="loading===true"/>
  </div>
</template>
<script setup>
import Button from "@/components/ui/Button.vue";
import Loader from "@/components/ui/Loader.vue";
import BreedsTable from "@/components/tables/BreedsTable.vue";
import useBreeds from "@/composables/useBreeds.js";
import Modal from "@/components/ui/Modal.vue";
import {ref} from "vue";
import AddBreedForm from "@/components/forms/AddBreedForm.vue";

const {breeds, loading, fetchBreeds} = useBreeds();
const showModal = ref(false);

const handleSubmit = async () => {
  await fetchBreeds();
  showModal.value = false;
};
</script>

<style lang="scss" scoped>
.breeds {
  &__header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }

  &__title {
    margin-bottom: 16px;
  }

  &__actions {
    margin-bottom: 16px;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    gap: 32px;
  }
}
</style>