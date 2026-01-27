<template>
  <v-card class="mb-4">
    <v-card-text>
      <p><strong>Сотрудник:</strong> {{ cleaningSchedule.staff.last_name }} {{cleaningSchedule.staff.first_name }} {{ cleaningSchedule.staff.patronymic }}</p>
      <p><strong>День Недели:</strong> {{ DayOfWeekLabel }}</p>
      <p><strong>Этаж id:</strong> {{ cleaningSchedule.floor.id }}</p>
    </v-card-text>
    <v-card-actions>
      <v-btn
        icon="mdi-eye"
        size="small"
        variant="text"
        :to="`/cleaningSchedules/${cleaningSchedule.id}`"
        title="Просмотр"
      ></v-btn>
      <v-btn
        icon="mdi-pencil"
        size="small"
        variant="text"
        :to="`/cleaningSchedules/${cleaningSchedule.id}/edit`"
        title="Редактировать"
      ></v-btn>
      <v-btn
        icon="mdi-delete"
        size="small"
        variant="text"
        color="error"
        @click="onDelete"
        title="Удалить"
        :disabled="disableDelete"
      ></v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  cleaningSchedule: {
    type: Object,
    required: true,
  },
  disableDelete: {
    type: Boolean,
    default: false,
  },
});

const daysOfWeek = {
  1: 'Понедельник',
  2: 'Вторник',
  3: 'Среда',
  4: 'Четверг',
  5: 'Пятница',
  6: 'Суббота',
  7: 'Воскресенье',
};
const DayOfWeekLabel = computed(() => {
  return daysOfWeek[props.cleaningSchedule.day_of_week] || props.cleaningSchedule.day_of_week;
});

const emit = defineEmits(['delete']);
const onDelete = () => {
  emit('delete');
};
</script>