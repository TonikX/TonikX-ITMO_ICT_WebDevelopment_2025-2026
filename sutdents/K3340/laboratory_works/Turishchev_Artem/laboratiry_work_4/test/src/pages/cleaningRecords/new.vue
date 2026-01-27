<template>
  <v-container>
    <v-card class="pa-6">
      <v-card-title>Добавить запись уборки</v-card-title>
      <v-form @submit.prevent="submit">
        <v-select
          v-model="form.staff"
          :items="staff"
          item-title="last_name"
          item-value="id"
          label="Служащий"
          required
          :rules="[v => !!v || 'Обязательно']"
        ></v-select>
        <v-select
          v-model="form.floor"
          :items="floors"
          item-title="number"
          item-value="id"
          label="Этаж"
          required
          :rules="[v => !!v || 'Обязательно']"
        ></v-select>
        <v-text-field
          v-model="form.cleaning_date"
          label="Дата уборки"
          type="date"
          required
          :rules="[v => !!v || 'Обязательно указать дату заезда']"
        ></v-text-field>

        <v-card-actions>
          <v-btn to="/cleaningschedules" variant="outlined">Отмена</v-btn>
          <v-spacer></v-spacer>
          <v-btn
            type="submit"
            color="success"
            :loading="loading"
          >
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/api';

const route = useRoute();
const router = useRouter();
const form = ref({
  staff: null,
  floor: null,
  cleaning_date: '',
});
const loading = ref(false);
const CleaningRecordId = route.params.id;
const staff = ref([]);
const floors = ref([]);

onMounted(async () => {
  try {
    const resStaffs = await api.get(`api/staff/`);
    staff.value = resStaffs.data;
    const resFloors = await api.get(`api/floor/`);
    floors.value = resFloors.data;
  } catch (err) {
    alert('Не удалось загрузить данные для записи уборки');
    console.error(err);
  }
});

const submit = async () => {
  loading.value = true;
  try {
    await api.post('api/cleaning_record/', form.value);
    router.push('/cleaningRecords');
  } catch (err) {
    const errors = err.response?.data;
    let msg = 'Ошибка создания записи уборки';
    if (errors) {
      msg = Object.entries(errors)
        .map(([field, msgs]) => `${field}: ${msgs.join(', ')}`)
        .join('\n');
    }
    alert(msg);
    console.error(err);
  } finally {
    loading.value = false;
  }
};
</script>