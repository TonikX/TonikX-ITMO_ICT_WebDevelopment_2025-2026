<template>
  <v-container>
    <v-btn to="/guests" icon="mdi-arrow-left" class="mb-4"></v-btn>
    <GuestCard :guest="guest" @delete="handleDeleteGuest" />
    <v-btn
      color="success"
      class="mt-4"
      :to="`/livingRecords/new?guest=${guest.id}`"
    >
      + Добавить запись о проживании
    </v-btn>

    <h3 class="mt-6 mb-4">Записи о проживаннии</h3>

    <div v-if="loading">Загрузка записей проживания...</div>

    <div v-else-if="livingRecords.length === 0">
      Этот гость пока не проживал в нашем отеле.
    </div>

    <div v-else>
      <LivingRecordCard
        v-for="livingRecord in livingRecords"
        :key="livingRecord.id"
        :livingRecord="livingRecord"
        @delete="confirmDeleteLivingRecord(livingRecord)"
      />
    </div>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/api';
import GuestCard from '@/components/GuestCard.vue';
import LivingRecordCard from '@/components/LivingRecordCard.vue';

const route = useRoute();
const router = useRouter();
const guest = ref({});
const livingRecords = ref([]);
const loading = ref(false);
const error = ref(null);

const fetch = async () => {
  loading.value = true;
  error.value = null;
  try {
    const guestRes = await api.get(`api/guest/${route.params.id}/`);
    guest.value = guestRes.data;
    livingRecords.value = guest.value.living_records;
  } catch (err) {
    error.value = 'Не удалось загрузить информацию о госте';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  fetch();
});

const handleDeleteGuest = () => {
  if (confirm(`Удалить Гостя ${guest.value.number}?`)) {
    deleteGuest();
  }
};

const deleteGuest = async () => {
  try {
    await api.delete(`/guest/${guest.value.id}/`);
    router.push('/guests');
  } catch (err) {
    alert('Не удалось гостя');
    console.error(err);
  }
};

const confirmDeleteLivingRecord = (livingRecord) => {
  if (confirm(`Удалить запись о проживании ${livingRecord.id}?`)) {
    deleteLivingRecord(livingRecord.id);
  }
};

const deleteLivingRecord = async (livingRecordId) => {
  try {
    await api.delete(`/livingRecord/${livingRecordId}/`);
    fetch();
  } catch (err) {
    alert('Не удалось удалить запись о проживании');
    console.error(err);
  }
};
</script>