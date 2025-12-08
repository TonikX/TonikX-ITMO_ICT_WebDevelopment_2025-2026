<template>
  <div class="rows">
    <div class="rows__actions">
      <Button
          label="Добавить ряд"
          mode="violet"
          location="page-action"
          @click="showModal = true"
      />
      <!-- <Button
          label="Удалить ряд"
          mode="violet"
          location="page-action"
      /> -->
      <Button
          style="margin-left: auto;"
          href="/cages"
          class="table-template__button"
          label="Клетки"
          icon-name="arrow-right"
          :icon-width="28"
          :icon-height="28"
      />
    </div>

    <Modal
        v-if="showModal"
        title="Добавить ряд"
        :form-component="AddRowForm"
        @close="showModal = false"
        @submit="handleSubmit"
    />

    <RowsTable
        v-if="loading === false"
        :headers-item="[
        { key: 'rowNumber', label: 'Номер ряда' },
        { key: 'workshopId', label: 'ID цеха' },
        { key: 'createdAt', label: 'Создан' },
        { key: 'updatedAt', label: 'Обновлен' },
      ]"
        :body-items="rows"
        :height-size="rows.length"
    />

    <Loader v-if="loading === true"/>
  </div>
</template>

<script setup>
import Button from "@/components/ui/Button.vue";
import Loader from "@/components/ui/Loader.vue";
import RowsTable from "@/components/tables/RowsTable.vue";
import Modal from "@/components/ui/Modal.vue";
import AddRowForm from "@/components/forms/AddRowForm.vue";
import useRows from "@/composables/useRows.js";
import { ref } from "vue";


const { rows, loading, fetchRows } = useRows();

const showModal = ref(false);

const handleSubmit = async () => {
  await fetchRows();
  showModal.value = false;
};
</script>

<style lang="scss" scoped>
.rows {
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
