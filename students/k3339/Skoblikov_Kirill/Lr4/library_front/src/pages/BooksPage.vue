<template>
  <div class="page">
    <LeftPanel
      @add="openAddModal"
      @update="openEditModal"
      @delete="deleteBook"
    />

    <BookList ref="bookListRef" />

    <BookForm
      v-if="showModal"
      :book="editingBook"
      @save="saveBook"
      @close="closeModal"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import LeftPanel from '@/components/LeftPanel.vue';
import BookList from '@/components/BookList.vue';
import BookForm from '@/components/BookForm.vue';
import authAPI from '@/api/api.js';

const bookListRef = ref(null);
const showModal = ref(false);
const editingBook = ref(null);

const openAddModal = () => {
  editingBook.value = null;
  showModal.value = true;
};

const openEditModal = () => {
  const selectedId = bookListRef.value?.selectedBookId;
  if (!selectedId) {
    alert('Выберите книгу для редактирования');
    return;
  }
  const book = bookListRef.value?.books.find(b => b.id === selectedId);
  if (book) {
    editingBook.value = book;
    showModal.value = true;
  }
};

const closeModal = () => {
  showModal.value = false;
  editingBook.value = null;
};

const saveBook = async (formData) => {
  try {
    if (editingBook.value) {
      await authAPI.updateBook(editingBook.value.id, formData);
    } else {
      await authAPI.createBook(formData);
    }
    await bookListRef.value?.loadBooks();
    closeModal();
  } catch (error) {
    console.error('Ошибка сохранения:', error);
    alert('Не удалось сохранить книгу');
  }
};

const deleteBook = async () => {
  const selectedId = bookListRef.value?.selectedBookId;
  if (!selectedId) {
    alert('Выберите книгу для удаления');
    return
  }

  try {
    await authAPI.deleteBook(selectedId);
    await bookListRef.value?.loadBooks();
    bookListRef.value.selectedBookId = null;
  } catch (error) {
    console.error('Ошибка удаления:', error);
    alert('Не удалось удалить книгу');
  }
};
</script>

<style scoped>

</style>
