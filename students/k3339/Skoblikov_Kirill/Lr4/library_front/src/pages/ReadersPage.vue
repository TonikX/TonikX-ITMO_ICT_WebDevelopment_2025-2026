<template>
  <div class="page">
    <LeftPanel
      @add="openAddModal"
      @update="openEditModal"
      @delete="deleteReader"
    />

    <ReaderList ref="readerListRef" />

    <ReaderForm
      v-if="showModal"
      :reader="editingReader"
      @save="saveReader"
      @close="closeModal"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import LeftPanel from '@/components/LeftPanel.vue';
import ReaderList from '@/components/ReaderList.vue';
import ReaderForm from '@/components/ReaderForm.vue';
import authAPI from '@/api/api.js';

const readerListRef = ref(null);
const showModal = ref(false);
const editingReader = ref(null);
const openAddModal = () => {
  editingReader.value = null;
  showModal.value = true;
};

const openEditModal = () => {
  const selectedId = readerListRef.value?.selectedReaderId;
  if (!selectedId) {
    alert('Выберите читателя для редактирования');
    return;
  }
  const reader = readerListRef.value?.readers.find(r => r.id === selectedId);
  if (reader) {
    editingReader.value = reader;
    showModal.value = true;
  }
};

const closeModal = () => {
  showModal.value = false;
  editingReader.value = null;
};

const saveReader = async (formData) => {
  try {
    if (editingReader.value) {
      await authAPI.updateReader(editingReader.value.id, formData);
    } else {
      await authAPI.createReader(formData);
    }
    await readerListRef.value?.loadReaders();
    closeModal();
  } catch (error) {
    console.error('Ошибка сохранения читателя:', error);
    alert('Не удалось сохранить читателя');
  }
};

const deleteReader = async () => {
  const selectedId = readerListRef.value?.selectedReaderId;
  if (!selectedId) {
    alert('Выберите читателя для удаления');
    return;
  }

  try {
    await authAPI.deleteReader(selectedId);
    await readerListRef.value?.loadReaders();
    readerListRef.value.selectedReaderId = null;
  } catch (error) {
    console.error('Ошибка удаления читателя:', error);
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