<template>
  <div class="cages">
    <div class="cages__actions">
      <Button
          label="Добавить клетку"
          mode="violet"
          location="page-action"
          @click="showModal = true"
      />
      <!-- <Button
          label="Удалить клетку"
          mode="violet"
          location="page-action"
      /> -->
    </div>

    <Modal
        v-if="showModal"
        title="Добавить клетку"
        :form-component="AddCageForm"
        @close="showModal = false"
        @submit="handleSubmit"
    />

    <CagesTable
        v-if="loading===false"
        :headers-item="[
            { key: 'id', label: 'ID клетки' },
            { key: 'cageNumber', label: 'Номер клетки' },
            { key: 'rowId', label: 'ID ряда' },
            { key: 'workshopId', label: 'ID цеха' },
          ]"
        :body-items="cages"
        :height-size="cages.length"
    />

    <Loader v-if="loading===true"/>
  </div>
</template>

<script setup>
import Button from "@/components/ui/Button.vue";
import Loader from "@/components/ui/Loader.vue";
import CagesTable from "@/components/tables/CagesTable.vue";
import useCages from "@/composables/useCages.js";
import Modal from "@/components/ui/Modal.vue";
import {ref} from "vue";
import AddCageForm from "@/components/forms/AddCageForm.vue";

const {cages, loading, fetchCages} = useCages();
const showModal = ref(false);

const handleSubmit = async () => {
  await fetchCages();
  showModal.value = false;
};
</script>

<style lang="scss" scoped>
.cages {
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