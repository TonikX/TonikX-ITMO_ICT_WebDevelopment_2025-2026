<template>
  <div class="egg-productions">
    <div class="egg-productions__actions">
      <Button
          label="Добавить производство"
          mode="violet"
          location="page-action"
          @click="showModal = true"
      />
      <!-- <Button
          label="Удалить запись"
          mode="violet"
          location="page-action"
      /> -->
    </div>

    <Modal
        v-if="showModal"
        title="Добавить производство яиц"
        :form-component="AddEggProductionForm"
        @close="showModal = false"
        @submit="handleSubmit"
    />

    <EggProductionsTable
        v-if="loading===false"
        :headers-item="[
            { key: 'id', label: 'ID записи' },
            { key: 'chickenName', label: 'Имя курицы' },
            { key: 'month', label: 'Месяц' },
            { key: 'year', label: 'Год' },
            { key: 'count', label: 'Количество яиц' },
            { key: 'breedName', label: 'Порода' }
          ]"
        :body-items="eggProductions"
        :height-size="eggProductions.length"
    />

    <Loader v-if="loading===true"/>
  </div>
</template>

<script setup>
import Button from "@/components/ui/Button.vue";
import Loader from "@/components/ui/Loader.vue";
import EggProductionsTable from "@/components/tables/EggProductionsTable.vue";
import useEggProductions from "@/composables/useEggProductions.js";
import Modal from "@/components/ui/Modal.vue";
import {ref} from "vue";
import AddEggProductionForm from "@/components/forms/AddEggProductionForm.vue";

const {eggProductions, loading, fetchEggProductions} = useEggProductions();
const showModal = ref(false);

const handleSubmit = async () => {
  await fetchEggProductions();
  showModal.value = false;
};
</script>

<style lang="scss" scoped>
.egg-productions {
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