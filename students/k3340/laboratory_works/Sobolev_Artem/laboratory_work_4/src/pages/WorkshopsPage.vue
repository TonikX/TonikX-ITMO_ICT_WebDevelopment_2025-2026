<template>
  <div class="workshops">
    <div class="workshops__actions">
      <Button
          label="Добавить цех"
          mode="violet"
          location="page-action"
          @click="showModal = true"
      />
      <!-- <Button
          label="Удалить цех"
          mode="violet"
          location="page-action"
      /> -->
      <Button
          style="margin-left: auto;"
          href="/rows"
          class="table-template__button"
          label="Ряды"
          icon-name="arrow-right"
          :icon-width="28"
          :icon-height="28"
      />
    </div>

    <Modal
        v-if="showModal"
        title="Добавить цех"
        :formComponent="AddWorkshopForm"
        @close="showModal = false"
        @submit="handleSubmit"
    />

    <WorkshopsTable
        v-if="loading===false"
        :headers-item="[
            { key: 'workshopNumber', label: 'Номер цеха' },
            { key: 'id', label: 'ID' },
          ]"
        :body-items="workshops"
        :height-size="workshops.length"
    />

    <Loader v-if="loading===true"/>
  </div>
</template>

<script setup>
import Button from "@/components/ui/Button.vue";
import Loader from "@/components/ui/Loader.vue";
import WorkshopsTable from "@/components/tables/WorkshopsTable.vue";
import useWorkshops from "@/composables/useWorkshops.js";
import Modal from "@/components/ui/Modal.vue";
import {ref} from "vue";
import AddWorkshopForm from "@/components/forms/AddWorkshopForm.vue";

const {workshops, loading, fetchWorkshops} = useWorkshops();
const showModal = ref(false);

const handleSubmit = async () => {
  await fetchWorkshops();
  showModal.value = false;
};
</script>

<style lang="scss" scoped>
.workshops {
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
