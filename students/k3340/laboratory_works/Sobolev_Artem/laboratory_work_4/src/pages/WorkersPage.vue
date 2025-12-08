<script setup>
import Button from "@/components/ui/Button.vue";
import WorkersTable from "@/components/tables/WorkersTable.vue";
import Loader from "@/components/ui/Loader.vue";
import {useWorkers} from "@/composables/useWorkers.js";

const {workers, loading} = useWorkers();
</script>

<template>
  <div class="workers">
    <div class="workers__actions">

      <Button
          label="Добавить сотрудника"
          mode="violet"
          location="page-action"
      />
      <!-- <Button
          label="Удалить сотрудника"
          mode="violet"
          location="page-action"
      /> -->
      <Button
          style="margin-left: auto;"
          href="/cages"
          class="table-template__button"
          label="Закрепленные клетки"
          icon-name="arrow-right"
          :icon-width="28"
          :icon-height="28"
      />
    </div>


    <WorkersTable
        v-if="loading===false"
        :headers-item="[
          { key: 'name', label: 'ФИО' },
          { key: 'position', label: 'Должность' },
          { key: 'salary', label: 'Зарплата' },
          { key: 'phoneNumber', label: 'Телефон'},
          { key: 'email', label: 'Почта'},
          { key: 'workersCells', label: 'Клетки' },
          { key: 'id', label: 'Ссылка'}
          ]"
        :body-items="workers"
        :height-size="workers.length"
    />

    <Loader v-if="loading===true" />
  </div>
</template>


<style lang="scss" scoped>
.workers {
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