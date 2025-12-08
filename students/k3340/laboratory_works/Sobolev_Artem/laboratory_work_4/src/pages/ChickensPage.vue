<template>
  <div class="chickens">
    <div class="chickens__actions">
      <Button
          label="Добавить курицу"
          mode="violet"
          location="page-action"
          @click="showModal = true"
      />
      <!-- <Button
          label="Удалить курицу"
          mode="violet"
          location="page-action"
          @click="showDeleteModal = true"
      /> -->
      <Button
          style="margin-left: auto;"
          href="/breeds"
          class="table-template__button"
          label="Породы куриц"
          icon-name="arrow-right"
          :icon-width="28"
          :icon-height="28"
      />
    </div>

    <Modal
      v-if="showModal"
      title="Добавить курицу"
      :form-component="AddChickenForm"
      @close="showModal = false"
      @submit="handleSubmit"
    />

    <!-- <Modal
      v-if="showDeleteModal"
      title="Удалить курицу"
      :form-component="DeleteChickenForm"
      @close="showDeleteModal = false"
      @submit="handleDeleteSubmit"
    /> -->

    <ChickensTable
        v-if="loading===false"
        :headers-item="[
            { key: 'id', label: 'ID' },
            { key: 'name', label: 'Имя' },
            { key: 'breedName', label: 'Порода' },
            { key: 'weight', label: 'Вес' },
            { key: 'eggs', label: 'Яиц в месяц' },
            { key: 'age', label: 'Возраст' },
            { key: 'birthDate', label: 'Дата рождения' },
            { key: 'link', label: 'Ссылка' }
          ]"
        :body-items="sortedChickens"
        :height-size="sortedChickens.length"
        :sort-key="sortKey"
        @sort="handleSort"
    />

    <Loader v-if="loading===true"/>
  </div>
</template>

<script setup>
import Button from "@/components/ui/Button.vue";
import ChickensTable from "@/components/tables/ChickensTable.vue";
import Loader from "@/components/ui/Loader.vue";
import {useChickens} from "@/composables/useChickens.js";
import Modal from "@/components/ui/Modal.vue";
import AddChickenForm from "@/components/forms/AddChickenForm.vue";
import {ref, computed} from "vue";

const {chickens, loading, fetchChickens} = useChickens();
const showModal = ref(false);
const showDeleteModal = ref(false);
const sortKey = ref(null);
const sortDirection = ref('asc');

const handleSort = (key) => {
  if (sortKey.value === key) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortKey.value = key;
    sortDirection.value = 'asc';
  }
};

const sortedChickens = computed(() => {
  if (!sortKey.value) {
    return chickens.value;
  }

  const sorted = [...chickens.value];
  const direction = sortDirection.value === 'asc' ? 1 : -1;

  sorted.sort((a, b) => {
    let aValue = a[sortKey.value];
    let bValue = b[sortKey.value];

    if (aValue == null && bValue == null) return 0;
    if (aValue == null) return direction;
    if (bValue == null) return -direction;

    if (sortKey.value === 'name' || sortKey.value === 'breedName') {
      aValue = String(aValue).toLowerCase();
      bValue = String(bValue).toLowerCase();
      return aValue.localeCompare(bValue) * direction;
    } else if (sortKey.value === 'id' || sortKey.value === 'weight' || sortKey.value === 'eggs') {
      aValue = Number(aValue) || 0;
      bValue = Number(bValue) || 0;
      return (aValue - bValue) * direction;
    } else if (sortKey.value === 'age') {
      aValue = a.birthDate ? new Date(a.birthDate).getTime() : 0;
      bValue = b.birthDate ? new Date(b.birthDate).getTime() : 0;
      return (aValue - bValue) * -direction;
    } else if (sortKey.value === 'birthDate') {
      aValue = new Date(aValue).getTime();
      bValue = new Date(bValue).getTime();
      return (aValue - bValue) * direction;
    }

    return 0;
  });

  return sorted;
});

const handleSubmit = async () => {
  await fetchChickens();
  showModal.value = false;
};

const handleDeleteSubmit = async () => {
  await fetchChickens();
  showDeleteModal.value = false;
};
</script>

<style lang="scss" scoped>
.chickens {
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