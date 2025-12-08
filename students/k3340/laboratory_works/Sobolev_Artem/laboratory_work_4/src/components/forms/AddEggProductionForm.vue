<template>
  <form @submit.prevent="addEggProduction" class="add-form">
    <label class="add-form__label">
      <span class="add-form__label-title">ID курицы:</span>
      <input
          class="add-form__input"
          type="number"
          min="1"
          v-model="newProduction.chickenId"
          placeholder="Введите ID курицы"
          required
      />
    </label>

    <label class="add-form__label">
      <span class="add-form__label-title">Месяц:</span>
      <input
          class="add-form__input"
          type="number"
          min="1"
          max="12"
          v-model="newProduction.month"
          placeholder="Введите месяц (1-12)"
          required
      />
    </label>

    <label class="add-form__label">
      <span class="add-form__label-title">Год:</span>
      <input
          class="add-form__input"
          type="number"
          min="2000"
          max="2100"
          v-model="newProduction.year"
          placeholder="Введите год"
          required
      />
    </label>

    <label class="add-form__label">
      <span class="add-form__label-title">Количество яиц:</span>
      <input
          class="add-form__input"
          type="number"
          min="0"
          v-model="newProduction.count"
          placeholder="Введите количество яиц"
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
import { createEggProduction } from "@/api/eggProductions.js";
import Button from "@/components/ui/Button.vue";

const emit = defineEmits(["close", "submit"]);

const newProduction = ref({
  chickenId: "",
  month: "",
  year: "",
  count: ""
});

const addEggProduction = async () => {
  try {
    const productionToSend = {
      month: Number(newProduction.value.month),
      year: Number(newProduction.value.year),
      count: Number(newProduction.value.count)
    };

    await createEggProduction(newProduction.value.chickenId, productionToSend);
    emit("submit", productionToSend);
    emit("close");
  } catch (error) {
    console.error("Ошибка при добавлении производства яиц:", error);
  }
};
</script>