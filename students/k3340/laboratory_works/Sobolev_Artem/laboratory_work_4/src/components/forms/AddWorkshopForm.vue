<template>
  <form @submit.prevent="addWorkshop" class="add-form">
    <label class="add-form__label">
      <span class="add-form__label-title">Номер цеха:</span>
      <input
          class="add-form__input"
          type="number"
          min="0"
          v-model="newWorkshop.workshopNumber"
          placeholder="Введите номер цеха"
          required
      />
    </label>

    <Button
        label="Добавить"
        mode="violet"
        location="page-action"
        type="submit"
        style="align-self: center; margin-top: 24px;"
    />
  </form>
</template>

<script setup>
import { ref } from "vue";
import { createWorkshop } from "@/api/workshops.js";
import Button from "@/components/ui/Button.vue";

const emit = defineEmits(["close", "submit"]);

const newWorkshop = ref({
  workshopNumber: "",
});

const addWorkshop = async () => {
  try {
    const workshopToSend = {
      workshopNumber: Number(newWorkshop.value.workshopNumber),
    };

    await createWorkshop(workshopToSend);
    emit("submit", workshopToSend);
    emit("close");
  } catch (error) {
    console.error("Ошибка при добавлении цеха:", error);
  }
};
</script>

<style scoped>
.add-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.add-form__label {
  display: flex;
  flex-direction: column;
}

.add-form__label-title {
  font-weight: 500;
  margin-bottom: 4px;
}

.add-form__input {
  padding: 8px;
  border: 1px solid var(--sidebar-text);
  border-radius: 4px;
  background: var(--section-bg);
  color: var(--color);
}
</style>
