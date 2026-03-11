<template>
  <v-container>
    <ScheduleCard :schedules="schedules" :employees="employees" />
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

onMounted(load);
</script>