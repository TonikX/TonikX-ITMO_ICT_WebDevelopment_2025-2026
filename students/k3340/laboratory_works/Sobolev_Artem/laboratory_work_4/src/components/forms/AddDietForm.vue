<template>
  <form @submit.prevent="addDiet" class="add-form">
    <label class="add-form__label">
      <span class="add-form__label-title">Название:</span>
      <input
          class="add-form__input"
          type="text"
          v-model="newDiet.title"
          placeholder="Введите название диеты"
          required
      />
    </label>

    <label class="add-form__label">
      <span class="add-form__label-title">Код:</span>
      <input
          class="add-form__input"
          type="text"
          v-model="newDiet.code"
          minLength="2"
          placeholder="Введите код диеты"
          required
      />
    </label>

    <label class="add-form__label">
      <span class="add-form__label-title">Сезон:</span>
      <select class="add-form__select" v-model="newDiet.season">
        <option value="WINTER">Зима</option>
        <option value="SPRING">Весна</option>
        <option value="SUMMER">Лето</option>
        <option value="AUTUMN">Осень</option>
      </select>
    </label>

    <label class="add-form__label">
      <span class="add-form__label-title">Породы:</span>
      <Multiselect
          v-model="newDiet.breedIds"
          :options="breeds"
          :multiple="true"
          :close-on-select="false"
          :clear-on-select="false"
          :preserve-search="true"
          label="name"
          track-by="id"
          placeholder="Выберите породы"
          class="add-form__multiselect"
      />
    </label>

    <label class="add-form__label">
      <span class="add-form__label-title">Описание:</span>
      <textarea
          class="add-form__textarea"
          v-model="newDiet.description"
          placeholder="Введите описание диеты"
          rows="3"
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
import { ref, onMounted } from "vue";
import { createDiet } from "@/api/diets.js";
import { getBreeds } from "@/api/breeds.js";
import Button from "@/components/ui/Button.vue";
import Multiselect from "vue-multiselect";

const emit = defineEmits(["close", "submit"]);

const newDiet = ref({
  title: "",
  code: "",
  description: "",
  season: "SPRING",
  breedIds: [],
});

const breeds = ref([]);

const loadBreeds = async () => {
  try {
    breeds.value = await getBreeds();
  } catch (error) {
    console.error("Ошибка при загрузке пород:", error);
  }
};
onMounted(loadBreeds);

const addDiet = async () => {
  try {
    const dietToSend = {
      title: newDiet.value.title.trim(),
      code: newDiet.value.code.trim(),
      description: newDiet.value.description.trim(),
      season: newDiet.value.season,
      breedIds: newDiet.value.breedIds.map(Number),
    };

    if (!dietToSend.title || !dietToSend.code) {
      return;
    }

    await createDiet(dietToSend);
    emit("submit", dietToSend);
    emit("close");
  } catch (error) {
    console.error("Ошибка при добавлении диеты:", error);
  }
};
</script>

<style lang="scss">
.add-form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 16px;

  &__label {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 12px;
  }

  &__label-title {
    color: var(--color-text);
    font-size: 20px;
    font-weight: 600;
  }

  &__input {
    font-size: 16px;
    border-radius: 4px;
    width: 400px;
    padding: 8px;
    font-weight: 500;
    background: var(--color-bg-light);
    color: var(--color-text-light);
  }

  &__input::placeholder {
    color: #686590;
    font-weight: 400;
  }

  &__select {
    width: 400px;
    height: 32px;
    font-weight: 500;
    font-size: 16px;
    border-radius: 4px;
    outline: none;
    padding-left: 12px;
    background: var(--color-bg-light);
    appearance: none;
    background-image: url('@/assets/icons/select-arrow.svg');
    background-repeat: no-repeat;
    background-position: right 12px center;
    background-size: 12px;
    color: #686590;
  }

  &__select-option {
    font-weight: 500;
    font-size: 16px;
    color: var(--color-text-light);
    width: 168px;
    outline: none;
  }

  &__textarea {
    width: 400px;
    resize: vertical;
    max-height: 180px;
    min-height: 60px;
    padding: 8px;
    font-size: 16px;
    background: var(--form-input-bg);
    border-radius: 4px;
    color: var(--color-text-light);
    font-weight: 500;
  }

  &__textarea::placeholder {
    color: #686590;
    font-weight: 400;
  }
}
</style>
