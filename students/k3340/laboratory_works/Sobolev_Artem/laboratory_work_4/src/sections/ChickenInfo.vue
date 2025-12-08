<template>
  <div class="chicken page-block">
<!--    <div class="chicken__img-container">-->
<!--      <img class="chicken__img" :src="photo" alt="Chicken photo"/>-->
<!--    </div>-->

    <div class="chicken__container">
      <div class="chicken__info">
        <h2>Основная информация</h2>

        <h3 class="h2">Имя</h3>
        <span>Куриное имя</span>

        <h3 class="h2">Порода</h3>
        <span>Куриная порода</span>

        <h3 class="h2">Возраст</h3>
        <span>{{ age }}</span>
      </div>


      <div class="chicken__info">
        <h2>Данные</h2>
        <h3 class="h2">Вес</h3>
        <span>{{ weight }} g</span>

        <h3 class="h2">Яиц в месяц</h3>
        <span>Яйца</span>

        <h3 class="h2">Дата рождения</h3>
        <span>{{ formattedBirthDate }}</span>

      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { formatDate } from "@/utils/formatDate.js";

const props = defineProps({
  photo: String,
  name: String,
  weight: Number,
  birthDate: String,
  age: String,
});

const formattedBirthDate = computed(() => {
  return props.birthDate ? formatDate(props.birthDate) : "";
});
</script>

<style scoped lang="scss">
.chicken {
  display: flex;
  flex-direction: row;
  align-items: flex-start;

  &__container {
    width: 70%;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    margin-inline: auto;
    gap: 64px;
  }

  &__info {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  &__img-container {
    width: 14vw;
    height: 14vw;
    overflow: hidden;
    border-radius: 8px;
  }

  &__img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
}

.row,
.salary-row {
  display: flex;
  flex-direction: row;
  gap: 16px;
  align-items: center;
}
</style>
