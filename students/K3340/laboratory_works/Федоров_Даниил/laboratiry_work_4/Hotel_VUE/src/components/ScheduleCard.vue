<template>
  <v-card class="pa-3 mb-4">
    <v-card-title>
      {{ dayName }}

      <v-btn icon variant="text" @click="show = !show">
        <i class="material-icons"> {{ show ? 'keyboard_arrow_up' : 'keyboard_arrow_down' }}</i>
      </v-btn>
    </v-card-title>

    <v-expand-transition>
      <div v-show="show">
        <v-card-text v-for="schedule in schedules" :key="schedule.id">
          Этаж {{ schedule.floor }}

          <v-select
            :items="employees"
            item-title="last_name"
            item-value="id"
            v-model="schedule.employee"
            @update:model-value="save(schedule)"
            density="compact"
          />
        </v-card-text>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';

const show = ref(false);

const props = defineProps({
  day: Number,
  schedules: Array,
  employees: Array,
});

const days = {
  1: 'Понедельник',
  2: 'Вторник',
  3: 'Среда',
  4: 'Четверг',
  5: 'Пятница',
  6: 'Суббота',
  7: 'Воскресенье',
};

const dayName = days[props.day];


const save = async (schedule) => {
  await axios.patch(`/api/cleaning_schedules/${schedule.id}/`, {
    employee: schedule.employee,
  });
};
</script>
