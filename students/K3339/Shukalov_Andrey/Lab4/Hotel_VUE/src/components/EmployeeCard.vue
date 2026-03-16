<template>
  <v-card :class="employee">
    <v-card-title primary-title> {{ employee.last_name }} {{ employee.first_name }} {{ employee.middle_name }} </v-card-title>
    <v-card-text v-if="employee.dismissed == true">
      <p>Уволен</p>
    </v-card-text>
    <v-card-text v-else-if="employee.dismissed == false">
      <p>Работает</p>
    </v-card-text>
    <v-card-actions>
      <v-btn v-if="employee.dismissed == false" @click="dismiss(employee.id)" color="red" small>Уволить</v-btn>
      <v-spacer></v-spacer>
      <v-btn icon @click="show = !show">
        <i class="material-icons">{{ show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</i>
      </v-btn>
    </v-card-actions>
    <v-slide-y-transition>
      <v-card-text v-show="show" v-if="employee.dismissed == true">
        <p>Принят на работу: {{ employee.add_date }}</p>
        <p>Уволен: {{ employee.delete_date }}</p>
      </v-card-text>
      <v-card-text v-else-if="employee.dismissed == false" v-show="show">
        <p>Принят на работу: {{ employee.add_date }}</p>
      </v-card-text>
    </v-slide-y-transition>
  </v-card>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const props = defineProps({
  employee: Object,
});

const router = useRouter();

const dismiss = async (employeeId) => {
  try {
    await axios.post(`/api/Employees/${employeeId}/dismiss/`);
    router.go();
    alert('Сотрудник уволен');
  } catch (error) {
    console.error('Ошибка', error);
    alert('Произошла оишбка');
  }
};

const show = ref(false);
</script>
