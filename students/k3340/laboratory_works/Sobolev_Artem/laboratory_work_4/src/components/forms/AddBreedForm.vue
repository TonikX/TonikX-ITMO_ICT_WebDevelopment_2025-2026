<template>
  <form @submit.prevent="addBreed" class="add-form">
    <label class="add-form__label">
      <span class="add-form__label-title">Название:</span>
      <input
          class="add-form__input"
          type="text"
          v-model="newBreed.name"
          placeholder="Введите название породы"
          required
      />
    </label>

    <label class="add-form__label">
      <span class="add-form__label-title">Яиц в месяц:</span>
      <input
          class="add-form__input"
          type="number"
          min="0"
          v-model="newBreed.eggsNumber"
          placeholder="Введите среднее количество"
          required
      />
    </label>

    <label class="add-form__label">
      <span class="add-form__label-title">Вес:</span>
      <input
          class="add-form__input"
          type="number"
          min="0"
          v-model="newBreed.weight"
          placeholder="Введите средний вес"
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
import {ref} from "vue";
import {createBreed} from "@/api/breeds.js";
import Button from "@/components/ui/Button.vue";

const emit = defineEmits(["close", "submit"]);

const newBreed = ref({
  name: "",
  eggsNumber: "",
  weight: "",
});

const addBreed = async () => {
  try {
    const breedToSend = {
      name: newBreed.value.name.trim(),
      weight: newBreed.value.weight,
      eggsNumber: newBreed.value.eggsNumber,
    };

    await createBreed(breedToSend);
    emit("submit", breedToSend);
    emit("close");
  } catch (error) {
    console.error("Ошибка при добавлении породы:", error);
  }
};
</script>
