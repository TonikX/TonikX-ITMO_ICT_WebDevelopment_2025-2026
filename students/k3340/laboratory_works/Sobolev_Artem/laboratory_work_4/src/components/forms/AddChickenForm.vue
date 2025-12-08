<template>
  <form @submit.prevent="addChicken" class="add-form">
    <label class="add-form__label">
      <span class="add-form__label-title">Имя:</span>
      <input
          class="add-form__input"
          type="text"
          v-model="newChicken.name"
          placeholder="Введите имя"
          required
      />
    </label>

    <label class="add-form__label">
      <span class="add-form__label-title">Вес:</span>
      <input
          class="add-form__input"
          type="text"
          v-model.number="newChicken.weight"
          placeholder="Введите вес"
          min="0"
          required
      />
    </label>

    <label class="add-form__label">
      <span class="add-form__label-title">Порода:</span>
      <input
          class="add-form__input"
          type="text"
          v-model="newChicken.breedId"
          placeholder="Введите породу"
          required
      />
    </label>

    <label class="add-form__label">
      <span class="add-form__label-title">Клетка:</span>
      <input
          class="add-form__input"
          type="text"
          v-model="newChicken.cageId"
          placeholder="Введите номер клетки:"
          required
      />
    </label>

    <label class="add-form__label">
      <span class="add-form__label-title">Дата рождения:</span>
      <Datepicker
          v-model="newChicken.birthDate"
          :format="formatDate"
          placeholder="Выберите дату"
          :input-class="'add-form__input'"
          :max-date="new Date()"
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
import Button from "@/components/ui/Button.vue";
import {createChicken} from "@/api/chickens.js";
import Datepicker from "vue3-datepicker";

const emit = defineEmits(["close", "submit"]);

const newChicken = ref({
  name: "",
  weight: "",
  birthDate: null,
  breedId: "",
  cageId: "",
});

const addChicken = async () => {
  try {
    const today = new Date();
    const selectedDate = new Date(newChicken.value.birthDate);

    if (selectedDate > today) {
      alert("Укажите корректную дату рождения");
      return;
    }

    const chickenToSend = {
      name: newChicken.value.name.trim(),
      weight: newChicken.value.weight,
      breedId: newChicken.value.breedId,
      birthDate: selectedDate.toISOString().split("T")[0],
      cageId: newChicken.value.cageId,
    };

    await createChicken(chickenToSend);
    emit("submit", chickenToSend);
    emit("close");
  } catch (error) {
    console.error("Ошибка при добавлении курицы:", error);
  }
};

const formatDate = (date) => {
  if (!date) return "";
  const d = new Date(date);
  return d.toISOString().split("T")[0];
};
</script>
