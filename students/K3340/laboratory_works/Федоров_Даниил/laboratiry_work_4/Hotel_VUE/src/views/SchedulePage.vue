<template>
  <v-container>
    <ScheduleCard v-for="day in 7" :key="day" :day="day" :schedules="getSchedules(day)" :employees="employees" />
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import ScheduleCard from '@/components/ScheduleCard.vue';

const schedules = ref([]);
const employees = ref([]);

const load = async () => {
  schedules.value = (await axios.get('/api/cleaning_schedules/')).data;

  employees.value = (await axios.get('/api/Employees/')).data;
};

const getSchedules = (day) => {
  return schedules.value.filter((s) => s.day_of_week == day);
};

onMounted(load);
</script>
