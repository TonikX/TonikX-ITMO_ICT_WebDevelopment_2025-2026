<template>
  <v-container>
    <div class="d-flex justify-space-between align-center mb-4">
      <h2>Сотрудники отеля</h2>
      <v-btn color="primary" to="/staff/new">+ Добавить сотрудника</v-btn>
    </div>

    <v-card v-if="loading" class="pa-4">
      <v-skeleton-loader type="list-item-three-line"></v-skeleton-loader>
    </v-card>

    <v-alert v-else-if="error" type="error">{{ error }}</v-alert>

    <StaffCard
        v-for="staff in staffs"
        :key="staff.id"
        :staff="staff"
        @delete="confirmDelete(staff)"
      />
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';
import StaffCard from '@/components/StaffCard.vue';


const staffs = ref([]);
const loading = ref(false);
const error = ref(null);
const router = useRouter();

const fetchStaffs = async () => {
  loading.value = true;
  error.value = null;
  try {
    const res = await api.get('api/staff/');
    staffs.value = res.data;
  } catch (err) {
    error.value = 'Не удалось загрузить список сотрудников';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const confirmDelete = (staff) => {
  if (confirm(`Удалить сотрудника ${ staff.last_name } ${staff.first_name } ${ staff.patronymic }? Это действие нельзя отменить.`)) {
    deleteStaff(staff.id);
  }
};

const deleteStaff = async (id) => {
  try {
    await api.delete(`api/staff/${id}/`);
    fetchStaffs(); 
  } catch (err) {
    alert('Ошибка при удалении сотрудника');
    console.error(err);
  }
};

onMounted(() => {
  fetchStaffs();
});
</script>