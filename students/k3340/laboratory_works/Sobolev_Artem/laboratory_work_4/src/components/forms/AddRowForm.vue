<template>
  <form @submit.prevent="addRow" class="add-form">
    <label class="add-form__label">
      <span class="add-form__label-title">ID цеха:</span>
      <input
          class="add-form__input"
          type="number"
          min="1"
          v-model="workshopId"
          placeholder="Введите ID цеха (число)"
          required
      />
    </label>

    <label class="add-form__label">
      <span class="add-form__label-title">Номер ряда:</span>
      <input
          class="add-form__input"
          type="number"
          min="1"
          v-model="newRow.rowNumber"
          placeholder="Введите номер ряда"
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
import { createRow } from "@/api/rows.js";
import Button from "@/components/ui/Button.vue";

const emit = defineEmits(["close", "submit"]);

const newRow = ref({
  rowNumber: "",
});

const workshopId = ref("");
const loading = ref(false);
const error = ref("");

const addRow = async () => {
  if (!workshopId.value || isNaN(workshopId.value) || workshopId.value < 1) {
    error.value = "Введите корректный ID цеха (число больше 0)";
    return;
  }

  if (!newRow.value.rowNumber || newRow.value.rowNumber < 1) {
    error.value = "Введите корректный номер ряда (число больше 0)";
    return;
  }

  loading.value = true;
  error.value = "";

  try {
    const rowToSend = {
      rowNumber: Number(newRow.value.rowNumber),
    };

    const result = await createRow(Number(workshopId.value), rowToSend);

    if (result) {
      emit("submit", {
        ...rowToSend,
        workshopId: Number(workshopId.value)
      });
      emit("close");
    }

  } catch (err) {
    console.error("Полная ошибка при добавлении ряда:", err);
  }

};
</script>
