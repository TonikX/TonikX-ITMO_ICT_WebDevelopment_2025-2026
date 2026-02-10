<script setup>
import {ref} from "vue";
import ScheduleModal from "@/components/ScheduleModal.vue";
import {getDayOfWeek} from "@/utils/functions.js";

defineProps({
  schedules: Array,
  employees: Array
});

const isEditModalVisible = ref(false);
const selectedSchedule = ref({})
const emits = defineEmits(["edit-schedule"]);


function handleEdit(schedule) {
  selectedSchedule.value = {...schedule};
  isEditModalVisible.value = true;
}

function handleUpdate(schedule) {
  emits("edit-schedule", schedule);
  isEditModalVisible.value = false;
}

</script>

<template>
  <v-data-table
      :headers="[
      { title: 'Сотрудник', value: 'employee.full_name' },
      { title: 'День недели', value: 'day_of_week' },
      { title: 'Этаж', value: 'floor' },
      { title: 'Действия', value: 'actions', sortable: false },
    ]"
      :items="schedules"
      class="elevation-1"
  >
    <template #item.day_of_week="{ item }">{{ getDayOfWeek(item.day_of_week) }}</template>
    <template #item.actions="{ item }">
      <v-btn color="primary" @click="handleEdit(item)">Редактировать</v-btn>
    </template>
  </v-data-table>

  <ScheduleModal
      v-model="isEditModalVisible"
      :schedule="selectedSchedule"
      :employees="employees"
      @save-schedule="handleUpdate"
  />
</template>