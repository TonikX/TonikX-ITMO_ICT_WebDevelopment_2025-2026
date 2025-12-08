<template>
  <form @submit.prevent="addCage" class="add-form">
    <label class="add-form__label">
      <span class="add-form__label-title">ID ряда:</span>
      <input
          class="add-form__input"
          type="number"
          min="1"
          v-model="rowId"
          placeholder="Введите ID ряда (число)"
          required
      />
    </label>

    <label class="add-form__label">
      <span class="add-form__label-title">Номер клетки:</span>
      <input
          class="add-form__input"
          type="number"
          min="1"
          v-model="newCage.cageNumber"
          placeholder="Введите номер клетки"
          required
      />
    </label>

    <div v-if="error" class="error-message">{{ error }}</div>

    <Button
        label="Добавить"
        mode="violet"
        location="page-action"
        type="submit"
        style="align-self: center; margin-top: 24px;"
        :loading="loading"
    />
  </form>
</template>

<script setup>
import { ref } from "vue";
import { createCage } from "@/api/cages.js";
import Button from "@/components/ui/Button.vue";

const emit = defineEmits(["close", "submit"]);

const newCage = ref({
  cageNumber: "",
});

const rowId = ref("");
const loading = ref(false);
const error = ref("");

const addCage = async () => {
  if (!rowId.value || isNaN(rowId.value) || rowId.value < 1) {
    error.value = "Введите корректный ID ряда (число больше 0)";
    return;
  }

  if (!newCage.value.cageNumber || newCage.value.cageNumber < 1) {
    error.value = "Введите корректный номер клетки (число больше 0)";
    return;
  }

  loading.value = true;
  error.value = "";

  try {
    const cageToSend = {
      cageNumber: Number(newCage.value.cageNumber),
    };

    console.log("Отправляемые данные для клетки:", {
      rowId: rowId.value,
      cageData: cageToSend
    });

    const result = await createCage(Number(rowId.value), cageToSend);

    console.log("Результат создания клетки:", result);

    if (result) {
      emit("submit", {
        ...cageToSend,
        rowId: Number(rowId.value)
      });
      emit("close");
    } else {
      error.value = "Не удалось создать клетку. Сервер не вернул результат.";
    }

  } catch (err) {
    console.error("Полная ошибка при добавлении клетки:", err);
  }
};
</script>