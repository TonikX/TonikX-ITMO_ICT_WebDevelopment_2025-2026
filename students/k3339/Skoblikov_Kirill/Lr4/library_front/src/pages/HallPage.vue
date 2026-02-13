<template>
  <div class="page">
    <LeftPanel
      @add="openAddModal"
      @update="openEditModal"
      @delete="deleteHall"
    />

    <HallList ref="hallListRef" />

    <HallForm
      v-if="showModal"
      :hall="editingHall"
      @save="saveHall"
      @close="closeModal"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import LeftPanel from '@/components/LeftPanel.vue';
import HallList from '@/components/HallList.vue';
import HallForm from '@/components/HallForm.vue';
import authAPI from '@/api/api.js';

const hallListRef = ref(null);
const showModal = ref(false);
const editingHall = ref(null);
const openAddModal = () => {
  editingHall.value = null;
  showModal.value = true;
};

const openEditModal = () => {
  const selectedId = hallListRef.value?.selectedHallNumber;
  if (!selectedId) {
    alert('Выберите зал для редактирования');
    return;
  }
  const hall = hallListRef.value?.halls.find(h => h.hall_number === selectedId);
  if (hall) {
    editingHall.value = hall;
    showModal.value = true;
  }
};

const closeModal = () => {
  showModal.value = false;
  editingHall.value = null;
};

const saveHall = async (formData) => {
  try {
    if (editingHall.value) {
      await authAPI.updateHall(editingHall.value.hall_number, formData);
    } else {
      await authAPI.createHall(formData);
    }
    await hallListRef.value?.loadHalls();
    closeModal();
  } catch (error) {
    console.error('Ошибка сохранения зала:', error);
    alert('Не удалось сохранить зал');
  }
};

const deleteHall = async () => {
  const selectedId = hallListRef.value?.selectedHallNumber;
  if (!selectedId) {
    alert('Выберите зал для удаления');
    return;
  }
  if (!confirm('Вы уверены, что хотите удалить зал?')) return;

  try {
    await authAPI.deleteHall(selectedId);
    await hallListRef.value?.loadHalls();
    hallListRef.value.selectedHallNumber = null;
  } catch (error) {
    console.error('Ошибка удаления зала:', error);
    alert('Не удалось удалить зал');
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