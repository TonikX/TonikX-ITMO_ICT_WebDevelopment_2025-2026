<template>
  <v-container>
    <!-- Форма добавления уборки (одна на всю страницу) -->
    <v-card class="pa-3 mb-4">
      <v-card-title>Добавить уборку</v-card-title>
      <v-card-text>
        <v-select
          v-model="newSchedule.floor"
          :items="[1,2,3,4,5]"
          label="Этаж"
          required
        />
        <v-select
          v-model="newSchedule.day_of_week"
          :items="dayNames"
          label="День недели"
          required
        />
        <v-select
          v-model="newSchedule.employee"
          :items="employees"
          item-title="last_name"
          item-value="id"
          label="Сотрудник"
          required
        />
        <v-btn color="primary" @click="addSchedule">Добавить уборку</v-btn>
      </v-card-text>
    </v-card>

    <!-- Список дней недели с уборками (по одному разу) -->
    <div v-for="day in 7" :key="day">
      <v-card class="pa-3 mb-4">
        <v-card-title>{{ days[day] }}</v-card-title>
        <v-card-text v-if="getSchedules(day).length">
          <v-card-text v-for="schedule in getSchedules(day)" :key="schedule.id" class="mb-2">
            Этаж {{ schedule.floor }} —
            <v-select
              :items="employees"
              item-title="last_name"
              item-value="id"
              v-model="schedule.employee"
              @update:model-value="save(schedule)"
              density="compact"
            />
          </v-card-text>
        </v-card-text>
        <v-card-text v-else>
          Уборок нет
        </v-card-text>
      </v-card>
    </div>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const props = defineProps({
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

const dayNames = Object.values(days);

const newSchedule = ref({
  floor: null,
  day_of_week: null,
  employee: null,
});

const getDayNumber = (dayName) => {
  return parseInt(Object.keys(days).find(key => days[key] === dayName));
};

const addSchedule = async () => {
  if (!newSchedule.value.floor || !newSchedule.value.day_of_week || !newSchedule.value.employee) {
    alert('Заполните все поля');
    return;
  }

  try {
    const payload = {
      floor: newSchedule.value.floor,
      day_of_week: getDayNumber(newSchedule.value.day_of_week),
      employee: newSchedule.value.employee,
    };
    await axios.post('/api/cleaning_schedules/', payload);
    alert('Уборка добавлена');
    newSchedule.value = { floor: null, day_of_week: null, employee: null };
    window.location.reload();
  } catch (error) {
    console.error('Ошибка при добавлении уборки', error);
    alert('Не удалось добавить уборку');
  }
};

const save = async (schedule) => {
  try {
    await axios.patch(`/api/cleaning_schedules/${schedule.id}/`, {
      employee: schedule.employee,
    });
  } catch (error) {
    console.error('Ошибка при сохранении уборки', error);
  }
};

const getSchedules = (day) => {
  return props.schedules.filter(s => s.day_of_week === day);
};
</script>