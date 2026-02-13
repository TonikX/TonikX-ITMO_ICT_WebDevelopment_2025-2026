<template>
  <div class="page">
    <LeftPanel
      @add="openAddModal"
      @update="openEditModal"
      @delete="deleteReading"
    />

    <ReadingList ref="readingListRef" />

    <ReadingForm
      v-if="showModal"
      :reading="editingReading"
      @save="saveReading"
      @close="closeModal"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import LeftPanel from '@/components/LeftPanel.vue';
import ReadingList from '@/components/ReadingList.vue';
import ReadingForm from '@/components/ReadingForm.vue';
import authAPI from '@/api/api.js';

const readingListRef = ref(null);
const showModal = ref(false);
const editingReading = ref(null);
const openAddModal = () => {
  editingReading.value = null;
  showModal.value = true;
};

const openEditModal = () => {
  const selectedId = readingListRef.value?.selectedReadingId;
  if (!selectedId) {
    alert('Выберите запись для редактирования');
    return;
  }
  const reading = readingListRef.value?.readings.find(r => r.reading_id === selectedId);
  if (reading) {
    editingReading.value = reading;
    showModal.value = true;
  }
};

const closeModal = () => {
  showModal.value = false;
  editingReading.value = null;
};

const saveReading = async (formData) => {
  try {
    const payload = {
      ...formData,
      returned_date: formData.returned_date || null
    };

    if (editingReading.value) {
      await authAPI.updateReading(editingReading.value.reading_id, payload);
    } else {
      await authAPI.createReading(payload);
    }
    await readingListRef.value?.loadReadings();
    closeModal();
  } catch (error) {
    console.error('Ошибка сохранения выдачи:', error);
    alert('Не удалось сохранить запись');
  }
};

const deleteReading = async () => {
  const selectedId = readingListRef.value?.selectedReadingId;
  if (!selectedId) {
    alert('Выберите запись для удаления');
    return;
  }
  if (!confirm('Вы уверены, что хотите удалить запись о выдаче?')) return;

  try {
    await authAPI.deleteReading(selectedId);
    await readingListRef.value?.loadReadings();
    readingListRef.value.selectedReadingId = null;
  } catch (error) {
    console.error('Ошибка удаления записи:', error);
    alert('Не удалось удалить запись');
  }
};
</script>

<style scoped>
.page {
  display: flex;
  gap: 20px;
  width: 100%;
  min-height: 100vh;
}

.page > :last-child {
  flex: 1;
  min-width: 0;
}
</style>